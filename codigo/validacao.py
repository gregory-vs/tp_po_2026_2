"""Conferencia independente, sem imprimir ou aceitar resultados antes da validacao."""
import math
from numbers import Real

from .dados import fim_inclusivo, termino_exclusivo


def verificar_solucao(atv, pre, dur, papeis, cap, S, horizonte=None, prazo=None,
                      tolerancia=1e-6):
    """prazo, se informado, e a duracao efetiva reportada, nao Cmax bruto."""
    if not (isinstance(tolerancia, Real) and math.isfinite(tolerancia)
            and 0 < tolerancia < 0.5):
        raise ValueError("Tolerancia deve estar entre zero e 0.5.")
    ids = [a["id"] for a in atv]
    esperados = set(ids)
    erros = []
    if not ids or len(ids) != len(esperados):
        erros.append("conjunto de atividades vazio ou com IDs duplicados")
    if not isinstance(S, dict):
        return erros + ["inicios devem ser um dicionario por atividade"]
    faltantes, extras = esperados - set(S), set(S) - esperados
    if faltantes:
        erros.append("atividades sem inicio: " + ", ".join(sorted(faltantes)))
    if extras:
        erros.append("inicios com IDs inesperados: " + ", ".join(sorted(extras)))
    if erros:
        return erros
    if horizonte is not None and (isinstance(horizonte, bool)
            or not isinstance(horizonte, int) or horizonte <= 0):
        return ["horizonte invalido"]
    inicios = {}
    for a in ids:
        valor = S[a]
        if (isinstance(valor, bool) or not isinstance(valor, Real)
                or not math.isfinite(valor)):
            erros.append(f"inicio ausente ou nao finito em {a}")
            continue
        if abs(valor - round(valor)) > tolerancia:
            erros.append(f"inicio nao inteiro em {a}")
            continue
        inicios[a] = round(valor)
        if inicios[a] < 0:
            erros.append(f"inicio negativo em {a}")
        if (a not in dur or isinstance(dur[a], bool)
                or not isinstance(dur[a], int) or dur[a] < 0):
            erros.append(f"duracao invalida em {a}")
        if a not in papeis or not papeis[a]:
            erros.append(f"atividade sem equipes: {a}")
        else:
            for equipe in papeis[a]:
                valor_cap = cap.get(equipe)
                if (isinstance(valor_cap, bool) or not isinstance(valor_cap, int)
                        or valor_cap < 0):
                    erros.append(f"capacidade ausente ou invalida: {equipe}")
    if erros:
        return erros
    C = {a: termino_exclusivo(inicios[a], dur[a]) for a in ids}
    F = {a: fim_inclusivo(inicios[a], dur[a]) for a in ids}
    for a in ids:
        if horizonte is not None and F[a] >= horizonte:
            erros.append(f"entrega de {a} fora do horizonte")
    prazo_efetivo = max(F.values()) + 1
    if prazo is not None and (isinstance(prazo, bool) or not isinstance(prazo, Real)
            or not math.isfinite(prazo) or abs(prazo - prazo_efetivo) > tolerancia):
        erros.append("prazo reportado diferente do ultimo dia de entrega mais um")
    for p in pre:
        i, j, tp = p["predecessora"], p["sucessora"], p["tipo_vinculo"]
        if i not in esperados or j not in esperados:
            erros.append(f"precedencia com ID ausente: {i}->{j}")
            continue
        try:
            lag = int(p["lag_dias"] or 0)
        except (ValueError, TypeError):
            erros.append(f"defasagem invalida em {i}->{j}")
            continue
        ok = (inicios[j] >= F[i] + lag if tp == "TI" else
              inicios[j] >= inicios[i] + lag if tp == "II" else
              F[j] >= F[i] + lag if tp == "TT" else
              F[j] >= inicios[i] + lag if tp == "IT" else False)
        if not ok:
            erros.append(f"precedencia {tp} {i}->{j}")
    if erros:
        return erros
    for equipe in {p for a in ids for p in papeis[a]}:
        usa = [a for a in ids if dur[a] > 0 and equipe in papeis[a]]
        for t in range(prazo_efetivo):
            n = sum(inicios[a] <= t < C[a] for a in usa)
            if n > cap[equipe]:
                erros.append(f"capacidade {equipe} no dia {t}: {n} > {cap[equipe]}")
                break
    return erros
