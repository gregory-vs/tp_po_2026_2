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
from codigo.heuristica import caminho_critico, melhor_cronograma, prazo_de
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

    def rodar(grupo, nome, d=None, c=None, explicacao=""):
        d = dict(dur) if d is None else d
        c = dict(cap) if c is None else c
        _, ub, lb, _ = resolver_cenario(ids, pre, d, papeis, c)
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

    # 5. Marginal: -1 dia em cada atividade da cadeia (preco-sombra da duracao)
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
    }
    saida.write_text(json.dumps(registro, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nRegistro: {saida.relative_to(configuracao.RAIZ_PROJETO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
