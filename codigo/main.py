"""Entrada principal. Edite codigo/configuracao.py e execute: python codigo/main.py."""
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from codigo import configuracao
from codigo.resolucao import resolver


def main():
    try:
        resultado = resolver(
            configuracao.PASTA_DADOS,
            horizonte=configuracao.HORIZONTE,
            tempo_limite=configuracao.TEMPO_LIMITE_SEGUNDOS,
            log_solver=configuracao.MOSTRAR_LOG_SOLVER,
            tolerancia=configuracao.TOLERANCIA_NUMERICA,
            pasta_resultados=configuracao.PASTA_RESULTADOS,
            warm_start=configuracao.USAR_WARM_START,
        )
    except (ValueError, RuntimeError, OSError) as erro:
        print("ERRO:", erro, file=sys.stderr)
        return 2
    return resultado.codigo_saida


if __name__ == "__main__":
    sys.exit(main())
