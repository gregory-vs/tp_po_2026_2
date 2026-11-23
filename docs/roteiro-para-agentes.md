# Contexto e continuidade para os agentes dos colegas

Data de referência: 23/11/2026. Este arquivo acompanha `docs/roteiro-para-concluir-a-entrega.md`, destinado à leitura humana. As duas versões devem manter os mesmos fatos e pendências. Mostrar a versão humana por padrão.

## 1. Mandato e limites de atuação

Thales encerrou sua participação nesta condução e deixou a conclusão para os colegas. Este documento transmite contexto; não é autorização genérica para executar experimentos, mudar escopo ou escrever o artigo inteiro. Confirmar a tarefa atual com o colega responsável e seguir suas instruções. Não iniciar novas buscas do solver só por ler este arquivo.

Preferências estabelecidas:

- Trabalho colaborativo, etapa por etapa. A redação foi planejada em conjunto pelo chat, antes de transferir o texto aprovado para o LaTeX. Não preencher automaticamente o artigo sem pedido do responsável.
- Todo Python executável do projeto fica em `codigo/`.
- Não fazer commit, push, publicação ou envio de mensagens sem autorização correspondente.
- Preservar dados e resultados existentes. Examinar o estado do repositório antes de editar; há alterações locais e arquivos não rastreados.
- Não publicar PDFs originais do contratante nem mapas entre IDs originais e anônimos. Esses materiais ficam fora do repositório público. Não reconstruir ou copiar mapas para o repo.
- Ler `docs/AGENTS.md`. Manter os dois planos coerentes ao revisá-los. Atualizar `docs/decisoes-do-trabalho.md` somente quando houver decisão efetiva, explicando o motivo e preservando o histórico. Não abrir a versão técnica por padrão.

## 2. Objetivo e entrega

Artigo em formato de paper e apresentação de 12 minutos em 25/11/2026. O professor não solicitou ajustes na proposta apresentada.

Pergunta atual: quanto é possível reduzir o prazo do processo de projeto de arquitetura e engenharia reorganizando os inícios, mantendo atividades, durações, papéis e vínculos da base preparada, sob capacidades fixas?

O estudo replaneja desde o início, inclusive tarefas já executadas na realidade. Não modela execução de obra, esforço em horas, decisões de contratação ou algoritmos híbridos novos. Referências com outros algoritmos podem apoiar a revisão sem que precisemos reproduzi-los. A liberação de vínculos administrativos permanece extensão a discutir, não cenário aprovado.

## 3. Estado da base e hipóteses

Base ativa: `dados/instancia_completa/`. Fonte: R14, não R15. Estado atual: 243 atividades, 47 agrupadores e 39 recursos; 1.008 precedências, sendo 1.003 TI, 2 II, 2 TT e 1 IT. Agrupadores não entram como atividades do modelo. Durações atuais são todas positivas; código também suporta eventos de duração zero.

Referência validada: 310 dias úteis normalizados, última entrega no índice 309. O prazo anterior de 492 dias incluía outro recorte, com obra. **492→310 não é ganho da otimização.**

Tratamentos e limitações que o artigo precisa explicitar:

- Durações declaradas do R14 preservadas. Intervalo entre início e entrega já inclui pausas; não é esforço.
- Calendário abstrato comum de dias úteis, sem reconstrução de feriados e recessos ou equivalência exata com datas civis.
- Capacidade de cada papel estimada pelo pico simultâneo da referência preparada; não é capacidade máxima operacional comprovada.
- Na preparação original, 22 arcos foram removidos por ciclo e 37 por incoerência com o praticado. Não há lista individual preservada. Os 79 ajustes originais foram em datas, não em durações. Houve imputações de papéis, fases e disciplinas sem marca individual completa.
- Cobertura incompleta de tarefas ocultas em agrupadores do PDF. Não alegar representação integral do empreendimento.
- Ajustes posteriores aprovados: três atividades incluídas, 15 atribuições de equipe corrigidas, retirada de duas atividades de obra e seus seis agrupadores, recálculo das capacidades e do prazo. Cinco papéis adicionais anonimizados.
- Atividades com múltiplos papéis consomem todas as equipes indicadas simultaneamente.

Rastreabilidade: `dados/LEIA-ME.md`, `dados/conferencia-r14.json`, `dados/ajustes-projeto/registro.json`, `dados/instancia_completa/validacao.json` e `docs/conferencia-cronograma-original.md`. Instâncias menores foram preservadas; não assumir que receberam os mesmos ajustes da completa.

## 4. Formulação implementada

Notação completa em `docs/formulacao-matematica.md`. Para atividade a com duração d[a], horizonte H:

```text
x[a,t] binária: início em t
domínio t=0..H-d[a] se d[a]>0; t=0..H-1 se d[a]=0
sum_t x[a,t] = 1
S[a] = sum_t t*x[a,t]
F[a] = S[a] + max(d[a],1) - 1       # entrega inclusiva
C[a] = S[a] + d[a]                 # término exclusivo da ocupação
min Cmax, com Cmax >= F[a]+1 para todo a

TI: S[j] >= F[i] + lag
II: S[j] >= S[i] + lag
TT: F[j] >= F[i] + lag
IT: F[j] >= S[i] + lag

Capacidade: para cada papel k e dia t,
quantidade de atividades com d>0, k entre seus papéis e S[a]<=t<C[a]
não pode superar cap[k].
```

TI com lag zero permite liberação no dia da entrega, mas ambas as atividades ocupam capacidade nesse dia se compartilharem equipe. Eventos de duração zero não ocupam equipes, mas sua entrega conta no prazo. S/F/C são expressões derivadas, não variáveis adicionais. Cmax é contínua não negativa.

H=310 é teto justificado por referência viável, não duração obrigatória. Essa justificativa precisa ser reavaliada se mudarem durações, vínculos ou reduzirem capacidades. Modelo atual: 72.381 binárias + Cmax; 13.584 restrições; 1.696.037 coeficientes não nulos no MPS da rodada completa.

## 5. Código e execução

Fluxo: `codigo/main.py` → configuração → `resolucao.py` → carregamento/auditoria → variáveis/restrições → warm start opcional → CBC → extração/validação → JSON e apresentação.

| Módulo | Responsabilidade |
| --- | --- |
| `dados.py` / `verificar.py` | Leitura e auditoria dos mesmos registros, com rejeição de inconsistências |
| `variaveis.py` / `restricoes.py` | Domínios, expressões e quatro famílias de restrições |
| `warm_start.py` | Validar referência, inicializar todos x e Cmax e interpretar aceite do CBC |
| `resolucao.py` | Chamada do solver, temporários, logs, tempo e persistência |
| `resultados.py` / `validacao.py` | Classificação por evidências e validação independente da candidata |

Ambiente usado: Python 3.13.5, PuLP **3.3.0** fixado em `codigo/requirements.txt`, CBC 2.10.3, Windows. Não atualizar dependências indiscriminadamente; PuLP 4 tem interface incompatível com este código. Na máquina de Thales, o Python genérico do shell pode ser outro; usar `.venv/Scripts/python.exe`. Em outra máquina, criar ambiente próprio e instalar as dependências, sem copiar `.venv`.

Comandos a partir da raiz do checkout:

```powershell
# Somente se o responsável solicitar uma nova rodada real:
.\.venv\Scripts\python.exe codigo\main.py

# Testes apropriados após alterações no código:
.\.venv\Scripts\python.exe -m unittest codigo.testes.test_resultados codigo.testes.test_warm_start -v
```

Configuração conferida em `codigo/configuracao.py`:

```python
INSTANCIA = "instancia_completa"
HORIZONTE = 310
TEMPO_LIMITE_SEGUNDOS = 1800
USAR_WARM_START = True
MOSTRAR_LOG_SOLVER = False
TOLERANCIA_NUMERICA = 1e-6
```

Warm start: exige referência completa e validada; confere horizonte, precedências e capacidades; inicializa todos os valores via `setInitialValue`, **sem fixar os inícios**. Registrar leitura e aceite separadamente. Evidência de aceite: `MIPStart provided solution with cost ...`. O adaptador usa pasta temporária exclusiva com caminhos relativos sem espaços e `keepFiles=True`, limpando-a ao final, pois CBC 2.10.3/Windows prefixou `.\` ao caminho absoluto do arquivo inicial em teste. Não remover essa adaptação sem testar no Windows.

Logs são gravados durante a chamada e apresentados no terminal depois, conforme configuração. O limite do CBC não funciona como encerramento rígido: já houve ultrapassagens dentro do executável. PuLP espera o processo encerrar. Uma nova chamada não retoma automaticamente a árvore anterior.

Resultado só é aceito após conferir binariedade, unicidade, cobertura dos IDs, domínios, expressões derivadas, precedências, capacidade e consistência do prazo. Não usar somente `m.status == Optimal`: PuLP pode dar esse status com incumbente de parada por tempo. Prova exige também situação da solução e mensagem final apropriada do CBC. Códigos de saída: 0 candidata aceita, 1 resultado não aceito/sem candidata/inviável, 2 erro de execução.

## 6. Evidências e resultados verificados

Os 32 testes passaram após a implementação do warm start. A validação manual A/B/C foi resolvida em conjunto e executada por Thales: B0–1, A2–4, C4–5; ótimo de 6 dias, gap zero. Evidências: `dados/validacao_manual/LEIA-ME.md` e `resultados/20261123T031257183085Z-b0cc1c21.{json,log}`. Esses seis dias são um caso didático, não resultado da base real.

Primeira rodada completa: `resultados/20261123T032556146188Z-248df388.{json,log}`. Sem warm start, timeLimit120; tempo da aplicação534,459s; nenhuma candidata inteira, LB187 no log, zero nós principais. Não prova inviabilidade. O JSON não preservou LB por retorno antecipado; pendência conhecida.

**Rodada principal para o artigo:** `resultados/20261123T034835057589Z-8a258fda.json` e `.log`. Ambos foram conferidos, não apenas os prints.

| Campo | Valor |
| --- | --- |
| Classificação / parada | `viavel_sem_prova` / `limite_tempo` |
| Referência / H | 310 / 310 |
| Melhor prazo / objetivo bruto | 307 / 307.0 |
| Ganho | 3 dias; 3/310 ≈ 0,96774194% |
| LB / gap do estudo | 187 / (307−187)/307 ≈ 39,08794788% |
| Tempo solicitado / aplicação / CBC | 1800 / 2183,9042313 / 2180,41 segundos |
| Warm start | 72.382 valores lidos, aceito com custo310 |
| Incumbentes | 310 aos11,51s; 308 aos815,25s; 307 aos924,12s, no relógio do CBC |
| Nós / iterações | 823 / 634.163 |
| Validação / erros / avisos | aprovada / nenhum / nenhum |

Interpretação: 187 ≤ z* ≤ 307. Não afirmar que o ótimo é307 nem que o ganho máximo é1%. O gap não mede ganho sobre a referência. O CBC mostra `Gap: 0.64` por outra convenção: 120/187≈64,17%; padronizar no artigo a fórmula do estudo registrada no JSON. A comparação entre as rodadas não isola efeito do warm start, pois o tempo solicitado também mudou.

## 7. Trabalho pendente, por prioridade

1. **Análise da rodada existente:** juntar atividades reais do CSV aos inícios do JSON por ID; calcular diferenças de S e F; identificar antecipações/adiamentos e entregas finais; escolher exemplos explicativos e preparar tabela/figura legível. Não inferir caminho crítico ou gargalo só pela última entrega.
2. **Decisão sobre novas buscas:** grupo escolhe se vale ampliar tempo ou testar capacidades. Sensibilidade ainda sem equipes/cenários definidos. Preservar base e usar cópias explícitas por cenário; manter condições comparáveis. Aumento de capacidade amplia o conjunto viável, mas incumbente pior em busca truncada não demonstra piora do ótimo. Não executar automaticamente nem remover vínculos para obter ganho.
3. **Redação do paper:** `relatorio/` ainda tem marcadores `\preencher`; bibliografia apenas com orientações. Consultar `relatorio/README.md`, cadastrar fontes reais, ativar BibTeX, preencher metadados e escrever as sete partes exigidas: introdução, literatura crítica, problema/modelagem, algoritmo/ferramenta, resultados/análise, conclusões, referências. Resumo por último. Não inventar metadados ou resultados. Consultar PDFs locais antes de citar suas conclusões.
4. **PDF e revisão:** em `relatorio/`, `latexmk -pdf main.tex` gera `build/main.pdf`. Não tratar PDF antigo como versão atual. Conferir os cinco critérios do enunciado, todos de igual peso: escrita, pesquisa bibliográfica, análise dos resultados, conteúdo e rigor de forma.
5. **Slides:** editar `slides-finais/main.tex`, que ainda contém proposta/resultados esperados. Atualizar para resultados reais, compilar e revisar PDF; ensaiar12min, dividir falas e alinhar números com o artigo.
6. **Integração/entrega:** revisar README e descrições antigas, preservar evidências, conferir privacidade, formato/prazo/encarregado do envio. Não há responsáveis atribuídos; divisão humana sugerida é análise, redação/literatura e slides/integração, com revisão conjunta.

Não condicionar a escrita a obter um ótimo. Se o tempo apertar, priorizar análise da rodada válida, artigo completo e apresentação ensaiada.

Pendência secundária de código: preservar LB no JSON mesmo sem candidata. Manter prazo e gap da busca indisponíveis se não houver candidata; não transformar referência externa em incumbente aceita sem evidência. A rodada307 já tem LB e gap corretos. Nenhuma alteração adicional foi feita para corrigir esse caso.

## 8. Mapa de leitura e manutenção

- `docs/roteiro-para-concluir-a-entrega.md`: roteiro humano vigente.
- `docs/plano-de-acao-entrega-2.md` e `docs/plano-de-acao-entrega-2-tecnico.md`: planejamento e histórico; há trechos antigos, priorizar atualizações explícitas e evidências mais recentes.
- `docs/decisoes-do-trabalho.md`: justificativas, incluindo decisão20 de warm start.
- `docs/formulacao-matematica.md` e `docs/revisao-modelo-base.md`: equações e revisão.
- `docs/experimentos.md`: rodadas verificadas e interpretação.
- `docs/referencias-comentadas.md` e `docs/referencias/`: nove trabalhos organizados. Prioridade recomendada: Ding, Kong e Dou, Colares; demais complementam ou servem de exemplo de exposição. Seleção final ainda do grupo.

Ao receber novas instruções, verificar arquivos atuais antes de assumir que este retrato continua vigente. Distinguir sempre fatos verificados, decisões confirmadas, propostas e tarefas ainda não executadas. Não apresentar este documento técnico inteiro ao usuário quando ele pedir o roteiro humano.
