# -*- coding: utf-8 -*-
"""
Auditoria dos dados de uma instância.

Roda antes de modelar. Se algum item vier com FALHA, o modelo vai dar problema
(infactível, prazo absurdo ou resultado sem sentido) e a causa está aqui.

Uso:  python codigo/verificar.py dados/instancia_media
"""
import csv, sys, os
from collections import Counter, defaultdict

pasta = sys.argv[1] if len(sys.argv) > 1 else 'dados/instancia_media'
ler = lambda n: list(csv.DictReader(open(os.path.join(pasta, n), encoding='utf-8'),
                                    delimiter=';'))
A, P, R = ler('atividades.csv'), ler('precedencias.csv'), ler('recursos.csv')
at = [a for a in A if a.get('nivel', 'ATIVIDADE') == 'ATIVIDADE']
ids = {a['id'] for a in at}
dur = {a['id']: int(a['duracao_dias']) for a in at}
pap = {a['id']: [p for p in a['papel'].split(';') if p] for a in at}
col = 'capacidade' if 'capacidade' in R[0] else 'capacidade_sugerida'
cap = {r['papel']: int(r[col]) for r in R}
tem_praticado = 'inicio_praticado' in at[0]

falhas = []
def chk(nome, condicao, detalhe=''):
    ok = 'ok  ' if condicao else 'FALHA'
    if not condicao: falhas.append(nome)
    print('  [%s] %-46s %s' % (ok, nome, detalhe))

print('\nAUDITORIA -', pasta)
print('=' * 72)
print('atividades: %d | precedencias: %d | papeis: %d' % (len(at), len(P), len(R)))
print()
print('INTEGRIDADE')
chk('todo id e unico', len(ids) == len(at))
chk('nenhum nome duplicado',
    all(c == 1 for c in Counter(a['nome'] for a in at).values()))
chk('toda duracao e positiva', all(d > 0 for d in dur.values()))
chk('toda atividade tem papel', all(pap[i] for i in ids))
chk('todo papel esta em recursos.csv',
    all(p in cap for l in pap.values() for p in l))
chk('precedencias so citam ids existentes',
    all(p['predecessora'] in ids and p['sucessora'] in ids for p in P))
chk('sem auto-referencia', all(p['predecessora'] != p['sucessora'] for p in P))
chk('sem precedencia duplicada',
    len(P) == len({(p['predecessora'], p['sucessora'], p['tipo_vinculo']) for p in P}))
chk('tipos de vinculo validos',
    all(p['tipo_vinculo'] in ('TI', 'II', 'TT', 'IT') for p in P))

# --- grafo aciclico (obrigatorio: com ciclo o modelo e infactivel)
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

if tem_praticado:
    ini = {a['id']: int(a['inicio_praticado']) for a in at}
    fim = {a['id']: int(a['fim_praticado']) for a in at}
    print()
    print('COERENCIA COM O CRONOGRAMA PRATICADO')
    chk('termino = inicio + duracao - 1',
        all(fim[i] == ini[i] + dur[i] - 1 for i in ids))

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
        usa = [i for i in ids if r in pap[i]]
        pico = max((sum(1 for i in usa if ini[i] <= t <= fim[i])
                    for t in range(lim + 1)), default=0)
        if pico > cap[r]: estouro.append((r, pico, cap[r]))
    chk('praticado cabe na capacidade declarada', not estouro,
        '; '.join('%s pico %d > cap %d' % e for e in estouro[:3]))
    print('  [nota ] %-46s %d dias uteis' % ('prazo do cronograma praticado', lim + 1))

print()
print('=' * 72)
if falhas:
    print('RESULTADO: %d verificacao(oes) falharam -> %s' % (len(falhas), ', '.join(falhas)))
    sys.exit(1)
print('RESULTADO: todas as verificacoes passaram. Dados prontos para modelar.')
