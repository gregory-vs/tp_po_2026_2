# -*- coding: utf-8 -*-
"""Gera um recorte menor da instancia completa, para testes rapidos.
Uso: python3 codigo/gerar_recorte.py ZONA-1,ZONA-2 dados/instancia_media
"""
import csv
import os
import sys

from dados import ler_instancia

zonas = set(sys.argv[1].split(',')) if len(sys.argv) > 1 else {'ZONA-1'}
dest  = sys.argv[2] if len(sys.argv) > 2 else 'dados/instancia_media'
orig  = sys.argv[3] if len(sys.argv) > 3 else 'dados/instancia_completa'

A, P, R = ler_instancia(orig)

sel = [a for a in A if a['nivel'] == 'ATIVIDADE' and a['zona'] in zonas]
if not sel:
    print('nenhuma atividade encontrada para as zonas: %s' % ','.join(sorted(zonas)),
          file=sys.stderr)
    sys.exit(1)

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
