"""Auditoria de entrada, chamada automaticamente antes de montar o modelo.

Tambem pode ser executada separadamente: python codigo/verificar.py
Usa a instancia definida em codigo/configuracao.py.
"""
import sys
from collections import Counter, defaultdict
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from codigo.dados import (
    TIPOS_VINCULO, atividades_reais, capacidades, duracoes, fim_inclusivo,
    ler_instancia, ler_status_validacao, papeis_por_atividade, tem_cronograma_praticado,
)


def auditar_dados(A, P, R, status=None, rotulo="instancia"):
    """Confere dados ja lidos e retorna as falhas, sem chamar solver ou sair do Python."""
    at = atividades_reais(A)
    ids = {a['id'] for a in at}
    dur = duracoes(at)
    pap = papeis_por_atividade(at)
    cap = capacidades(R)
    tem_praticado = tem_cronograma_praticado(at)

    falhas = []
    def chk(nome, condicao, detalhe=''):
        ok = 'ok  ' if condicao else 'FALHA'
        if not condicao: falhas.append(nome + (': ' + detalhe if detalhe else ''))
        print('  [%s] %-46s %s' % (ok, nome, detalhe))

    print('\nAUDITORIA -', rotulo)
    print('=' * 72)
    print('atividades: %d | precedencias: %d | papeis: %d' % (len(at), len(P), len(R)))
    print()
    print('INTEGRIDADE')
    chk('todo id e unico', len(ids) == len(at))
    chk('nenhum nome duplicado',
        all(c == 1 for c in Counter(a['nome'] for a in at).values()))
    chk('nenhuma duracao negativa', all(d >= 0 for d in dur.values()))
    print('  [nota ] eventos de duracao zero: %d (sem ocupacao de equipe)' %
          sum(d == 0 for d in dur.values()))
    chk('toda atividade tem papel', all(pap[i] for i in ids))
    chk('todo papel esta em recursos.csv',
        all(p in cap for l in pap.values() for p in l),
        ', '.join(sorted({p for l in pap.values() for p in l if p not in cap})))
    chk('precedencias so citam ids existentes',
        all(p['predecessora'] in ids and p['sucessora'] in ids for p in P),
        '; '.join(p['predecessora'] + '->' + p['sucessora'] for p in P
                  if p['predecessora'] not in ids or p['sucessora'] not in ids))
    chk('sem auto-referencia', all(p['predecessora'] != p['sucessora'] for p in P))
    chk('sem precedencia duplicada',
        len(P) == len({(p['predecessora'], p['sucessora'], p['tipo_vinculo']) for p in P}))
    chk('tipos de vinculo validos',
        all(p['tipo_vinculo'] in TIPOS_VINCULO for p in P))

    # --- aciclicidade exigida pela estrutura de rede adotada neste estudo.
    # Em precedencias generalizadas, um ciclo nao prova sozinho inviabilidade.
    suc = defaultdict(list)
    for p in P: suc[p['predecessora']].append(p['sucessora'])
    cor, ciclos = {}, [0]
    sys.setrecursionlimit(20000)
    def dfs(u):
        cor[u] = 1
        for v in suc.get(u, []):
            if cor.get(v) == 1: ciclos[0] += 1
            elif cor.get(v, 0) == 0: dfs(v)
        cor[u] = 2
    for i in ids:
        if cor.get(i, 0) == 0: dfs(i)
    print()
    print('ESTRUTURA')
    chk('rede sem ciclo', ciclos[0] == 0, '%d arcos fechando ciclo' % ciclos[0])
    isoladas = ids - {p['predecessora'] for p in P} - {p['sucessora'] for p in P}
    print('  [nota ] %-46s %d' % ('atividades sem nenhum vinculo', len(isoladas)))

    if tem_praticado and not falhas:
        ini = {a['id']: int(a['inicio_praticado']) for a in at}
        fim = {a['id']: int(a['fim_praticado']) for a in at}
        print()
        print('COERENCIA COM O CRONOGRAMA PRATICADO')
        chk('entrega coerente com inicio e duracao',
            all(fim[i] == fim_inclusivo(ini[i], dur[i]) for i in ids))

        def respeita(p):
            a, b, lag = p['predecessora'], p['sucessora'], int(p['lag_dias'])
            t = p['tipo_vinculo']
            if t == 'TI': return ini[b] >= fim[a] + lag
            if t == 'II': return ini[b] >= ini[a] + lag
            if t == 'TT': return fim[b] >= fim[a] + lag
            if t == 'IT': return fim[b] >= ini[a] + lag
            return True
        ruins = [p for p in P if not respeita(p)]
        chk('praticado respeita todos os vinculos', not ruins, '%d violacoes' % len(ruins))

        # o praticado tem que caber na capacidade declarada, senao o modelo nao
        # consegue nem empatar com ele
        lim = max(fim.values())
        estouro = []
        for r in cap:
            usa = [i for i in ids if dur[i] > 0 and r in pap[i]]
            pico = max((sum(1 for i in usa if ini[i] <= t <= fim[i])
                        for t in range(lim + 1)), default=0)
            if pico > cap[r]: estouro.append((r, pico, cap[r]))
        chk('praticado cabe na capacidade declarada', not estouro,
            '; '.join('%s pico %d > cap %d' % e for e in estouro[:3]))
        print('  [nota ] %-46s %d dias uteis' % ('prazo do cronograma praticado', lim + 1))
    elif at and 'inicio_praticado' in at[0]:
        print('\nREFERENCIA: datas anteriores preservadas apenas para historico; nao validadas.')

    if status:
        print('\nCONFERENCIA COM A FONTE')
        chk('base conciliada para experimentos',
            status.get('pronta_para_experimentos', False), status.get('motivo', ''))

    print()
    print('=' * 72)
    if falhas:
        print('RESULTADO: %d verificacao(oes) falharam -> %s' % (len(falhas), ', '.join(falhas)))
        return falhas
    print('RESULTADO: todas as verificacoes passaram. Dados prontos para modelar.')

    return []


def auditar_instancia(pasta):
    A, P, R = ler_instancia(pasta)
    return auditar_dados(A, P, R, status=ler_status_validacao(pasta), rotulo=str(pasta))


def main():
    from codigo.configuracao import PASTA_DADOS
    pasta = sys.argv[1] if len(sys.argv) > 1 else PASTA_DADOS
    try:
        return 1 if auditar_instancia(pasta) else 0
    except (ValueError, KeyError, OSError) as erro:
        print("ERRO NA AUDITORIA:", erro, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
