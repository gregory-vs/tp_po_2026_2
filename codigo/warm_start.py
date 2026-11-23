"""Prepara a referencia como sugestao completa, sem fixar variaveis."""
import re

from .dados import fim_inclusivo, tem_cronograma_praticado
from .validacao import verificar_solucao


def aplicar_referencia(variaveis, atividades, precedencias, duracoes, papeis,
                       capacidades, horizonte, tolerancia=1e-6):
    if not tem_cronograma_praticado(atividades):
        raise ValueError("Warm start requer referencia praticada completa e validada. "
                         "Desative USAR_WARM_START para executar sem referencia.")
    try:
        inicios = {a['id']: int(a['inicio_praticado']) for a in atividades}
    except (TypeError, ValueError) as erro:
        raise ValueError("Inicio praticado invalido para warm start.") from erro
    erros = verificar_solucao(atividades, precedencias, duracoes, papeis,
                              capacidades, inicios, horizonte=horizonte,
                              tolerancia=tolerancia)
    if erros:
        raise ValueError("Referencia rejeitada para warm start: " + "; ".join(erros))
    prazo = max(fim_inclusivo(inicios[a], duracoes[a]) for a in inicios) + 1
    for a, dias in variaveis.x.items():
        for t, x in dias.items():
            x.setInitialValue(int(t == inicios[a]))
    variaveis.Cmax.setInitialValue(prazo)
    return {"solicitado": True, "referencia_validada": True,
            "prazo_inicial": prazo, "atividades": len(inicios),
            "variaveis_inicializadas": sum(len(d) for d in variaveis.x.values()) + 1,
            "valores_lidos_cbc": None, "aceito_cbc": None,
            "custo_aceito_cbc": None}


def conferir_aceitacao(registro, log):
    """Ler o arquivo inicial nao significa aceita-lo como solucao viavel."""
    leitura = re.search(r"MIPStart values read for (\d+) variables", log, re.I)
    aceite = re.search(r"MIPStart provided solution with cost\s+"
                       r"([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)", log, re.I)
    if leitura:
        registro['valores_lidos_cbc'] = int(leitura.group(1))
    if aceite:
        registro['aceito_cbc'] = True
        registro['custo_aceito_cbc'] = float(aceite.group(1))
    elif re.search(r"mipstart.*could not be used|mipstart.*not valid", log, re.I):
        registro['aceito_cbc'] = False
