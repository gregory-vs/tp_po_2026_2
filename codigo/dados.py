# -*- coding: utf-8 -*-
"""Leitura e convencoes comuns das instancias de cronograma."""
import csv
import os


TIPOS_VINCULO = ("TI", "II", "TT", "IT")


def ler_csv(caminho):
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        return list(csv.DictReader(arquivo, delimiter=";"))


def ler_instancia(pasta):
    atividades = ler_csv(os.path.join(pasta, "atividades.csv"))
    precedencias = ler_csv(os.path.join(pasta, "precedencias.csv"))
    recursos = ler_csv(os.path.join(pasta, "recursos.csv"))
    return atividades, precedencias, recursos


def atividades_reais(atividades):
    return [a for a in atividades if a.get("nivel", "ATIVIDADE") == "ATIVIDADE"]


def precedencias_reais(precedencias, ids):
    return [
        p for p in precedencias
        if p["predecessora"] in ids and p["sucessora"] in ids
    ]


def duracoes(atividades):
    return {a["id"]: int(a["duracao_dias"]) for a in atividades}


def papeis_por_atividade(atividades):
    return {
        a["id"]: [p.strip() for p in a["papel"].split(";") if p.strip()]
        for a in atividades
    }


def capacidades(recursos, papeis=None):
    if not recursos:
        capacidade = {}
    else:
        coluna = "capacidade" if "capacidade" in recursos[0] else "capacidade_sugerida"
        capacidade = {r["papel"]: int(r[coluna]) for r in recursos}

    if papeis:
        for lista in papeis.values():
            for papel in lista:
                capacidade.setdefault(papel, 1)

    return capacidade


def tem_cronograma_praticado(atividades):
    return bool(atividades and "inicio_praticado" in atividades[0])


def prazo_praticado(atividades):
    fins = [int(a["fim_praticado"]) for a in atividades if a.get("fim_praticado")]
    return max(fins, default=-1) + 1


def fim_inclusivo(inicio, duracao):
    return inicio + duracao - 1


def termino_exclusivo(inicio, duracao):
    return inicio + duracao


def carregar_modelagem(pasta):
    atividades, precedencias, recursos = ler_instancia(pasta)
    atividades = atividades_reais(atividades)
    ids = {a["id"] for a in atividades}
    precedencias = precedencias_reais(precedencias, ids)
    duracao = duracoes(atividades)
    papeis = papeis_por_atividade(atividades)
    capacidade = capacidades(recursos, papeis)
    praticado = prazo_praticado(atividades)
    return atividades, precedencias, duracao, papeis, capacidade, praticado
