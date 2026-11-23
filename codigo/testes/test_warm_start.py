import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from codigo.resolucao import resolver
from codigo.variaveis import criar_variaveis
from codigo.warm_start import aplicar_referencia, conferir_aceitacao


class WarmStart(unittest.TestCase):
    def setUp(self):
        self.atv = [dict(id=a, nome=a, papel='R', inicio_praticado=str(s),
                         fim_praticado=str(s + 1))
                    for a, s in [('A', 0), ('B', 3), ('C', 5)]]
        self.dur = {a['id']: 2 for a in self.atv}
        self.pap = {a: ['R'] for a in self.dur}
        self.v = criar_variaveis(self.dur, 8)

    def preparar(self, horizonte=8, cap=1, pre=()):
        return aplicar_referencia(self.v, self.atv, list(pre), self.dur,
                                   self.pap, {'R': cap}, horizonte)

    def test_inicializa_todos_os_valores_sem_fixar(self):
        r = self.preparar()
        self.assertEqual(r['prazo_inicial'], 7)
        self.assertEqual(r['variaveis_inicializadas'], 22)
        for a in self.atv:
            for t, x in self.v.x[a['id']].items():
                self.assertEqual(x.value(), int(t == int(a['inicio_praticado'])))
                self.assertEqual((x.lowBound, x.upBound), (0, 1))
        self.assertEqual(self.v.Cmax.value(), 7)
        self.assertIsNone(self.v.Cmax.upBound)

    def test_rejeita_falta_de_referencia(self):
        del self.atv[0]['inicio_praticado']
        with self.assertRaisesRegex(ValueError, 'completa e validada'):
            self.preparar()

    def test_rejeita_capacidade_precedencia_e_horizonte_antes_de_inicializar(self):
        for kwargs in [dict(cap=0), dict(horizonte=6),
                       dict(pre=[dict(predecessora='C', sucessora='A', tipo_vinculo='TI', lag_dias='0')])]:
            with self.subTest(kwargs=kwargs), self.assertRaisesRegex(ValueError, 'rejeitada'):
                self.preparar(**kwargs)
            self.assertIsNone(self.v.Cmax.value())

    def test_leitura_nao_equivale_a_aceitacao(self):
        r = self.preparar()
        conferir_aceitacao(r, 'MIPStart values read for 22 variables.\n')
        self.assertEqual(r['valores_lidos_cbc'], 22)
        self.assertIsNone(r['aceito_cbc'])
        conferir_aceitacao(r, 'Cbc0045I Warning: mipstart values could not be used to build a solution.\n')
        self.assertIs(r['aceito_cbc'], False)

    def test_cbc_recebe_aceita_e_melhora_referencia_com_caminho_com_espacos(self):
        dados = (self.atv, [], self.dur, self.pap, {'R': 1}, 7)
        with tempfile.TemporaryDirectory(prefix='po warm start ') as temp:
            with patch('codigo.resolucao.carregar_modelagem', return_value=dados), \
                    contextlib.redirect_stdout(io.StringIO()):
                r = resolver('teste', horizonte=8, tempo_limite=5,
                             pasta_resultados=temp, warm_start=True)
            registro = json.loads(Path(r.caminho_registro).read_text(encoding='utf8'))
            inicial = registro['warm_start']
            self.assertTrue(r.aceita)
            self.assertEqual(r.prazo, 6)
            self.assertTrue(inicial['aceito_cbc'])
            self.assertEqual(inicial['custo_aceito_cbc'], 7)
            self.assertEqual(inicial['valores_lidos_cbc'], 22)
            self.assertTrue(registro['parametros_solver']['warmStart'])
            self.assertIn('-mips ', Path(r.caminho_log).read_text())


if __name__ == '__main__':
    unittest.main()
