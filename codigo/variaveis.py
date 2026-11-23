"""Variaveis de decisao, dominios de inicio e expressoes de tempo."""
from dataclasses import dataclass

from .dados import fim_inclusivo, termino_exclusivo


@dataclass
class Variaveis:
    x: dict
    Cmax: object
    S: dict
    F: dict
    C: dict
    inicios: dict
    horizonte: int


def inicios_permitidos(duracoes, horizonte):
    """Positivos: 0..H-d; eventos: 0..H-1. Todas as entregas cabem em H."""
    if isinstance(horizonte, bool) or not isinstance(horizonte, int) or horizonte <= 0:
        raise ValueError("O horizonte deve ser um numero inteiro positivo de dias.")
    inicios = {}
    for atividade, duracao in duracoes.items():
        if isinstance(duracao, bool) or not isinstance(duracao, int) or duracao < 0:
            raise ValueError(f"Duracao invalida em {atividade}: {duracao}.")
        if duracao > horizonte:
            raise ValueError(
                f"A atividade {atividade} dura {duracao} dias e nao cabe "
                f"no horizonte de {horizonte} dias."
            )
        inicios[atividade] = range(horizonte - max(duracao, 1) + 1)
    return inicios


def criar_variaveis(duracoes, horizonte):
    inicios = inicios_permitidos(duracoes, horizonte)
    import pulp

    x = {
        a: {t: pulp.LpVariable(f"x_{a}_{t}", cat="Binary") for t in dias}
        for a, dias in inicios.items()
    }
    prazo = pulp.LpVariable("Cmax", lowBound=0)
    S = {a: pulp.lpSum(t * x[a][t] for t in dias) for a, dias in inicios.items()}
    F = {a: fim_inclusivo(S[a], d) for a, d in duracoes.items()}
    C = {a: termino_exclusivo(S[a], d) for a, d in duracoes.items()}
    return Variaveis(x=x, Cmax=prazo, S=S, F=F, C=C,
                     inicios=inicios, horizonte=horizonte)
