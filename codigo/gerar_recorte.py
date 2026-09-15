# -*- coding: utf-8 -*-
"""Gera um recorte menor da instância completa, para testes rápidos.
Uso: python codigo/gerar_recorte.py ZONA-1,ZONA-2 dados/instancia_media
"""
import csv, sys, os
zonas = set(sys.argv[1].split(',')) if len(sys.argv) > 1 else {'ZONA-1'}
dest  = sys.argv[2] if len(sys.argv) > 2 else 'dados/instancia_media'
orig  = sys.argv[3] if len(sys.argv) > 3 else 'dados/instancia_completa'

def ler(n): return list(csv.DictReader(open(os.path.join(orig, n), encoding='utf-8'), delimiter=';'))
A, P, R = ler('atividades.csv'), ler('precedencias.csv'), ler('recursos.csv')

sel = [a for a in A if a['nivel'] == 'ATIVIDADE' and a['zona'] in zonas]
ids = {a['id'] for a in sel}
pre = [p for p in P if p['predecessora'] in ids and p['sucessora'] in ids]
pap = {x for a in sel for x in a['papel'].split(';') if x}
rec = [r for r in R if r['papel'] in pap]

# rebaseia o tempo para o recorte comecar no dia 0
base = min(int(a['inicio_praticado']) for a in sel)
for a in sel:
    a['inicio_praticado'] = int(a['inicio_praticado']) - base
    a['fim_praticado']    = int(a['fim_praticado']) - base

os.makedirs(dest, exist_ok=True)
for nome, dados in [('atividades.csv', sel), ('precedencias.csv', pre), ('recursos.csv', rec)]:
    with open(os.path.join(dest, nome), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(dados[0].keys()), delimiter=';')
        w.writeheader(); w.writerows(dados)
print('%s: %d atividades, %d precedencias, %d papeis | prazo praticado: %d dias'
      % (dest, len(sel), len(pre), len(rec), max(a['fim_praticado'] for a in sel) + 1))
