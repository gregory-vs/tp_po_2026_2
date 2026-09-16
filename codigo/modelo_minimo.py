# -*- coding: utf-8 -*-
"""
Modelo mínimo de sequenciamento de projeto multidisciplinar.

Isto é o ESQUELETO: só precedência + recurso + minimizar prazo.
Serve para validar que a leitura dos dados está certa e que o modelo fecha.
Tudo o mais (revisões, zonas, órgãos públicos, reprogramação) entra depois, por cima.

Uso:
    python3 codigo/modelo_minimo.py dados/instancia_pequena
    python3 codigo/modelo_minimo.py dados/instancia_media
    python3 codigo/modelo_minimo.py dados/instancia_completa

Requer:  python3 -m pip install -r codigo/requirements.txt
"""
import sys

from dados import carregar_modelagem

try:
    import pulp
except ModuleNotFoundError:
    pulp = None


# ----------------------------------------------------------------- modelo ---
def resolver(pasta, horizonte=None, tempo_limite=120, log_solver=False):
    if pulp is None:
        print("ERRO: a biblioteca PuLP nao esta instalada.", file=sys.stderr)
        print("Instale com: python3 -m pip install -r codigo/requirements.txt", file=sys.stderr)
        sys.exit(2)

    atv, pre, dur, papeis, cap, praticado = carregar_modelagem(pasta)
    A = [a["id"] for a in atv]

    # horizonte: o prazo praticado ja e uma solucao viavel, entao serve de teto.
    # Se nao houver essa informacao, cai na soma das duracoes (sempre viavel).
    H = horizonte or praticado or sum(dur.values())
    print(f"atividades: {len(A)} | precedencias: {len(pre)} | horizonte: {H} dias")
    if praticado:
        print(f"prazo do cronograma praticado (referencia): {praticado} dias")
    T = range(H)

    m = pulp.LpProblem("sequenciamento_projeto", pulp.LpMinimize)

    # x[a][t] = 1 se a atividade a COMEÇA no dia t
    x = {a: {t: pulp.LpVariable(f"x_{a}_{t}", cat="Binary") for t in T} for a in A}
    Cmax = pulp.LpVariable("Cmax", lowBound=0)

    # Inicio e termino exclusivo como expressoes lineares.
    # Nos CSVs, fim_praticado e inclusivo: fim = inicio + duracao - 1.
    # No modelo, C = inicio + duracao facilita contar dias ativos como S <= t < C.
    S = {a: pulp.lpSum(t * x[a][t] for t in T) for a in A}
    C = {a: S[a] + dur[a] for a in A}
    F = {a: C[a] - 1 for a in A}

    # --- objetivo: terminar o quanto antes
    m += Cmax

    # --- (1) cada atividade começa exatamente uma vez
    for a in A:
        m += pulp.lpSum(x[a][t] for t in T) == 1, f"inicio_unico_{a}"

    # --- (2) precedência: respeita os quatro tipos de vínculo
    for k, p in enumerate(pre):
        i, j = p["predecessora"], p["sucessora"]
        lag = int(p.get("lag_dias", 0) or 0)
        tipo = p.get("tipo_vinculo", "TI") or "TI"
        if tipo == "TI":      # término -> início
            m += S[j] >= F[i] + lag, f"prec_{k}"
        elif tipo == "II":    # início -> início
            m += S[j] >= S[i] + lag, f"prec_{k}"
        elif tipo == "TT":    # término -> término
            m += F[j] >= F[i] + lag, f"prec_{k}"
        elif tipo == "IT":    # início -> término
            m += F[j] >= S[i] + lag, f"prec_{k}"

    # --- (3) capacidade: em cada dia, cada papel não passa da sua capacidade.
    # A atividade 'a' está em execução no dia t se começou em algum dia
    # entre t-duracao+1 e t.
    todos_papeis = sorted({p for lista in papeis.values() for p in lista})
    for r in todos_papeis:
        usa = [a for a in A if r in papeis[a]]
        if not usa:
            continue
        for t in T:
            m += pulp.lpSum(
                x[a][tau]
                for a in usa
                for tau in range(max(0, t - dur[a] + 1), t + 1)
            ) <= cap[r], f"cap_{r}_{t}"

    # --- (4) makespan
    for a in A:
        m += Cmax >= C[a], f"mksp_{a}"

    # --- resolver
    m.solve(pulp.PULP_CBC_CMD(msg=log_solver, timeLimit=tempo_limite))

    print()
    print("status  :", pulp.LpStatus[m.status])
    if m.status != 1:
        return
    mk = int(pulp.value(Cmax))
    print("makespan:", mk, "dias uteis")
    if praticado:
        print("praticado:", praticado, "dias uteis  ->  ganho de",
              praticado - mk, "dias (%.1f%%)" % (100.0 * (praticado - mk) / praticado))
    print()
    print("cronograma (inicio -> fim):")
    linhas = []
    for a in atv:
        i = int(sum(t * x[a["id"]][t].value() for t in T))
        linhas.append((i, i + dur[a["id"]] - 1, a["id"], a["nome"], a["papel"]))
    for i, f, aid, nome, pap in sorted(linhas)[:40]:
        print(f"  {aid:>5}  dia {i:>4} -> {f:>4}   {pap:<28} {nome[:46]}")
    if len(linhas) > 40:
        print(f"  ... (+{len(linhas)-40} atividades)")

    verificar_solucao(atv, pre, dur, papeis, cap,
                      {a: int(sum(t * x[a][t].value() for t in T)) for a in A})


def verificar_solucao(atv, pre, dur, papeis, cap, S):
    """Confere se a solucao respeita tudo. Nunca confie no solver sem isso."""
    C = {a: S[a] + dur[a] for a in S}
    F = {a: C[a] - 1 for a in S}
    erros = []
    for p in pre:
        i, j, lag, tp = (p["predecessora"], p["sucessora"],
                         int(p["lag_dias"] or 0), p["tipo_vinculo"])
        ok = (S[j] >= F[i] + lag if tp == "TI" else
              S[j] >= S[i] + lag if tp == "II" else
              F[j] >= F[i] + lag if tp == "TT" else
              F[j] >= S[i] + lag)
        if not ok:
            erros.append("precedencia %s %s->%s" % (tp, i, j))
    lim = max(C.values())
    for r in cap:
        usa = [a for a in S if r in papeis[a]]
        for t in range(lim + 1):
            n = sum(1 for a in usa if S[a] <= t < C[a])
            if n > cap[r]:
                erros.append("capacidade %s no dia %d: %d > %d" % (r, t, n, cap[r]))
                break
    print()
    if erros:
        print("VERIFICACAO: %d problema(s) -> %s" % (len(erros), erros[:5]))
    else:
        print("VERIFICACAO: solucao respeita todas as precedencias e capacidades.")


if __name__ == "__main__":
    pasta = sys.argv[1] if len(sys.argv) > 1 else "dados/instancia_pequena"
    limite = int(sys.argv[2]) if len(sys.argv) > 2 else None
    resolver(pasta, horizonte=limite)
