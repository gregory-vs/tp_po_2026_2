"""Executa CBC, confere a candidata e so depois apresenta o resultado aceito."""
from dataclasses import asdict
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import platform
import tempfile
import time
from uuid import uuid4

from .dados import carregar_modelagem, fim_inclusivo
from .restricoes import adicionar_restricoes
from .resultados import ResultadoResolucao, VERSAO_PULP, avaliar_resultado
from .variaveis import criar_variaveis, inicios_permitidos
from .warm_start import aplicar_referencia, conferir_aceitacao


ROTULOS = {
    "otimo_comprovado": "Otimo comprovado (dentro das tolerancias numericas)",
    "viavel_sem_prova": "Solucao viavel sem prova de otimo",
    "sem_solucao": "Nenhuma solucao inteira encontrada",
    "inviavel_comprovado": "Solver informou prova de inviabilidade do modelo",
    "candidata_rejeitada": "Candidata rejeitada pela validacao",
    "erro_execucao": "Erro de execucao do solver",
}


def criar_solver_cbc(tempo_limite, caminho_log, warm_start=False):
    """Prepara CBC e um caminho temporario que sua interface consegue interpretar."""
    import pulp

    class CBCComInicio(pulp.PULP_CBC_CMD):
        # CBC 2.10.3 no Windows acrescenta .\ ao caminho do MIP start.
        # Um caminho absoluto deixa de ser valido. Usamos nomes relativos,
        # sem espacos, em uma pasta exclusiva; nao mudamos o diretorio atual.
        def solve_CBC(self, lp, use_mps=True):
            if not warm_start:
                return super().solve_CBC(lp, use_mps=use_mps)
            with tempfile.TemporaryDirectory(prefix='cbc-', dir=os.getcwd()) as pasta:
                self.pasta_relativa = Path(pasta).name
                return super().solve_CBC(lp, use_mps=use_mps)

        def create_tmp_files(self, name, *extensoes):
            if not warm_start:
                return super().create_tmp_files(name, *extensoes)
            return (str(Path(self.pasta_relativa) / ('modelo.' + ext)) for ext in extensoes)

    # keepFiles atende a interface Windows. O contexto acima limpa somente
    # a pasta temporaria desta chamada, inclusive se houver erro.
    solver = CBCComInicio(msg=False, timeLimit=tempo_limite,
                          warmStart=warm_start, keepFiles=warm_start,
                          gapRel=0, gapAbs=0, logPath=str(Path(caminho_log).resolve()))
    # PuLP 3.3.0 separa os argumentos dos arquivos temporarios por espacos.
    # No Windows, o nome curto aponta para a mesma pasta, sem mover arquivos.
    if not warm_start and os.name == "nt" and any(c.isspace() for c in solver.tmpDir):
        import ctypes
        from ctypes import wintypes

        obter_curto = ctypes.windll.kernel32.GetShortPathNameW
        obter_curto.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
        obter_curto.restype = wintypes.DWORD
        buffer = ctypes.create_unicode_buffer(32768)
        tamanho = obter_curto(solver.tmpDir, buffer, len(buffer))
        if not tamanho or tamanho >= len(buffer) or any(c.isspace() for c in buffer.value):
            raise RuntimeError("CBC precisa de um diretorio temporario sem espacos; nome curto indisponivel.")
        solver.tmpDir = buffer.value
    return solver


def apresentar_resultado(resultado, atividades, duracoes, referencia):
    print("\nSituacao:", ROTULOS[resultado.classificacao])
    print("Motivo de parada:", resultado.motivo_parada)
    print("Tempo do solver: %.3f s" % resultado.tempo_segundos)
    for erro in resultado.erros:
        print("ERRO:", erro)
    for aviso in resultado.avisos:
        print("AVISO:", aviso)
    if not resultado.aceita:
        return
    print("Validacao: cronograma conferido.")
    print("Prazo calculado:", resultado.prazo, "dias uteis")
    print("Objetivo bruto do solver:", resultado.objetivo_bruto)
    if referencia:
        ganho = referencia - resultado.prazo
        print("Referencia:", referencia, "dias -> ganho de", ganho,
              "dias (%.1f%%)" % (100.0 * ganho / referencia))
    if resultado.limite_inferior is not None:
        print("Limite inferior:", resultado.limite_inferior)
        print("Gap relativo do estudo: %.4f%%" % (100 * resultado.gap_relativo))
    else:
        print("Limite inferior e gap: indisponiveis.")
    print("\nCronograma (inicio -> entrega):")
    linhas = [(resultado.inicios[a["id"]],
               fim_inclusivo(resultado.inicios[a["id"]], duracoes[a["id"]]),
               a["id"], a["nome"], a["papel"]) for a in atividades]
    for inicio, fim, ident, nome, papel in sorted(linhas)[:40]:
        print(f"  {ident:>5} dia {inicio:>4} -> {fim:>4} {papel:<28} {nome[:46]}")
    if len(linhas) > 40:
        print(f"  ... (+{len(linhas)-40} atividades; todas constam no registro JSON)")


def resolver(pasta, horizonte=None, tempo_limite=120, log_solver=False,
             tolerancia=1e-6, pasta_resultados=None, warm_start=False):
    if not isinstance(warm_start, bool):
        raise ValueError("warm_start deve ser True ou False.")
    if not (isinstance(tolerancia, (int, float)) and math.isfinite(tolerancia)
            and 0 < tolerancia < 0.5):
        raise ValueError("Tolerancia deve estar entre zero e 0.5.")
    if (isinstance(tempo_limite, bool) or not isinstance(tempo_limite, (int, float))
            or not math.isfinite(tempo_limite) or tempo_limite <= 0):
        raise ValueError("Limite de tempo deve ser positivo e finito.")
    atv, pre, dur, papeis, cap, praticado = carregar_modelagem(pasta)
    if not atv:
        raise ValueError("A instancia nao contem atividades para modelar.")
    if horizonte is None:
        if not praticado:
            raise ValueError("Sem referencia validada. Defina HORIZONTE em codigo/configuracao.py.")
        H = praticado
    else:
        H = horizonte
    inicios_permitidos(dur, H)
    try:
        import pulp
    except ModuleNotFoundError as erro:
        raise RuntimeError("Instale as dependencias com: python -m pip install -r codigo/requirements.txt") from erro
    if pulp.__version__ != VERSAO_PULP:
        raise RuntimeError(f"PuLP {pulp.__version__} encontrado; este projeto requer {VERSAO_PULP}. "
                           "Instale codigo/requirements.txt no ambiente virtual do projeto.")
    print(f"Atividades: {len(atv)} | vinculos: {len(pre)} | horizonte: {H} dias")
    modelo = pulp.LpProblem("sequenciamento_projeto", pulp.LpMinimize)
    variaveis = criar_variaveis(dur, H)
    adicionar_restricoes(modelo, variaveis, pre, dur, papeis, cap)
    inicial = {"solicitado": False}
    if warm_start:
        inicial = aplicar_referencia(variaveis, atv, pre, dur, papeis, cap, H, tolerancia)
        print(f"Warm start: referencia conferida, prazo {inicial['prazo_inicial']} dias; inicios livres para melhoria.")
    destino = Path(pasta_resultados) if pasta_resultados is not None else Path(__file__).resolve().parents[1] / "resultados"
    destino.mkdir(parents=True, exist_ok=True)
    ident = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "-" + uuid4().hex[:8]
    log = destino / (ident + ".log")
    registro = destino / (ident + ".json")
    inicio = time.perf_counter()
    try:
        solver = criar_solver_cbc(tempo_limite, log, warm_start=warm_start)
        if not solver.available():
            raise RuntimeError("Executavel CBC nao esta disponivel neste ambiente.")
        modelo.solve(solver)
    except (pulp.PulpSolverError, OSError, RuntimeError) as erro:
        resultado = ResultadoResolucao("erro_execucao", "falha_na_chamada",
                                      tempo_segundos=time.perf_counter() - inicio,
                                      erros=[str(erro)])
    else:
        resultado = avaliar_resultado(
            modelo, variaveis, atv, pre, dur, papeis, cap, H,
            log.read_text(encoding="utf-8", errors="replace") if log.exists() else "",
            tempo_segundos=time.perf_counter() - inicio, tolerancia=tolerancia,
        )
        if resultado.classificacao == "inviavel_comprovado" and praticado and H >= praticado:
            resultado.avisos.append("Ha referencia auditada que cabe no horizonte; investigar a divergencia com o modelo.")
    if warm_start:
        conferir_aceitacao(inicial, log.read_text(encoding="utf-8", errors="replace") if log.exists() else "")
        if inicial['aceito_cbc'] is not True:
            resultado.avisos.append("Aceitacao do warm start pelo CBC nao confirmada; confira o log.")
        else:
            print(f"Warm start aceito pelo CBC: custo {inicial['custo_aceito_cbc']:g}.")
    resultado.caminho_log = str(log.resolve())
    resultado.caminho_registro = str(registro.resolve())
    documento = asdict(resultado)
    documento.update(instancia=str(Path(pasta).resolve()), horizonte=H,
                     referencia_dias=praticado, tolerancia=tolerancia,
                     solucao_validada=resultado.aceita, codigo_saida=resultado.codigo_saida,
                     versao_python=platform.python_version(), plataforma=platform.platform(),
                     solver="CBC",
                     warm_start=inicial,
                     parametros_solver={"timeLimit": tempo_limite, "gapRel": 0, "gapAbs": 0,
                                        "warmStart": warm_start},
                     formula_gap="max(0, (prazo-limite_inferior)/max(1, abs(prazo)))")
    registro.write_text(json.dumps(documento, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    if log_solver and log.exists():
        print(log.read_text(encoding="utf-8", errors="replace"))
    apresentar_resultado(resultado, atv, dur, praticado)
    print("Registro:", registro)
    print("Log CBC:", log if log.exists() else "indisponivel (falha antes da escrita)")
    return resultado
