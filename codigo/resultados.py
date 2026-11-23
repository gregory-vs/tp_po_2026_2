"""Extracao e classificacao conservadora da saida PuLP 3.3.0/CBC."""
from dataclasses import dataclass, field
import math
from numbers import Real
import re

from .dados import fim_inclusivo, termino_exclusivo
from .validacao import verificar_solucao
from .variaveis import inicios_permitidos

VERSAO_PULP = "3.3.0"


@dataclass
class ResultadoResolucao:
    classificacao: str
    motivo_parada: str
    status_problema: str = ""
    status_solucao: str = ""
    tempo_segundos: float = 0.0
    versao_pulp: str = VERSAO_PULP
    versao_cbc: str | None = None
    caminho_log: str = ""
    caminho_registro: str = ""
    objetivo_bruto: float | None = None
    prazo: int | None = None
    inicios: dict = field(default_factory=dict)
    limite_inferior: float | None = None
    gap_relativo: float | None = None
    otimo_comprovado: bool = False
    erros: list = field(default_factory=list)
    avisos: list = field(default_factory=list)

    @property
    def aceita(self):
        return self.classificacao in ("otimo_comprovado", "viavel_sem_prova")

    @property
    def codigo_saida(self):
        if self.aceita:
            return 0
        return 2 if self.classificacao == "erro_execucao" else 1


def numero_finito(valor):
    return not isinstance(valor, bool) and isinstance(valor, Real) and math.isfinite(valor)


def ler_valor(expressao):
    return expressao.value() if hasattr(expressao, "value") else expressao


def interpretar_log_cbc(texto):
    """So usa mensagens finais explicitas; nao infere prova de um limite de tempo."""
    linhas = [linha.strip() for linha in texto.splitlines()]
    finais = [linha for linha in linhas if linha.startswith("Result -")]
    final = finais[-1] if finais else ""
    prova_otimo = final == "Result - Optimal solution found"
    prova_inviavel = (final == "Result - Problem proven infeasible" or
                      any(linha.startswith("Problem is infeasible") for linha in linhas))
    if prova_otimo:
        motivo = "otimo"
    elif "within gap tolerance" in final.lower():
        motivo = "limite_gap"
    elif "time limit" in final.lower():
        motivo = "limite_tempo"
    elif "node limit" in final.lower():
        motivo = "limite_nos"
    elif prova_inviavel:
        motivo = "inviavel"
    elif "unbounded" in final.lower():
        motivo = "ilimitado"
    elif final:
        motivo = "interrompido"
    else:
        motivo = "nao_identificado"
    limites = re.findall(r"^\s*Lower bound:\s*([-+0-9.eE]+)\s*$", texto, re.MULTILINE)
    limite = None
    if limites:
        try:
            valor = float(limites[-1])
            if math.isfinite(valor):
                limite = valor
        except ValueError:
            pass
    versao = re.search(r"^\s*Version:\s*(\S+)", texto, re.MULTILINE)
    return dict(motivo=motivo, prova_otimo=prova_otimo,
                prova_inviavel=prova_inviavel, limite_inferior=limite,
                versao_cbc=versao[1] if versao else None)


def extrair_inicios(variaveis, duracoes, horizonte, tolerancia=1e-6):
    """Confere os x antes de usar o indice escolhido; nao trunca uma soma ponderada."""
    erros, inicios = [], {}
    esperados = inicios_permitidos(duracoes, horizonte)
    if set(variaveis.x) != set(duracoes):
        return {}, ["IDs das variaveis de inicio diferem das atividades esperadas"]
    for a, dias in esperados.items():
        if set(variaveis.x[a]) != set(dias):
            erros.append(f"dominio de inicio incompleto ou inesperado em {a}")
            continue
        valores, escolhidos = [], []
        falha = False
        for t, variavel in variaveis.x[a].items():
            valor = ler_valor(variavel)
            if not numero_finito(valor):
                erros.append(f"valor ausente ou nao finito em x[{a},{t}]")
                falha = True
                break
            if min(abs(valor), abs(valor - 1)) > tolerancia:
                erros.append(f"valor nao binario em x[{a},{t}]: {valor}")
                falha = True
                break
            valores.append(valor)
            if abs(valor - 1) <= tolerancia:
                escolhidos.append(t)
        if falha:
            continue
        if len(escolhidos) != 1 or abs(math.fsum(valores) - 1) > tolerancia:
            erros.append(f"inicio unico nao atendido em {a}")
            continue
        inicio = escolhidos[0]
        # A pequena variacao dos x pode acumular-se na expressao ponderada.
        tolerancia_tempo = tolerancia * max(1, horizonte)
        expressoes = [(variaveis.S, inicio, "S"),
                      (variaveis.F, fim_inclusivo(inicio, duracoes[a]), "F"),
                      (variaveis.C, termino_exclusivo(inicio, duracoes[a]), "C")]
        for expressoes_a, esperado, nome in expressoes:
            valor = ler_valor(expressoes_a.get(a))
            if not numero_finito(valor) or abs(valor - esperado) > tolerancia_tempo:
                erros.append(f"expressao {nome} inconsistente em {a}")
        inicios[a] = inicio
    return inicios, erros


def avaliar_resultado(modelo, variaveis, atividades, precedencias, duracoes,
                      papeis, capacidades, horizonte, texto_log,
                      tempo_segundos=0.0, tolerancia=1e-6):
    import pulp

    evidencia = interpretar_log_cbc(texto_log)
    status = modelo.status
    sol_status = getattr(modelo, "sol_status", None)
    resultado = ResultadoResolucao(
        classificacao="sem_solucao", motivo_parada=evidencia["motivo"],
        status_problema=pulp.LpStatus.get(status, str(status)),
        status_solucao=pulp.LpSolution.get(sol_status, str(sol_status)),
        tempo_segundos=tempo_segundos,
        versao_cbc=evidencia["versao_cbc"],
    )
    tem_candidata = sol_status in (pulp.LpSolutionOptimal, pulp.LpSolutionIntegerFeasible)
    if status in (pulp.LpStatusInfeasible, pulp.LpStatusUnbounded):
        if tem_candidata:
            resultado.classificacao = "candidata_rejeitada"
            resultado.erros.append("status de termino contradiz a existencia de candidata")
        elif status == pulp.LpStatusInfeasible and evidencia["prova_inviavel"]:
            resultado.classificacao = "inviavel_comprovado"
        else:
            resultado.avisos.append("sem evidencia suficiente para classificar inviabilidade")
        return resultado
    if not tem_candidata:
        return resultado

    inicios, erros = extrair_inicios(variaveis, duracoes, horizonte, tolerancia)
    resultado.classificacao = "candidata_rejeitada"
    resultado.erros.extend(erros)
    if erros:
        return resultado
    erros = verificar_solucao(atividades, precedencias, duracoes, papeis,
                              capacidades, inicios, horizonte=horizonte,
                              tolerancia=tolerancia)
    resultado.erros.extend(erros)
    if erros:
        return resultado
    prazo = max(fim_inclusivo(inicios[a], duracoes[a]) for a in inicios) + 1
    bruto = ler_valor(variaveis.Cmax)
    if not numero_finito(bruto):
        resultado.erros.append("objetivo bruto ausente ou nao finito")
        return resultado
    resultado.objetivo_bruto = float(bruto)
    if bruto < prazo - tolerancia:
        resultado.erros.append("objetivo bruto nao cobre todas as entregas")
        return resultado
    resultado.inicios = inicios
    resultado.prazo = prazo
    resultado.classificacao = "viavel_sem_prova"
    objetivo_justo = abs(bruto - prazo) <= tolerancia
    if not objetivo_justo:
        resultado.avisos.append("objetivo bruto com folga; prazo calculado pelas entregas")
    if (status == pulp.LpStatusOptimal and sol_status == pulp.LpSolutionOptimal
            and evidencia["prova_otimo"] and objetivo_justo):
        resultado.classificacao = "otimo_comprovado"
        resultado.otimo_comprovado = True
        resultado.limite_inferior = float(prazo)
        resultado.gap_relativo = 0.0
    else:
        limite = evidencia["limite_inferior"]
        if limite is not None:
            if limite <= prazo + tolerancia:
                resultado.limite_inferior = limite
                # Formula do estudo; nao confundir com convencoes de gap do CBC.
                resultado.gap_relativo = max(0.0, (prazo - limite) / max(1, abs(prazo)))
            else:
                resultado.avisos.append("limite inferior incompativel com o prazo; gap indisponivel")
        if evidencia["prova_otimo"] and not resultado.otimo_comprovado:
            resultado.avisos.append("alegacao de otimo nao confirmada pelos demais dados")
    return resultado
