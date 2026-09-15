# Base de dados — cronograma de projeto multidisciplinar

Instâncias de teste extraídas de um cronograma real de projeto de um empreendimento
vertical de grande porte, **anonimizadas**.

Nada aqui identifica o empreendimento, a construtora, a incorporadora, os escritórios
projetistas ou qualquer pessoa. Não há datas de calendário, nomes de produto, endereços
nem contatos. Sobrou só o que o modelo precisa: duração, dependência e quem executa.

---

## As três instâncias

| Pasta | Ativid. | Vínculos | Prazo praticado | Para que serve |
|---|---:|---:|---:|---|
| `instancia_pequena` | 12 | 24 | — | montada à mão. Começar por aqui, dá pra conferir no papel |
| `instancia_media` | 28 | 98 | 138 dias | um bloco construtivo real. Roda em segundos no CBC |
| `instancia_completa` | 242 | 994 | 492 dias | tudo. Para os resultados finais e teste de escalabilidade |

Cada pasta tem `atividades.csv`, `precedencias.csv` e `recursos.csv` — CSV com
separador `;`, codificação UTF-8.

---

## atividades.csv

| Coluna | O que é |
|---|---|
| `id` | identificador (`T001`, `A01`…) |
| `nome` | rótulo montado a partir dos outros campos. Único em toda a instância |
| `nivel` | `ATIVIDADE` = trabalho real. `AGRUPADOR` = linha que só soma outras no cronograma original. **Use apenas `ATIVIDADE`** (a coluna não existe na pequena e na média, que já vêm filtradas) |
| `tipo` | o que a atividade é — ver tabela abaixo |
| `entregavel` | id da cadeia de revisões a que ela pertence (`E001`…). Junta o R00, a análise, o R01 etc. do mesmo pacote |
| `disciplina` | sigla da especialidade. `GERAL` quando a atividade não é de uma disciplina específica |
| `fase` | `EP`, `AP`, `PL`, `EX` ou `GERAL` |
| `revisao` | `R00`, `R01`, `R02`, `R03`. Vazio quando não se aplica |
| `zona` | `ZONA-1` a `ZONA-4` (blocos construtivos). Vazio = atividade do empreendimento todo |
| `papel` | quem executa. Vários papéis vêm separados por `;` |
| `duracao_dias` | duração em **dias úteis** |
| `inicio_praticado` / `fim_praticado` | o que o cronograma real fez, em dias úteis contados do início do projeto. **É referência de comparação, não restrição** |
| `pct_concluido` | percentual executado na data de status do cronograma |
| `estado` | `CONCLUIDA`, `EM_ANDAMENTO` ou `NAO_INICIADA` |

### Valores de `tipo`

| Valor | Significado | Comportamento esperado no modelo |
|---|---|---|
| `EMISSAO` | um projetista produz e entrega uma revisão | consome a equipe da disciplina |
| `ANALISE` | a equipe do contratante revisa e devolve comentários | consome a equipe de análise — o gargalo |
| `COMPATIBILIZACAO` | junta os modelos e procura conflitos entre disciplinas | recurso de coordenação, capacidade baixa |
| `TRAMITE-EXTERNO` | espera por órgão público | **não consome recurso nosso e não comprime** |
| `GATE` | reunião ou marco de validação | decisor, capacidade 1 |
| `CONSULTORIA` | parecer de consultor externo | recurso dedicado |
| `RETRABALHO` | ajuste após comentário, envolvendo várias disciplinas | multi-disciplina |

### Siglas de disciplina

`ARQ` arquitetura · `ARI` interiores · `EST` estrutura · `HID` hidráulica ·
`ELE` elétrica · `CLI` climatização · `PCI` combate a incêndio · `PRE` pressurização ·
`GAS` gás · `AUT` automação · `FUN` fundação · `PSG` paisagismo · `LUM` luminotécnico ·
`ACU` acústica · `CXO` caixilhos · `VED` vedações · `IMP` impermeabilização ·
`COM` comunicação visual · `SMOP` drenagem urbana · `CLASH` compatibilização ·
`CTV` / `NBR` / `INS` consultorias · `GERAL` sem disciplina específica

---

## precedencias.csv

| Coluna | O que é |
|---|---|
| `predecessora` | id da atividade que vem antes |
| `sucessora` | id da atividade que vem depois |
| `tipo_vinculo` | `TI`, `II`, `TT` ou `IT` |
| `lag_dias` | folga obrigatória entre as duas |

### Os quatro tipos de vínculo

| Sigla | Nome | Restrição correspondente |
|---|---|---|
| `TI` | término–início | `inicio[b] >= fim[a] + lag` |
| `II` | início–início | `inicio[b] >= inicio[a] + lag` |
| `TT` | término–término | `fim[b] >= fim[a] + lag` |
| `IT` | início–término | `fim[b] >= inicio[a] + lag` |

`TI` é a grande maioria. Os outros três são poucos mas mudam o resultado: tratar tudo
como `TI` serializa o cronograma artificialmente e infla o prazo.

---

## recursos.csv

| Coluna | O que é |
|---|---|
| `papel` | identificador, igual ao usado em `atividades.papel` |
| `categoria` | `PROJETISTA`, `ANALISTA`, `CONSULTOR`, `ORGAO_PUBLICO`, `DECISOR`, `COLETIVO` |
| `n_atividades` | em quantas atividades esse papel aparece |
| `capacidade_observada` | maior número de atividades desse papel rodando ao mesmo tempo **no cronograma praticado** |
| `capacidade_sugerida` | o que usar como $R_k$ no modelo. Vem da capacidade observada |

**De onde vem a capacidade.** O cronograma não diz quantas pessoas cada escritório tem.
Mas diz quantas atividades daquele papel rodaram simultaneamente — e esse pico é, por
definição, a menor capacidade que torna o cronograma praticado viável. Usar esse número
tem uma consequência importante: **o cronograma praticado é sempre uma solução viável do
modelo**, então o ótimo encontrado nunca pode ser pior que ele. Se der pior, tem bug.

Essa é uma estimativa por baixo (a equipe pode ter folga que o cronograma não usou), e
por isso mesmo é um bom parâmetro para análise de sensibilidade: aumente a capacidade do
papel mais carregado em uma unidade e veja quanto o prazo cai.

---

## Como usar

```bash
pip install pulp

python verificar.py instancia_media       # audita os dados antes de modelar
python modelo_minimo.py instancia_media   # resolve e confere a solução
```

O `verificar.py` roda 13 checagens (integridade, ciclos, coerência com o praticado).
Se alguma falhar, o modelo vai dar problema e a causa está ali.

O `modelo_minimo.py` resolve com precedência + capacidade + prazo mínimo, e no fim
**confere a própria solução** contra todas as precedências e capacidades.

Para gerar um recorte diferente:

```bash
python gerar_recorte.py ZONA-1,ZONA-2 minha_instancia
```

---

## Cinco coisas que vão poupar tempo

1. **Filtre `nivel = ATIVIDADE`** na instância completa. As linhas `AGRUPADOR` são
   barras-mãe do cronograma; incluí-las conta o mesmo trabalho duas vezes.
2. **Use `fim_praticado` como horizonte.** O prazo praticado já é uma solução viável,
   então serve de teto. Usar a soma das durações como horizonte multiplica o número de
   variáveis por cinco e trava o solver.
3. **As datas são em dias úteis**, contadas do início do projeto. Não há calendário e
   `fim = inicio + duracao - 1` vale sempre.
4. **O praticado não é o ótimo.** Ele é o que uma pessoa montou arrastando barras.
   É a referência de comparação, e o resultado principal do trabalho é a diferença.
5. **Há dependência circular no mundo real** (estrutura ↔ instalações, arquitetura ↔
   shafts). Nos dados ela aparece já resolvida como duas revisões da mesma disciplina.
   Não tente "consertar" isso: é assim que funciona.

---

## Limitações conhecidas

| Item | Situação |
|---|---|
| 4 atividades sem nenhum vínculo na instância completa | são marcos soltos no cronograma original. Ficam livres no modelo, não atrapalham |
| 37 vínculos descartados na preparação | o próprio cronograma não os respeitava, o que indica erro de extração. Mantê-los impediria o modelo de reproduzir o praticado |
| 22 arcos que fechavam ciclo, removidos | rede de precedência precisa ser acíclica |
| Disciplina/fase `GERAL` | atividades administrativas e marcos que não pertencem a uma disciplina |
| Capacidade estimada por baixo | ver a seção de recursos acima |

Tudo isso está registrado em `relatorio_qualidade.txt`, com os números de cada etapa
da preparação.
