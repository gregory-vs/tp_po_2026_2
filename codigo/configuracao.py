"""Edite aqui os parametros da execucao iniciada por main.py."""
from pathlib import Path

RAIZ_PROJETO = Path(__file__).resolve().parents[1]
INSTANCIA = "instancia_completa"
PASTA_DADOS = RAIZ_PROJETO / "dados" / INSTANCIA

# 310 dias (indices 0..309): teto justificado pela referencia viavel auditada.
# None permite usar automaticamente o prazo de uma referencia validada.
# Sem referencia, e obrigatorio informar um horizonte; nao somamos duracoes.
HORIZONTE = 310
TEMPO_LIMITE_SEGUNDOS = 1800
# Exige inicio_praticado de todas as atividades e referencia viavel no horizonte.
USAR_WARM_START = True
MOSTRAR_LOG_SOLVER = False
TOLERANCIA_NUMERICA = 1e-6
PASTA_RESULTADOS = RAIZ_PROJETO / "resultados"
