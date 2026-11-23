# Otimização do cronograma de projeto de empreendimentos de grande porte

Trabalho computacional de **Pesquisa Operacional (ELE082)** — UFMG, 2026/2.

**Situação dos dados em 22/11/2026:** usamos o R14 com os ajustes de projeto aprovados: três atividades incluídas, equipes corrigidas e execução de obra retirada. A completa tem 243 atividades, 1008 vínculos, 39 recursos e referência normalizada de 310 dias. A auditoria de entrada passou; a otimização da base completa ainda não foi executada nesta revisão conjunta. A mudança de 492 para 310 dias é de escopo, não ganho do solver. Consulte `dados/ajustes-projeto/registro.json`.

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
4. Edite `codigo/configuracao.py` e execute `python codigo/main.py`, após instalar a dependência.

`docs/03-modelagem-completa.pdf` é a formulação matemática inteira, com todas as
extensões. Consulte conforme precisar — não precisa ler de cabo a rabo agora.

---

## Executando o modelo

Edite `codigo/configuracao.py` para escolher a instância, o horizonte, o limite de tempo e os logs. Os caminhos são calculados a partir da pasta do projeto. A configuração padrão usa a instância completa, conforme a orientação de executar o conjunto inteiro. A auditoria roda automaticamente e impede montar o modelo se encontrar dados inválidos. A base atual passou nessa auditoria.

```bash
python -m pip install -r codigo/requirements.txt
python codigo/main.py
```

Use Python 3.10 ou superior e o ambiente virtual do projeto. O PuLP está fixado em 3.3.0; a versão 4 não usa a mesma interface. Em 22/11, a versão compatível foi instalada em `.venv/Scripts/python.exe` e o CBC foi verificado com testes sintéticos. O Python global MSYS é outro interpretador e não deve ser confundido com esse ambiente.

No PowerShell, também é possível executar diretamente:

```powershell
.\.venv\Scripts\python.exe codigo/main.py
```

A auditoria de entrada usa somente a biblioteca padrão. A entrada antiga e o gerador de recortes foram removidos.

O código está separado em leitura (`dados.py`), variáveis (`variaveis.py`), restrições (`restricoes.py`), resolução (`resolucao.py`) e validação (`validacao.py`). O prazo conta o último dia de entrega mais um, inclusive para eventos de duração zero (suporte mantido no código, sem uso na base R14 atual). O horizonte foi definido como 310 dias (índices 0 a 309), justificado pelo cronograma de referência viável. `HORIZONTE=None` usa a referência validada; sem referência e sem valor informado, o programa interrompe a execução, sem estimar o horizonte pela soma das durações.

## Como os resultados são aceitos

O programa só apresenta prazo e ganho depois de conferir valores binários, um início por atividade, todas as atividades esperadas, domínios, vínculos e capacidades. O prazo é calculado pelas entregas e guardado separadamente do objetivo bruto do solver.

A saída distingue ótimo comprovado, viável sem prova de ótimo, ausência de solução, inviabilidade com evidência, candidata rejeitada e erro. Código de saída zero significa candidata aceita; um significa ausência de resultado aceito; dois significa erro de execução ou configuração. A prova de ótimo exige dados consistentes, status da solução e evidência no log; o status isolado não basta.

Logs e JSON são guardados em `resultados/`, configurável em `codigo/configuracao.py`. O JSON inclui todos os inícios aceitos, versões, tempo, parâmetros, classificação e limites disponíveis. `MOSTRAR_LOG_SOLVER` controla a exibição, não a preservação do log. O gap do estudo é `(prazo-limite_inferior)/max(1,abs(prazo))`, limitado inferiormente a zero; sem limite confiável, permanece indisponível.

Para conferir o programa sem otimizar a base real:

```powershell
.\.venv\Scripts\python.exe -m unittest codigo.testes.test_resultados -v
```

Os 27 testes passaram. Quatro casos exercitam o CBC em modelos sintéticos pequenos; as situações de parada com e sem candidata são simuladas de forma determinística. A referência real de 310 dias também passou no novo validador sem otimização. No Windows, o adaptador usa o nome curto da mesma pasta temporária quando o caminho contém espaços; se esse nome não estiver disponível, informa um erro.

Saída registrada da versão anterior, ainda não validada para os dados corrigidos:

```
atividades: 28 | precedencias: 98 | horizonte: 138 dias
prazo do cronograma praticado (referencia): 138 dias
status  : Optimal
makespan: 109 dias uteis
praticado: 138 dias uteis  ->  ganho de 29 dias (21.0%)
VERIFICACAO: solucao respeita todas as precedencias e capacidades.
```

Esses valores pertencem à preparação anterior. Não representam resultados da base de projeto atual; os novos experimentos ainda precisam ser executados e conferidos.

---

## Estrutura

```
dados/
  LEIA-ME.md                 dicionário de dados: cada coluna de cada arquivo
  relatorio_qualidade.txt    o que foi feito na preparação, com os números
  instancia_pequena/          12 atividades, montada à mão, dá para conferir no papel
  instancia_media/            28 atividades, um bloco real, roda em segundos
  instancia_completa/        243 atividades, 1008 vínculos, referência de 310 dias

codigo/
  dados.py                    leitura dos CSVs e convenções comuns
  main.py                   entrada principal
  configuracao.py           instância e parâmetros editáveis
  verificar.py              auditoria automática dos dados antes do modelo
  variaveis.py              variáveis e expressões de tempo
  restricoes.py             dependências, capacidade, início único e objetivo
  resolucao.py              chamada do solver e apresentação após validar
  resultados.py             extração, classificação e resultado estruturado
  validacao.py              conferência da solução após resolver
  testes/                   casos de erro e integração sintética com CBC
  requirements.txt

docs/
  01-a-ideia.pdf             a proposta, sem jargão
  02-plano-de-modelagem.pdf  o documento de trabalho do grupo
  03-modelagem-completa.pdf  formulação matemática completa

relatorio/                  projeto LaTeX modular do artigo final
  main.tex                  documento principal: ordem das seções
  config/                   pacotes, comandos e metadados do artigo
  secoes/                   conteúdo dividido em arquivos por seção
  bibliografia/             referências bibliográficas
  imagens/                  figuras e logos
  build/                    PDF e arquivos gerados na compilação

slides/                     apresentação original
slides-finais/              cópia independente para a apresentação final
```

Para editar e compilar o relatório, consulte `relatorio/README.md`.
Os slides finais começam como uma cópia da apresentação original; edite
`slides-finais/main.tex` para preparar a entrega final.

---

## O modelo, em quatro restrições

O módulo `restricoes.py` implementa o núcleo. A variável de decisão é
`x[a][t] = 1 se a atividade a começa no dia t`, e daí saem o início e o término:

| # | Restrição | Em português |
|---|---|---|
| 1 | `soma_t x[a][t] = 1` | cada atividade começa em exatamente um dia |
| 2 | `inicio[b] >= fim[a] + lag` | B não começa antes de A terminar (e as 3 variações) |
| 3 | `soma das ativas no dia t <= R[k]` | nenhuma equipe faz mais do que consegue |
| 4 | `Cmax >= fim[a] + 1`, minimizar `Cmax` | conta todos os dias até a última entrega, começando do zero |

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
