# Otimização do cronograma de projeto de empreendimentos de grande porte

Trabalho computacional de **Pesquisa Operacional (ELE082)** — UFMG, 2026/2.

---

## O problema, em um parágrafo

Projetar um edifício envolve mais de vinte equipes independentes — arquitetura,
estrutura, hidráulica, elétrica, climatização, incêndio e por aí vai — que dependem
umas das outras numa ordem rígida: ninguém consegue desenhar antes de receber a
informação que outra equipe produz. Hoje a ordem em que tudo isso acontece é decidida
na mão, por uma pessoa arrastando barras numa tela. Com algumas centenas de tarefas e
cerca de mil dependências, não há como essa pessoa garantir que a ordem escolhida é a
melhor. **Este trabalho modela esse processo como um problema de sequenciamento com
precedências e recursos limitados, e mostra com número quanto se ganha ao otimizar.**

O modelo é genérico: recebe a lista de tarefas, quem depende de quem e o tamanho das
equipes. Serve para qualquer empreendimento com essa estrutura.

---

## Por onde começar

Se você acabou de chegar no projeto, nesta ordem:

1. **`docs/01-a-ideia.pdf`** (2 páginas, sem termo técnico) — o que é projetar um
   prédio, por que as equipes travam umas nas outras e o que vamos otimizar.
2. **`docs/02-plano-de-modelagem.pdf`** (10 páginas) — o documento principal. O processo
   real em detalhe, a tradução para o modelo bloco a bloco, o código e a divisão de
   tarefas. As Partes I e II são para todo mundo.
3. **`dados/LEIA-ME.md`** — o que tem em cada coluna de cada arquivo.
4. Rode o modelo mínimo (instruções abaixo) e veja saindo um resultado.

`docs/03-modelagem-completa.pdf` é a formulação matemática inteira, com todas as
extensões. Consulte conforme precisar — não precisa ler de cabo a rabo agora.

---

## Rodando em três comandos

```bash
python3 -m pip install -r codigo/requirements.txt

python3 codigo/verificar.py dados/instancia_media        # audita os dados
python3 codigo/modelo_minimo.py dados/instancia_media    # resolve
```

Saída esperada:

```
atividades: 28 | precedencias: 98 | horizonte: 138 dias
prazo do cronograma praticado (referencia): 138 dias
status  : Optimal
makespan: 109 dias uteis
praticado: 138 dias uteis  ->  ganho de 29 dias (21.0%)
VERIFICACAO: solucao respeita todas as precedencias e capacidades.
```

Esses 29 dias são o trabalho inteiro em miniatura: o cronograma que uma pessoa montou
leva 138 dias, a solução ótima com exatamente as mesmas restrições leva 109.

---

## Estrutura

```
dados/
  LEIA-ME.md                 dicionário de dados: cada coluna de cada arquivo
  relatorio_qualidade.txt    o que foi feito na preparação, com os números
  instancia_pequena/          12 atividades, montada à mão, dá para conferir no papel
  instancia_media/            28 atividades, um bloco real, roda em segundos
  instancia_completa/        242 atividades, 994 vínculos, para os resultados finais

codigo/
  dados.py                    leitura dos CSVs e convenções comuns
  verificar.py               13 checagens nos dados. Rode antes de modelar
  modelo_minimo.py           modelo base + verificação automática da solução
  gerar_recorte.py           cria recortes menores da instância completa
  requirements.txt

docs/
  01-a-ideia.pdf             a proposta, sem jargão
  02-plano-de-modelagem.pdf  o documento de trabalho do grupo
  03-modelagem-completa.pdf  formulação matemática completa

template-latex/              template do relatório final
```

---

## O modelo, em quatro restrições

O `modelo_minimo.py` implementa só o núcleo. A variável de decisão é
`x[a][t] = 1 se a atividade a começa no dia t`, e daí saem o início e o término:

| # | Restrição | Em português |
|---|---|---|
| 1 | `soma_t x[a][t] = 1` | cada atividade começa em exatamente um dia |
| 2 | `inicio[b] >= fim[a] + lag` | B não começa antes de A terminar (e as 3 variações) |
| 3 | `soma das ativas no dia t <= R[k]` | nenhuma equipe faz mais do que consegue |
| 4 | `Cmax >= fim[a]`, minimizar `Cmax` | o projeto acaba com a última atividade |

O que ainda não entrou, em ordem de prioridade: ciclo de revisão com número de revisões
como decisão, ordem dos blocos construtivos como decisão, trâmites em órgão público como
categoria própria, reprogramação a partir do estado atual. O plano de modelagem detalha
cada um e a ordem de implementação.

---

## O resultado que o trabalho persegue

A ordem em que os blocos construtivos são projetados, no cronograma real, é uma fila:
a mesma equipe faz um bloco, depois o outro, depois o outro. **Isso não é obrigação
técnica** — um bloco não precisa do outro para ser projetado. É escolha de quem montou
o cronograma.

O experimento central é rodar duas vezes: com a ordem travada como está no cronograma, e
com a ordem livre. A diferença de prazo é o ganho atribuível só à decisão de
sequenciamento, e responde sozinha à pergunta "para que serve otimizar isso?".

---

## Sobre os dados

Vêm de um cronograma real, e estão **anonimizados**: sem nome de empreendimento,
construtora, incorporadora, escritório projetista ou pessoa; sem datas de calendário,
endereços ou contatos. Restaram duração, dependência, disciplina e papel.

Um detalhe metodológico que importa: a capacidade de cada equipe foi derivada do pico de
atividades simultâneas observado no próprio cronograma. Isso garante que **o cronograma
praticado é sempre uma solução viável do modelo** — então o ótimo nunca pode sair pior
que ele. Se sair, é bug.

---

## Ferramentas

`PuLP` com o solver CBC, que é livre e já funciona. O Gurobi é bem mais rápido e tem
licença acadêmica gratuita com e-mail `@ufmg.br` — vale migrar quando a instância
completa entrar.
