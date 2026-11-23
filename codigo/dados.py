# -*- coding: utf-8 -*-
"""Leitura e convencoes comuns das instancias de cronograma."""
import csv
import json
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
    invalidas = [
        p for p in precedencias
        if p["predecessora"] not in ids or p["sucessora"] not in ids
    ]
    if invalidas:
        detalhes = "; ".join(
            f"{p['predecessora']}->{p['sucessora']}"
            for p in invalidas
        )
        raise ValueError(
            "Precedencias citam atividades ausentes do conjunto modelado: "
            + detalhes
            + ". Confira os identificadores; prepare recortes explicitamente."
        )
    return list(precedencias)


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
        ausentes = sorted({
            papel for lista in papeis.values() for papel in lista
            if papel not in capacidade
        })
        if ausentes:
            raise ValueError(
                "Equipes sem capacidade cadastrada em recursos.csv: "
                + ", ".join(ausentes)
                + ". Cadastre as capacidades antes de executar o modelo."
            )

    return capacidade


def tem_cronograma_praticado(atividades):
    return bool(atividades and all(
        a.get("inicio_praticado", "") != ""
        and a.get("fim_praticado", "") != ""
        and a.get("referencia_praticada_validada", "SIM") == "SIM"
        for a in atividades
    ))


def prazo_praticado(atividades):
    if not tem_cronograma_praticado(atividades):
        return 0
    fins = [int(a["fim_praticado"]) for a in atividades if a.get("fim_praticado")]
    return max(fins, default=-1) + 1


def fim_inclusivo(inicio, duracao):
    # Duracao zero representa um evento, sem intervalo de ocupacao.
    return inicio + max(duracao, 1) - 1


def termino_exclusivo(inicio, duracao):
    return inicio + duracao


def carregar_modelagem(pasta):
    status = ler_status_validacao(pasta)
    atividades, precedencias, recursos = ler_instancia(pasta)
    # Importacao local evita ciclo entre leitura e auditoria. Os CSVs sao lidos
    # uma unica vez e os mesmos registros conferidos seguem para o modelo.
    from codigo.verificar import auditar_dados

    falhas = auditar_dados(atividades, precedencias, recursos,
                          status=status, rotulo=str(pasta))
    if falhas:
        raise ValueError("Auditoria dos dados reprovada: " + "; ".join(falhas))
    atividades = atividades_reais(atividades)
    if not status and any(a.get("referencia_praticada_validada") == "NAO"
                          for a in atividades):
        raise ValueError("Base corrigida sem registro de validacao; confira validacao.json.")
    ids = {a["id"] for a in atividades}
    precedencias = precedencias_reais(precedencias, ids)
    duracao = duracoes(atividades)
    papeis = papeis_por_atividade(atividades)
    capacidade = capacidades(recursos, papeis)
    praticado = prazo_praticado(atividades)
    return atividades, precedencias, duracao, papeis, capacidade, praticado


def ler_status_validacao(pasta):
    caminho = os.path.join(pasta, "validacao.json")
    if not os.path.exists(caminho):
        return None
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)
