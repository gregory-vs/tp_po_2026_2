"""Analise de sensibilidade: o que limita o prazo e o que vale a pena mudar.

Execute a partir da raiz do projeto:

    python codigo/sensibilidade.py

Nao chama o CBC e nao altera os CSVs. Cada cenario trabalha numa copia dos
parametros em memoria. Para cada cenario o script informa:

  LB   limite inferior pelo caminho critico (ignora equipes)
  UB   melhor cronograma viavel encontrado pela heuristica
  otimo  "sim" quando UB == LB (prova de otimalidade)

e grava em resultados/ um JSON com tudo e o cronograma da base.

A ideia e a mesma do preco-sombra da PL, mas medida por cenario: em PLI o
dual da relaxacao nao da o efeito exato de mudar um parametro, entao muda-se
o parametro, resolve-se de novo e mede-se quantos dias o prazo muda.
"""
import contextlib
import io
import json
import math
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from codigo import configuracao
from codigo.dados import carregar_modelagem
from codigo.heuristica import (caminho_critico, inicio_minimo, melhor_cronograma,
                               prazo_de, preparar_vinculos)
from codigo.validacao import verificar_solucao

# ---------------------------------------------------------------- parametros
# Reducoes percentuais testadas nas duracoes (0.2 = 20% mais rapido).
REDUCOES = (0.10, 0.20, 0.30, 0.50)
# Prazos maximos testados para a analise do cliente (SLA), em dias uteis.
SLA_ANALISE = (10, 5, 3)
AMOSTRAS_ALEATORIAS = 30


def reduzir(d, p):
    """Duracao reduzida em p, arredondada para cima, nunca abaixo de 1."""
    return d if d == 0 else max(1, math.ceil(d * (1 - p)))


def carregar(pasta):
    with contextlib.redirect_stdout(io.StringIO()):  # silencia a auditoria
        atv, pre, dur, papeis, cap, praticado = carregar_modelagem(pasta)
    return atv, pre, dur, papeis, cap, praticado


def resolver_cenario(ids, pre, dur, papeis, cap):
    S, ub, regra, lb = melhor_cronograma(ids, pre, dur, papeis, cap,
                                         amostras_aleatorias=AMOSTRAS_ALEATORIAS)
    return S, ub, lb, regra


def cadeia_ate_o_fim(ids, pre, dur, ES):
    """Uma cadeia de vinculos ativos que define o limite inferior."""
    preds = defaultdict(list)
    for p in pre:
        lag = int(p["lag_dias"] or 0)
        preds[p["sucessora"]].append((p["predecessora"], p["tipo_vinculo"], lag))
    D = lambda a: max(dur[a], 1)
    fim = max(ids, key=lambda a: ES[a] + D(a))
    cadeia, j = [fim], fim
    while True:
        prox = None
        for i, tipo, lag in preds[j]:
            Fi = ES[i] + D(i) - 1
            v = {"TI": Fi + lag, "II": ES[i] + lag,
                 "TT": Fi + lag - (D(j) - 1), "IT": ES[i] + lag - (D(j) - 1)}[tipo]
            if v == ES[j]:
                prox = i
                break
        if prox is None:
            break
        cadeia.append(prox)
        j = prox
    return list(reversed(cadeia))


def com_liberacao(ids, pre, dur, papeis, liberacao):
    """Proibe cada atividade de comecar antes de um dia (data de liberacao).

    liberacao = {atividade: dia}. Usa uma atividade ficticia sem equipe, de
    duracao dia + 1, ligada por TI lag 0: assim S[a] >= dia. A ficticia so
    representa a data; nao consome capacidade.
    """
    ids, pre, dur, papeis = list(ids), list(pre), dict(dur), dict(papeis)
    for a, dia in liberacao.items():
        f = "LIB_" + a
        ids.append(f)
        dur[f] = dia + 1
        papeis[f] = []
        pre.append({"predecessora": f, "sucessora": a, "tipo_vinculo": "TI", "lag_dias": "0"})
    return ids, pre, dur, papeis


def paralelizar(pre, corrente):
    """Desfaz uma corrente a1 -> a2 -> ... de emissoes feitas em sequencia.

    Retira os vinculos entre elementos consecutivos e da a cada um as mesmas
    predecessoras da primeira. Representa entregar as zonas em paralelo quando
    a ordem entre elas nao for tecnica.
    """
    cortes = set(zip(corrente, corrente[1:]))
    novo = [p for p in pre if (p["predecessora"], p["sucessora"]) not in cortes]
    herdadas = [p for p in pre if p["sucessora"] == corrente[0]]
    for b in corrente[1:]:
        novo += [dict(p, sucessora=b) for p in herdadas]
    return novo


def esperas_do_praticado(ids, pre, dur, praticado_inicio):
    """Dias que cada atividade esperou no praticado alem do que os vinculos exigem.

    Devolve (espera por atividade, caminho que fecha o prazo praticado).
    """
    preds, _ = preparar_vinculos(pre)
    espera = {a: praticado_inicio[a] - inicio_minimo(a, praticado_inicio, preds, dur)
              for a in ids}
    D = lambda a: max(dur[a], 1)
    fim = max(ids, key=lambda a: praticado_inicio[a] + D(a))
    caminho, j = [fim], fim
    while preds[j]:
        def limite(p):
            i, t, lag = p
            Fi = praticado_inicio[i] + D(i) - 1
            return {"TI": Fi + lag, "II": praticado_inicio[i] + lag,
                    "TT": Fi + lag - (D(j) - 1),
                    "IT": praticado_inicio[i] + lag - (D(j) - 1)}[t]
        j = max(preds[j], key=limite)[0]
        caminho.append(j)
    return espera, list(reversed(caminho))


# Correntes de emissoes por zona feitas em sequencia no AP (ver docs/analise-sensibilidade.md).
ZONAS_AP_INTERIORES = ["T114", "T115", "T116", "T117"]
ZONAS_AP_ARQUITETURA = ["T135", "T136", "T137", "T138", "T139"]
# Emissoes finais de ARQ no AP, uma por torre/embasamento, depois de receber as disciplinas.
ZONAS_AP_ARQUITETURA_FINAL = ["T255", "T256", "T257", "T258"]
# Mapas de esquadrias (rotulados EP no cronograma original, executados durante o AP).
MAPAS_DE_ESQUADRIAS = ["T141", "T142", "T143", "T144"]


def carga_das_equipes(S, dur, papeis, cap, prazo):
    uso = defaultdict(lambda: [0] * prazo)
    for a, s in S.items():
        for k in papeis[a]:
            for t in range(s, s + dur[a]):
                uso[k][t] += 1
    linhas = []
    for k, u in uso.items():
        ocup = sum(1 for x in u if x > 0)
        linhas.append({"equipe": k, "capacidade": cap[k], "pico_usado": max(u),
                       "dias_ocupada": ocup,
                       "dias_no_limite": sum(1 for x in u if x >= cap[k]),
                       "ocupacao_percentual": round(100 * ocup / prazo, 1)})
    return sorted(linhas, key=lambda r: -r["dias_ocupada"])


def main():
    pasta = configuracao.PASTA_DADOS
    atv, pre, dur, papeis, cap, praticado = carregar(pasta)
    A = {a["id"]: a for a in atv}
    ids = list(A)
    tipo = {a: A[a]["tipo"] for a in ids}
    disc = {a: A[a]["disciplina"] for a in ids}

    # ------------------------------------------------------------ base
    S0, ub0, lb0, regra0 = resolver_cenario(ids, pre, dur, papeis, cap)
    erros = verificar_solucao(atv, pre, dur, papeis, cap, S0,
                              horizonte=max(praticado, ub0), prazo=ub0)
    if erros:
        raise SystemExit("Cronograma da heuristica reprovado: " + "; ".join(erros))
    ES, LS, folga, _ = caminho_critico(ids, pre, dur)
    criticas = [a for a in ids if folga[a] == 0]
    cadeia = cadeia_ate_o_fim(ids, pre, dur, ES)

    print(f"Instancia: {pasta.name} | atividades {len(ids)} | vinculos {len(pre)}")
    print(f"Referencia praticada: {praticado} dias")
    print(f"Limite inferior (caminho critico, sem equipes): {lb0} dias")
    print(f"Heuristica: {ub0} dias (regra {regra0}) | validado pelo verificador: sim")
    print("Otimo comprovado: " + ("SIM" if ub0 == lb0 else "nao"))
    print(f"Reducao sobre a referencia: {praticado - ub0} dias "
          f"({100 * (praticado - ub0) / praticado:.1f}%)")
    print(f"Atividades com folga zero: {len(criticas)} de {len(ids)}")
    dias_tipo = Counter()
    for a in cadeia:
        dias_tipo[tipo[a]] += max(dur[a], 1)
    print(f"Cadeia que define o prazo: {len(cadeia)} atividades; dias por tipo: "
          + ", ".join(f"{k} {v}" for k, v in dias_tipo.most_common()))

    # -------------------------------------------------------- cenarios
    cenarios = []

    def rodar(grupo, nome, d=None, c=None, explicacao="", p=None, i=None, pap=None):
        d = dict(dur) if d is None else d
        c = dict(cap) if c is None else c
        p = pre if p is None else p
        i = ids if i is None else i
        pap = papeis if pap is None else pap
        _, ub, lb, _ = resolver_cenario(i, p, d, pap, c)
        cenarios.append({"grupo": grupo, "cenario": nome, "limite_inferior": lb,
                         "melhor_viavel": ub, "otimo_comprovado": ub == lb,
                         "variacao_dias": ub - ub0, "explicacao": explicacao})

    # 1. Equipes (capacidade)
    rodar("equipes", "todas as equipes +1", c={k: v + 1 for k, v in cap.items()},
          explicacao="contratar uma pessoa/frente a mais em todas as equipes")
    rodar("equipes", "todas as equipes -1 (minimo 1)",
          c={k: max(1, v - 1) for k, v in cap.items()},
          explicacao="quanto as equipes atuais tem de sobra")
    rodar("equipes", "todas as equipes com capacidade 1",
          c={k: 1 for k in cap},
          explicacao="cada equipe toca uma atividade por vez")
    for k in sorted(cap):
        if cap[k] > 1:
            c = dict(cap)
            c[k] -= 1
            rodar("equipes (uma a uma, -1)", k, c=c,
                  explicacao="tirar uma frente so dessa equipe")

    # 2. Duracoes por tipo de atividade
    for t in ("ANALISE", "EMISSAO"):
        for p in REDUCOES:
            d = {a: reduzir(v, p) if tipo[a] == t else v for a, v in dur.items()}
            rodar(f"duracao {t.lower()}", f"{t.lower()} {int(p * 100)}% mais rapida", d=d)
    for p in REDUCOES:
        d = {a: reduzir(v, p) for a, v in dur.items()}
        rodar("duracao geral", f"todas {int(p * 100)}% mais rapidas", d=d)

    # 3. Prazo maximo para a analise do cliente (SLA)
    for sla in SLA_ANALISE:
        d = {a: min(v, sla) if tipo[a] == "ANALISE" else v for a, v in dur.items()}
        rodar("sla de analise", f"analise do cliente em ate {sla} dias", d=d,
              explicacao="contrato/rotina que limita o tempo de retorno do cliente")

    # 4. Por disciplina (20% mais rapida em tudo daquela disciplina)
    for dd in sorted(set(disc.values())):
        d = {a: reduzir(v, 0.20) if disc[a] == dd else v for a, v in dur.items()}
        rodar("disciplina 20% mais rapida", dd, d=d)

    # 5. Largadas: atividades sem predecessora que, no praticado, comecaram
    #    depois do dia 0. O modelo deixa todas comecarem no dia 0. Aqui cada
    #    uma e presa na data praticada, primeiro sozinha (efeito no limite
    #    inferior) e depois todas juntas (cenario conservador).
    preds_base, _ = preparar_vinculos(pre)
    inicio_prat = {a: int(A[a]["inicio_praticado"]) for a in ids}
    tardias = [a for a in ids if not preds_base[a] and inicio_prat[a] > 0]
    largadas = []
    for a in tardias:
        i2, p2, d2, _ = com_liberacao(ids, pre, dur, papeis, {a: inicio_prat[a]})
        *_, lb = caminho_critico(i2, p2, d2)
        largadas.append({"id": a, "nome": A[a]["nome"], "papel": A[a]["papel"],
                         "inicio_praticado": inicio_prat[a], "efeito_no_limite": lb - lb0})
    largadas.sort(key=lambda r: -r["efeito_no_limite"])
    i2, p2, d2, pap2 = com_liberacao(ids, pre, dur, papeis,
                                     {a: inicio_prat[a] for a in tardias})
    rodar("largadas", f"todas as {len(tardias)} sem predecessora na data praticada",
          i=i2, p=p2, d=d2, pap=pap2,
          explicacao="cenario conservador: os atrasos de largada tinham motivo real")
    for a in ("T007", "T072"):
        i2, p2, d2, pap2 = com_liberacao(ids, pre, dur, papeis, {a: inicio_prat[a]})
        rodar("largadas", f"so {a} na data praticada (dia {inicio_prat[a]})",
              i=i2, p=p2, d=d2, pap=pap2)
    arq_ep = [a for a in ("T141", "T142", "T143", "T144") if a in tardias]
    i2, p2, d2, pap2 = com_liberacao(ids, pre, dur, papeis, {a: inicio_prat[a] for a in arq_ep})
    rodar("largadas", "so as emissoes de ARQ do EP (T141-T144) na data praticada",
          i=i2, p=p2, d=d2, pap=pap2)

    # 6. Medidas pontuais nas duas cadeias (interiores e arquitetura do AP)
    pre_ari = paralelizar(pre, ZONAS_AP_INTERIORES)
    pre_arq = paralelizar(pre, ZONAS_AP_ARQUITETURA)
    pre_ambas = paralelizar(pre_ari, ZONAS_AP_ARQUITETURA)
    rodar("medidas pontuais", "zonas do AP de interiores em paralelo", p=pre_ari)
    rodar("medidas pontuais", "zonas do AP de arquitetura em paralelo", p=pre_arq)
    rodar("medidas pontuais", "zonas do AP em paralelo (ARI e ARQ)", p=pre_ambas)
    for a, v in (("T026", 10), ("T166", 10)):
        d = dict(dur)
        d[a] = v
        rodar("medidas pontuais", f"{a} em {v} dias (era {dur[a]})", d=d)
    # T026 (analise da consultoria, 22 dias) e especifica deste empreendimento:
    # janela de decisao do cliente. Nao entra como medida; o cenario com ela
    # serve so como limite superior do ganho do pacote.
    d = dict(dur)
    d["T166"] = 10
    rodar("medidas pontuais", "zonas em paralelo (ARI e ARQ) + T166 em 10 dias",
          d=d, p=pre_ambas)
    d = dict(dur)
    d["T026"], d["T166"] = 10, 10
    rodar("medidas pontuais", "zonas em paralelo (ARI e ARQ) + T026 e T166 em 10 dias",
          d=d, p=pre_ambas,
          explicacao="limite superior: T026 e especifica deste projeto, nao e medida")

    # 7. Combinacoes de medidas gerais
    d = {a: reduzir(v, 0.20) if disc[a] in ("ARI", "ARQ") and tipo[a] == "EMISSAO" else v
         for a, v in dur.items()}
    rodar("combinacoes", "emissao ARI e ARQ 20% mais rapida", d=d)
    rodar("combinacoes", "emissao ARI e ARQ 20% + SLA de analise de 5 dias",
          d={a: min(v, 5) if tipo[a] == "ANALISE" else v for a, v in d.items()})

    # 8. Base com liberacoes: as 27 largadas tardias ficam presas na data
    #    praticada. No R14 original, a maioria delas depende de entregas do
    #    estudo preliminar de arquitetura que nao estao na base (bloco
    #    recolhido no PDF). Os cenarios abaixo medem as mesmas alavancas
    #    sobre essa base mais realista; a variacao e em relacao a ela.
    liberacao = {a: inicio_prat[a] for a in tardias}

    def base_lib(d=None, c=None, p=None):
        d = dict(dur) if d is None else d
        c = dict(cap) if c is None else c
        p = pre if p is None else p
        i2, p2, d2, pap2 = com_liberacao(ids, p, d, papeis, liberacao)
        S, ub, lb, _ = resolver_cenario(i2, p2, d2, pap2, c)
        return S, ub, lb, (i2, p2, d2)

    S_lib, ub_lib, lb_lib, (i_lib, p_lib, d_lib) = base_lib()
    S_lib_real = {a: S_lib[a] for a in ids}
    erros = verificar_solucao(atv, pre, dur, papeis, cap, S_lib_real,
                              horizonte=max(praticado, ub_lib), prazo=ub_lib)
    if erros or any(S_lib_real[a] < v for a, v in liberacao.items()):
        raise SystemExit("Cronograma da base com liberacoes reprovado: " + "; ".join(erros))
    ES_l, _, folga_l, _ = caminho_critico(i_lib, p_lib, d_lib)
    cadeia_lib = [a for a in cadeia_ate_o_fim(i_lib, p_lib, d_lib, ES_l)
                  if not a.startswith("LIB_")]
    cenarios_lib = []

    def rodar_lib(nome, **kw):
        _, ub, lb, _ = base_lib(**kw)
        cenarios_lib.append({"cenario": nome, "limite_inferior": lb, "melhor_viavel": ub,
                             "otimo_comprovado": ub == lb, "variacao_dias": ub - ub_lib})

    rodar_lib("todas as equipes +1", c={k: v + 1 for k, v in cap.items()})
    rodar_lib("todas as equipes -1 (minimo 1)", c={k: max(1, v - 1) for k, v in cap.items()})
    for t in ("ANALISE", "EMISSAO"):
        for pp in REDUCOES:
            rodar_lib(f"{t.lower()} {int(pp * 100)}% mais rapida",
                      d={a: reduzir(v, pp) if tipo[a] == t else v for a, v in dur.items()})
    for pp in REDUCOES:
        rodar_lib(f"todas {int(pp * 100)}% mais rapidas", d={a: reduzir(v, pp) for a, v in dur.items()})
    rodar_lib("analise do cliente em ate 5 dias",
              d={a: min(v, 5) if tipo[a] == "ANALISE" else v for a, v in dur.items()})
    for dd in ("ARQ", "CXO", "ARI"):
        rodar_lib(f"disciplina {dd} 20% mais rapida",
                  d={a: reduzir(v, 0.20) if disc[a] == dd else v for a, v in dur.items()})
    for pp in (0.10, 0.20):
        rodar_lib(f"mapas de esquadrias {int(pp * 100)}% mais rapidos",
                  d={a: reduzir(v, pp) if a in MAPAS_DE_ESQUADRIAS else v for a, v in dur.items()})
    rodar_lib("torres do AP final de arquitetura em paralelo",
              p=paralelizar(pre, ZONAS_AP_ARQUITETURA_FINAL))
    rodar_lib("emissao ARQ e CXO 10% mais rapida",
              d={a: reduzir(v, 0.10) if disc[a] in ("ARQ", "CXO") and tipo[a] == "EMISSAO" else v
                 for a, v in dur.items()})

    # 9. Esperas do cronograma praticado
    espera, caminho_prat = esperas_do_praticado(ids, pre, dur, inicio_prat)

    # 10. Marginal: -1 dia em cada atividade da cadeia (preco-sombra da duracao)
    marginal = []
    for a in cadeia:
        if dur[a] <= 1:
            continue
        d = dict(dur)
        d[a] -= 1
        *_, lb = caminho_critico(ids, pre, d)
        marginal.append({"id": a, "nome": A[a]["nome"], "papel": A[a]["papel"],
                         "duracao": dur[a], "limite_inferior_com_menos_1_dia": lb,
                         "ganho_no_limite": lb0 - lb})

    # ---------------------------------------------------------- saida
    print("\nCENARIOS (dias; variacao em relacao ao otimo da base)")
    print(f"{'grupo':30s} {'cenario':42s} {'LB':>4s} {'UB':>4s} {'otimo':>5s} {'var':>5s}")
    for c in cenarios:
        print(f"{c['grupo'][:30]:30s} {c['cenario'][:42]:42s} {c['limite_inferior']:4d} "
              f"{c['melhor_viavel']:4d} {'sim' if c['otimo_comprovado'] else 'nao':>5s} "
              f"{c['variacao_dias']:+5d}")
    print(f"\nPRATICADO: caminho que fecha os {praticado} dias "
          "(espera = dias parados alem do que os vinculos exigem)")
    for a in caminho_prat:
        print(f"  {a} {A[a]['nome'][:40]:40s} {A[a]['papel'][:16]:16s} "
              f"inicio {inicio_prat[a]:3d} duracao {dur[a]:3d} espera {espera[a]:3d}")
    print(f"  soma das esperas no caminho: {sum(espera[a] for a in caminho_prat)} dias")
    print(f"\nLARGADAS: {len(tardias)} atividades sem predecessora comecaram depois do dia 0")
    for r in largadas:
        if r["efeito_no_limite"] > 0:
            print(f"  {r['id']} {r['nome'][:40]:40s} {r['papel'][:16]:16s} "
                  f"dia {r['inicio_praticado']:3d}  presa nessa data: +{r['efeito_no_limite']}")
    print(f"\nBASE COM LIBERACOES ({len(liberacao)} largadas na data praticada): "
          f"{ub_lib} dias, LB {lb_lib}, " + ("otimo comprovado" if ub_lib == lb_lib else "sem prova")
          + f" | reducao sobre a referencia: {praticado - ub_lib} dias "
          f"({100 * (praticado - ub_lib) / praticado:.1f}%)")
    print("  cadeia: " + " -> ".join(cadeia_lib))
    for c in cenarios_lib:
        print(f"  {c['cenario'][:50]:50s} LB {c['limite_inferior']:4d} UB {c['melhor_viavel']:4d} "
              f"{'sim' if c['otimo_comprovado'] else 'nao':>3s} {c['variacao_dias']:+5d}")
    print("\nMARGINAL: -1 dia em cada atividade da cadeia critica")
    for m in marginal:
        print(f"  {m['id']} {m['nome'][:45]:45s} {m['papel']:16s} ganho {m['ganho_no_limite']} dia")

    destino = configuracao.PASTA_RESULTADOS
    destino.mkdir(parents=True, exist_ok=True)
    ident = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    saida = destino / f"sensibilidade-{ident}.json"
    registro = {
        "instancia": pasta.name, "referencia_dias": praticado,
        "limite_inferior": lb0, "heuristica_prazo": ub0, "heuristica_regra": regra0,
        "otimo_comprovado": ub0 == lb0, "solucao_validada": True,
        "parametros": {"reducoes": REDUCOES, "sla_analise": SLA_ANALISE,
                       "amostras_aleatorias": AMOSTRAS_ALEATORIAS},
        "inicios": S0,
        "folga_total": folga,
        "atividades_folga_zero": criticas,
        "cadeia_que_define_o_prazo": [
            {"id": a, "inicio_mais_cedo": ES[a], "duracao": dur[a], "tipo": tipo[a],
             "disciplina": disc[a], "fase": A[a]["fase"], "papel": A[a]["papel"]}
            for a in cadeia],
        "carga_das_equipes": carga_das_equipes(S0, dur, papeis, cap, ub0),
        "cenarios": cenarios,
        "marginal_cadeia": marginal,
        "praticado_caminho_que_fecha_o_prazo": [
            {"id": a, "papel": A[a]["papel"], "inicio": inicio_prat[a],
             "duracao": dur[a], "espera": espera[a]} for a in caminho_prat],
        "praticado_espera_por_disciplina": dict(Counter(
            {dd: sum(espera[a] for a in ids if disc[a] == dd) for dd in set(disc.values())}
        ).most_common()),
        "largadas_tardias": largadas,
        "base_com_liberacoes": {
            "liberacoes": liberacao, "prazo": ub_lib, "limite_inferior": lb_lib,
            "otimo_comprovado": ub_lib == lb_lib, "solucao_validada": True,
            "inicios": S_lib_real,
            "cadeia_que_define_o_prazo": [
                {"id": a, "inicio_mais_cedo": ES_l[a], "duracao": dur[a], "tipo": tipo[a],
                 "disciplina": disc[a], "fase": A[a]["fase"], "papel": A[a]["papel"]}
                for a in cadeia_lib],
            "atividades_folga_zero": [a for a in ids if folga_l[a] == 0],
            "cenarios": cenarios_lib,
        },
    }
    saida.write_text(json.dumps(registro, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nRegistro: {saida.relative_to(configuracao.RAIZ_PROJETO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
