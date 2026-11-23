"""Heuristica construtiva (esquema serial) e limites por caminho critico.

Este modulo nao usa o solver. Ele serve para tres coisas:

1. Calcular o limite inferior do prazo ignorando as equipes (caminho critico,
   CPM). Nenhum cronograma viavel pode terminar antes desse valor.
2. Construir cronogramas viaveis rapidamente com o esquema serial de geracao
   de cronogramas (serial SGS), tecnica classica do RCPSP: as atividades sao
   escolhidas uma a uma por uma regra de prioridade e cada uma entra no
   primeiro dia em que os vinculos e as capacidades permitem.
3. Rodar muitos cenarios de sensibilidade em segundos, o que o CBC nao
   consegue fazer na base completa.

Se o melhor cronograma da heuristica tiver prazo igual ao limite inferior, ele
e otimo para o modelo: nenhum cronograma pode ser menor que o limite e ele ja
atinge o limite. Se ficar acima, o valor e apenas um limite superior.

As convencoes de tempo sao as mesmas de restricoes.py:
  F = S + max(d, 1) - 1   (entrega inclusiva)
  ocupacao da equipe nos dias S .. S + d - 1 (duracao zero nao ocupa)
  TI: S[j] >= F[i] + lag     II: S[j] >= S[i] + lag
  TT: F[j] >= F[i] + lag     IT: F[j] >= S[i] + lag
  prazo = max(F) + 1
"""
import random
from collections import defaultdict


def _D(d):
    return max(d, 1)


def _lag(p):
    valor = p.get("lag_dias", "")
    return int(valor) if str(valor).strip() != "" else 0


def preparar_vinculos(precedencias):
    """Devolve (predecessoras, sucessoras) indexadas por atividade."""
    preds, succs = defaultdict(list), defaultdict(list)
    for p in precedencias:
        i, j, tipo = p["predecessora"], p["sucessora"], p["tipo_vinculo"]
        preds[j].append((i, tipo, _lag(p)))
        succs[i].append((j, tipo, _lag(p)))
    return preds, succs


def inicio_minimo(j, S, preds, dur):
    """Menor inicio de j dado o inicio das predecessoras ja programadas."""
    m = 0
    for i, tipo, lag in preds[j]:
        Fi = S[i] + _D(dur[i]) - 1
        if tipo == "TI":
            v = Fi + lag
        elif tipo == "II":
            v = S[i] + lag
        elif tipo == "TT":
            v = Fi + lag - (_D(dur[j]) - 1)
        else:  # IT
            v = S[i] + lag - (_D(dur[j]) - 1)
        m = max(m, v)
    return m


def ordem_topologica(ids, preds):
    pendentes = {a: len(preds[a]) for a in ids}
    succ = defaultdict(list)
    for j in ids:
        for i, _, _ in preds[j]:
            succ[i].append(j)
    fila = [a for a in ids if pendentes[a] == 0]
    ordem = []
    while fila:
        a = fila.pop()
        ordem.append(a)
        for j in succ[a]:
            pendentes[j] -= 1
            if pendentes[j] == 0:
                fila.append(j)
    if len(ordem) != len(ids):
        raise ValueError("A rede de vinculos tem ciclo.")
    return ordem


def caminho_critico(ids, precedencias, dur):
    """CPM sem equipes: inicio mais cedo, inicio mais tarde, folga total.

    Devolve (ES, LS, folga, limite_inferior).
    """
    preds, succs = preparar_vinculos(precedencias)
    ordem = ordem_topologica(list(ids), preds)
    ES = {}
    for a in ordem:
        ES[a] = inicio_minimo(a, ES, preds, dur)
    LB = max(ES[a] + _D(dur[a]) for a in ids)
    LS = {a: LB - _D(dur[a]) for a in ids}
    for i in reversed(ordem):
        for j, tipo, lag in succs[i]:
            if tipo == "TI":
                v = LS[j] - lag - (_D(dur[i]) - 1)
            elif tipo == "II":
                v = LS[j] - lag
            elif tipo == "TT":
                v = LS[j] + (_D(dur[j]) - 1) - lag - (_D(dur[i]) - 1)
            else:  # IT
                v = LS[j] + (_D(dur[j]) - 1) - lag
            LS[i] = min(LS[i], v)
    folga = {a: LS[a] - ES[a] for a in ids}
    return ES, LS, folga, LB


def esquema_serial(ids, precedencias, dur, papeis, cap, prioridade):
    """Serial SGS. prioridade(a) menor = escolhida antes entre as liberadas."""
    preds, _ = preparar_vinculos(precedencias)
    S = {}
    uso = defaultdict(lambda: defaultdict(int))
    faltam = set(ids)
    while faltam:
        liberadas = [j for j in faltam if all(i in S for i, _, _ in preds[j])]
        j = min(liberadas, key=prioridade)
        t = inicio_minimo(j, S, preds, dur)
        if dur[j] > 0:
            while any(uso[k][x] >= cap[k] for k in papeis[j]
                      for x in range(t, t + dur[j])):
                t += 1
            for k in papeis[j]:
                for x in range(t, t + dur[j]):
                    uso[k][x] += 1
        S[j] = t
        faltam.remove(j)
    return S


def prazo_de(S, dur):
    return max(S[a] + _D(dur[a]) for a in S)


def melhor_cronograma(ids, precedencias, dur, papeis, cap,
                      amostras_aleatorias=30, semente=2026):
    """Testa varias regras de prioridade e fica com o menor prazo.

    Regras deterministicas: menor inicio mais tarde (LST), menor folga,
    menor inicio mais cedo (EST), maior duracao. Depois, amostras aleatorias
    enviesadas pelo LST, com semente fixa para o resultado ser reprodutivel.
    """
    ids = list(ids)
    ES, LS, folga, LB = caminho_critico(ids, precedencias, dur)
    regras = {
        "menor_inicio_mais_tarde": lambda a: (LS[a], ES[a], a),
        "menor_folga": lambda a: (folga[a], LS[a], a),
        "menor_inicio_mais_cedo": lambda a: (ES[a], LS[a], a),
        "maior_duracao": lambda a: (-dur[a], LS[a], a),
    }
    melhor = None
    for nome, regra in regras.items():
        S = esquema_serial(ids, precedencias, dur, papeis, cap, regra)
        z = prazo_de(S, dur)
        if melhor is None or z < melhor[1]:
            melhor = (S, z, nome)
        if z == LB:
            return melhor[0], melhor[1], melhor[2], LB
    rng = random.Random(semente)
    for k in range(amostras_aleatorias):
        ruido = {a: rng.random() * (1 + folga[a]) for a in ids}
        S = esquema_serial(ids, precedencias, dur, papeis, cap,
                           lambda a: (LS[a] + ruido[a], a))
        z = prazo_de(S, dur)
        if z < melhor[1]:
            melhor = (S, z, f"amostra_{k}")
        if z == LB:
            break
    return melhor[0], melhor[1], melhor[2], LB
