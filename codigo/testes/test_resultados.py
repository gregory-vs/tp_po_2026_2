import contextlib
import io
import math
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import pulp

from codigo import main
from codigo.resolucao import apresentar_resultado, criar_solver_cbc, resolver
from codigo.resultados import ResultadoResolucao, avaliar_resultado
from codigo.restricoes import adicionar_restricoes
from codigo.validacao import verificar_solucao
from codigo.variaveis import criar_variaveis, inicios_permitidos


OTIMO = "Result - Optimal solution found\n"
TEMPO = "Result - Stopped on time limit\nLower bound: 3\n"


def candidata(inicio=2, bruto=4, duracao=2, horizonte=6):
    x = {t: float(t == inicio) for t in inicios_permitidos({'A': duracao}, horizonte)['A']}
    return SimpleNamespace(x={'A': x}, Cmax=bruto, S={'A': inicio},
                           F={'A': inicio + max(duracao, 1) - 1},
                           C={'A': inicio + duracao})


class ExtracaoEStatus(unittest.TestCase):
    def avaliar(self, v=None, status=1, sol_status=1, log=OTIMO):
        return avaliar_resultado(SimpleNamespace(status=status, sol_status=sol_status),
                                 v or candidata(), [{'id': 'A'}], [], {'A': 2},
                                 {'A': ['R']}, {'R': 1}, 6, log)

    def test_status_optimal_com_incumbente_de_timeout_nao_prova_otimo(self):
        r = self.avaliar(sol_status=pulp.LpSolutionIntegerFeasible, log=TEMPO)
        self.assertEqual(r.classificacao, 'viavel_sem_prova')
        self.assertFalse(r.otimo_comprovado)
        self.assertEqual(r.prazo, 4)
        self.assertAlmostEqual(r.gap_relativo, 0.25)

    def test_relaxacao_sem_incumbente_nao_e_extraida(self):
        r = self.avaliar(status=pulp.LpStatusNotSolved,
                         sol_status=pulp.LpSolutionNoSolutionFound, log=TEMPO)
        self.assertEqual(r.classificacao, 'sem_solucao')
        self.assertIsNone(r.prazo)
        self.assertEqual(r.inicios, {})

    def test_prova_consistente(self):
        r = self.avaliar()
        self.assertEqual(r.classificacao, 'otimo_comprovado')
        self.assertEqual(r.gap_relativo, 0)

    def test_sem_log_nao_declara_otimo_nem_gap_zero(self):
        r = self.avaliar(log='')
        self.assertEqual(r.classificacao, 'viavel_sem_prova')
        self.assertIsNone(r.gap_relativo)

    def test_parada_por_gap_nao_declara_otimo_global(self):
        r = self.avaliar(log='Result - Optimal solution found (within gap tolerance)\n')
        self.assertEqual(r.classificacao, 'viavel_sem_prova')
        self.assertEqual(r.motivo_parada, 'limite_gap')

    def test_objetivo_com_folga_preserva_cronograma_sem_prova(self):
        r = self.avaliar(candidata(bruto=7))
        self.assertTrue(r.aceita)
        self.assertEqual(r.prazo, 4)
        self.assertEqual(r.objetivo_bruto, 7)
        self.assertFalse(r.otimo_comprovado)

    def test_objetivo_abaixo_da_entrega_rejeita(self):
        r = self.avaliar(candidata(bruto=3))
        self.assertEqual(r.classificacao, 'candidata_rejeitada')
        self.assertIsNone(r.prazo)

    def test_objetivo_ausente_ou_infinito_rejeita(self):
        for bruto in (None, math.inf):
            with self.subTest(bruto=bruto):
                self.assertEqual(self.avaliar(candidata(bruto=bruto)).classificacao,
                                 'candidata_rejeitada')

    def test_ids_das_variaveis_nao_podem_faltar_ou_sobrar(self):
        for ids in ({}, {'A': {}, 'EXTRA': {}}):
            with self.subTest(ids=ids):
                v = candidata(); v.x = ids
                self.assertEqual(self.avaliar(v).classificacao, 'candidata_rejeitada')

    def test_expressao_derivada_incompativel_rejeita(self):
        v = candidata(); v.F['A'] = 5
        self.assertEqual(self.avaliar(v).classificacao, 'candidata_rejeitada')

    def test_valores_fracionarios_com_inicio_medio_inteiro_rejeitados(self):
        v = candidata()
        v.x['A'] = {t: 0.5 if t in (1, 3) else 0.0 for t in v.x['A']}
        self.assertEqual(self.avaliar(v).classificacao, 'candidata_rejeitada')

    def test_ruido_numerico_nao_trunca_indice(self):
        v = candidata(bruto=3.999999999)
        v.x['A'][0] = 1e-8
        v.x['A'][2] = 1 - 1e-8
        v.S['A'] = 1.99999998
        v.F['A'] = 2.99999998
        v.C['A'] = 3.99999998
        r = self.avaliar(v)
        self.assertTrue(r.aceita)
        self.assertEqual(r.inicios['A'], 2)
        self.assertEqual(r.prazo, 4)

    def test_duplo_inicio_ausencia_none_nan_e_dominio_incompleto(self):
        for alteracao in ('duplo', 'nenhum', 'None', 'nan', 'dominio'):
            with self.subTest(alteracao=alteracao):
                v = candidata()
                if alteracao == 'duplo': v.x['A'][0] = 1
                elif alteracao == 'nenhum': v.x['A'][2] = 0
                elif alteracao == 'None': v.x['A'][1] = None
                elif alteracao == 'nan': v.x['A'][1] = math.nan
                else: del v.x['A'][1]
                self.assertEqual(self.avaliar(v).classificacao, 'candidata_rejeitada')

    def test_inviabilidade_exige_evidencia(self):
        kwargs = dict(status=pulp.LpStatusInfeasible, sol_status=pulp.LpSolutionInfeasible)
        self.assertEqual(self.avaliar(log='', **kwargs).classificacao, 'sem_solucao')
        self.assertEqual(self.avaliar(log='Result - Problem proven infeasible\n', **kwargs).classificacao,
                         'inviavel_comprovado')

    def test_limite_incompativel_nao_gera_gap(self):
        r = self.avaliar(sol_status=pulp.LpSolutionIntegerFeasible,
                         log='Result - Stopped on time limit\nLower bound: 8\n')
        self.assertIsNone(r.gap_relativo)
        self.assertTrue(r.avisos)

    def test_rejeitada_nao_exibe_prazo_ou_ganho(self):
        r = self.avaliar(candidata(bruto=3))
        saida = io.StringIO()
        with contextlib.redirect_stdout(saida):
            apresentar_resultado(r, [], {}, 310)
        self.assertNotIn('ganho', saida.getvalue())
        self.assertNotIn('Prazo calculado:', saida.getvalue())

    def test_main_propaga_codigo_de_saida(self):
        for classe, codigo in [('viavel_sem_prova', 0), ('sem_solucao', 1),
                               ('candidata_rejeitada', 1), ('erro_execucao', 2)]:
            with self.subTest(classe=classe), patch.object(main, 'resolver',
                    return_value=ResultadoResolucao(classe, 'teste')):
                self.assertEqual(main.main(), codigo)


class ValidadorIndependente(unittest.TestCase):
    def verificar(self, S, **kwargs):
        return verificar_solucao([{'id': 'A'}], [], {'A': 2}, {'A': ['R']},
                                  {'R': 1}, S, horizonte=6, **kwargs)

    def test_atividade_isolada_ausente_nao_passa(self):
        self.assertTrue(self.verificar({}))

    def test_atividade_extra_fracao_e_nao_finito_nao_passam(self):
        for S in ({'A': 0, 'B': 1}, {'A': 0.5}, {'A': math.inf}, {'A': None}):
            with self.subTest(S=S): self.assertTrue(self.verificar(S))

    def test_negativo_horizonte_e_prazo_incorretos(self):
        self.assertTrue(self.verificar({'A': -1}))
        self.assertTrue(self.verificar({'A': 5}))
        self.assertTrue(self.verificar({'A': 0}, prazo=5))

    def test_evento_na_entrega_nao_ocupa_segunda_vaga(self):
        erros = verificar_solucao([{'id': 'A'}, {'id': 'E'}],
            [dict(predecessora='A', sucessora='E', tipo_vinculo='TI', lag_dias='0')],
            {'A': 2, 'E': 0}, {'A': ['R'], 'E': ['R']}, {'R': 1},
            {'A': 0, 'E': 1}, horizonte=2, prazo=2)
        self.assertEqual(erros, [])

    def test_capacidade_e_vinculo_invalidos(self):
        a = [{'id': 'A'}, {'id': 'B'}]
        pre = [dict(predecessora='A', sucessora='B', tipo_vinculo='TI', lag_dias='0')]
        argumentos = (a, pre, {'A': 2, 'B': 2}, {'A': ['R'], 'B': ['R']}, {'R': 1})
        self.assertTrue(verificar_solucao(*argumentos, {'A': 0, 'B': 0}, horizonte=4))
        self.assertTrue(verificar_solucao(a, [], argumentos[2], argumentos[3], argumentos[4],
                                         {'A': 0, 'B': 0}, horizonte=4))


class IntegracaoCBC(unittest.TestCase):
    def executar(self, dur, horizonte, pre=()):
        self.assertEqual(pulp.__version__, '3.3.0')
        self.assertTrue(pulp.PULP_CBC_CMD(msg=False).available(), 'CBC deve estar instalado')
        with tempfile.TemporaryDirectory(prefix='po teste ') as temp:
            log = Path(temp) / 'cbc.log'
            m = pulp.LpProblem('teste', pulp.LpMinimize)
            v = criar_variaveis(dur, horizonte)
            pap = {a: ['R'] for a in dur}
            adicionar_restricoes(m, v, list(pre), dur, pap, {'R': 1})
            m.solve(criar_solver_cbc(5, log))
            return avaliar_resultado(m, v, [{'id': a} for a in dur], list(pre), dur,
                                      pap, {'R': 1}, horizonte, log.read_text())

    def test_dois_trabalhos_no_mesmo_recurso(self):
        r = self.executar({'A': 2, 'B': 2}, 4)
        self.assertEqual(r.classificacao, 'otimo_comprovado')
        self.assertEqual(r.prazo, 4)
        self.assertIsNotNone(r.versao_cbc)

    def test_solver_indisponivel_registra_erro_sem_mostrar_ganho(self):
        dados = ([dict(id='A', nome='A', papel='R')], [], {'A': 2},
                 {'A': ['R']}, {'R': 1}, 3)
        with tempfile.TemporaryDirectory(prefix='po teste ') as temp:
            saida = io.StringIO()
            with patch('codigo.resolucao.carregar_modelagem', return_value=dados), \
                    patch('codigo.resolucao.criar_solver_cbc',
                          return_value=SimpleNamespace(available=lambda: False)), \
                    contextlib.redirect_stdout(saida):
                r = resolver('teste', horizonte=3, pasta_resultados=temp)
            self.assertEqual(r.classificacao, 'erro_execucao')
            self.assertEqual(r.codigo_saida, 2)
            self.assertTrue(Path(r.caminho_registro).exists())
            self.assertNotIn('ganho de', saida.getvalue())

    def test_evento_terminal_com_espera(self):
        r = self.executar({'A': 2, 'E': 0}, 4,
                         [dict(predecessora='A', sucessora='E', tipo_vinculo='TI', lag_dias='2')])
        self.assertEqual(r.classificacao, 'otimo_comprovado')
        self.assertEqual(r.prazo, 4)
        self.assertEqual(r.inicios['E'], 3)

    def test_horizonte_curto_com_prova_de_inviabilidade(self):
        r = self.executar({'A': 2, 'B': 2}, 3)
        self.assertEqual(r.classificacao, 'inviavel_comprovado')
        self.assertFalse(r.aceita)

    def test_fluxo_completo_grava_json_apenas_apos_validacao(self):
        import csv
        import json
        with tempfile.TemporaryDirectory(prefix='po teste ') as temp:
            folder = Path(temp)
            entradas = {
                'atividades.csv': [dict(id='A', nome='Atividade A', nivel='ATIVIDADE',
                                       papel='R', duracao_dias='2')],
                'precedencias.csv': [],
                'recursos.csv': [dict(papel='R', capacidade='1')],
            }
            for nome, linhas in entradas.items():
                campos = list(linhas[0]) if linhas else ['predecessora', 'sucessora', 'tipo_vinculo', 'lag_dias']
                with (folder / nome).open('w', newline='', encoding='utf8') as arquivo:
                    w = csv.DictWriter(arquivo, fieldnames=campos, delimiter=';')
                    w.writeheader(); w.writerows(linhas)
            with contextlib.redirect_stdout(io.StringIO()):
                r = resolver(folder, horizonte=3, tempo_limite=5,
                             pasta_resultados=folder / 'saida')
            self.assertTrue(r.aceita)
            registro = json.loads(Path(r.caminho_registro).read_text(encoding='utf8'))
            self.assertEqual(registro['prazo'], 2)
            self.assertEqual(registro['inicios'], {'A': 0})
            self.assertTrue(Path(r.caminho_log).exists())


if __name__ == '__main__':
    unittest.main()
