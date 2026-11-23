import contextlib
import io
from pathlib import Path
import unittest

from codigo.dados import carregar_modelagem
from codigo.heuristica import caminho_critico, esquema_serial, melhor_cronograma, prazo_de
from codigo.validacao import verificar_solucao

RAIZ = Path(__file__).resolve().parents[2]


def carregar(nome):
    with contextlib.redirect_stdout(io.StringIO()):
        return carregar_modelagem(RAIZ / "dados" / nome)


class TestHeuristica(unittest.TestCase):
    def test_validacao_manual_atinge_o_otimo_conhecido(self):
        atv, pre, dur, pap, cap, _ = carregar("validacao_manual")
        ids = [a["id"] for a in atv]
        S, ub, _, lb = melhor_cronograma(ids, pre, dur, pap, cap)
        self.assertEqual(ub, 6)  # otimo resolvido a mao e pelo CBC
        self.assertEqual(verificar_solucao(atv, pre, dur, pap, cap, S, prazo=ub), [])
        self.assertLessEqual(lb, ub)

    def test_completa_viavel_e_dentro_dos_limites(self):
        atv, pre, dur, pap, cap, praticado = carregar("instancia_completa")
        ids = [a["id"] for a in atv]
        S, ub, _, lb = melhor_cronograma(ids, pre, dur, pap, cap)
        self.assertEqual(verificar_solucao(atv, pre, dur, pap, cap, S,
                                           horizonte=praticado, prazo=ub), [])
        self.assertLessEqual(lb, ub)
        self.assertLessEqual(ub, praticado)

    def test_capacidade_infinita_reproduz_o_caminho_critico(self):
        atv, pre, dur, pap, cap, _ = carregar("instancia_completa")
        ids = [a["id"] for a in atv]
        ES, LS, folga, lb = caminho_critico(ids, pre, dur)
        S = esquema_serial(ids, pre, dur, pap, {k: 10**6 for k in cap},
                           lambda a: (ES[a], a))
        self.assertEqual(prazo_de(S, dur), lb)
        self.assertTrue(all(v >= 0 for v in folga.values()))


if __name__ == "__main__":
    unittest.main()
