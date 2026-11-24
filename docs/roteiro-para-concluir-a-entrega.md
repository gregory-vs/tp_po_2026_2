# O que falta para terminar o trabalho

Atualizado em 23/11/2026. **A entrega do PDF no Moodle é terça-feira, 24/11, até 23:59. A apresentação de 12 minutos é na quarta, 25/11.**

## Passagem da parte do Henrique (23/11, noite): ler primeiro

A análise dos resultados está fechada e as seções 3 a 6 do artigo estão escritas. Os trechos mais abaixo que falam em "307 dias" ou "ganho de 1%" são do começo do trabalho: valem só como resultado do CBC, para comparar métodos.

### Números para usar no artigo e nos slides

| O quê | Prazo | Leitura |
| --- | ---: | --- |
| Cronograma praticado (referência) | 310 | ponto de partida |
| CBC, 36 min | 307 | parou por tempo, sem prova; mostra o limite do solver |
| **Ótimo com as liberações praticadas** | **285** | **número realista: −25 dias (8,1%), comprovado** |
| Ótimo com todas as disciplinas liberadas no início | 187 | limite da reordenação: −123 dias (39,7%), comprovado |

- **Por que 285 é o realista:** 27 atividades começaram tarde porque esperavam a arquitetura do estudo preliminar, que ficou fora da base. Isso foi conferido no R14 e confirmado pelo Henrique: as disciplinas só começam depois da arquitetura. A versão de 285 prende essas atividades nas datas em que começaram.
- **Por que os resultados são ótimos:** o cronograma encontrado pela heurística tem o mesmo prazo do limite inferior do caminho crítico. Nenhum cronograma termina antes desse limite, então não existe nada melhor.
- **O que limita o prazo:** a sequência de emissões e análises, e não o tamanho das equipes. Com uma frente a mais em todas as equipes, o prazo continua o mesmo. Na versão de 285, a cadeia é a de arquitetura e caixilhos do anteprojeto.

### O que os testes mostraram (versão de 285)

| Mudança | Efeito no prazo |
| --- | ---: |
| +1 ou −1 frente em todas as equipes | 0 |
| Emissão do projetista 10% mais rápida | −15 |
| Arquitetura 20% mais rápida | −10 |
| Zonas do AP de arquitetura emitidas em paralelo | −10 |
| Análise do cliente 50% mais rápida | −2 |
| Prazo máximo de 5 dias para a análise do cliente | 0 |

### Propostas de melhoria (subseção "Propostas de melhoria" da seção 5 do artigo)

São ideias que saem dos testes e de como o processo funciona na prática. Nenhuma foi testada no projeto real.

1. **Liberar as disciplinas mais cedo:** entregar a base de arquitetura em pacotes, por torre, para as disciplinas não esperarem a etapa inteira. É o ponto que mais pesa: toda a diferença entre 285 e 187 vem dessa espera.
2. **Reduzir o tempo de emissão só onde vira prazo:** usar templates, bibliotecas e tabelas geradas direto do modelo BIM nas emissões de arquitetura e caixilhos da cadeia crítica. Na prática, uma emissão de 7 dias já caiu para 3 com um template bom. Com uma hipótese conservadora de 10%, o ganho é de 10 dias. A mesma redução fora da cadeia não muda nada.
3. **Tratar as zonas como uma entrega única:** as zonas são separadas pelo volume de trabalho, não por dependência técnica. Emitidas em paralelo, reduzem 10 dias.
4. **Não começar contratando mais gente:** mais equipe só ajuda se for usada para encurtar a cadeia crítica.
5. **Prazo máximo para a análise do cliente só como complemento:** sozinho, rende pouco.

Duas ideias foram retiradas em 23/11, a pedido do Henrique:

- **Encurtar a análise de 22 dias da consultoria de interiores.** É uma janela de decisão do cliente, específica demais deste projeto. Aparece só como limite superior do ganho, e não como medida.
- **Compatibilizar por zona.** A espera de 31 dias antes da compatibilização era um vínculo que faltou na base, e não uma espera real. O Henrique confirmou que a compatibilização não toma esses dias. O caso ficou registrado nas limitações do artigo: com o vínculo restaurado, o limite de 187 sobe para 196, e o resultado de 285 não muda. A base não foi alterada, porque essa correção é decisão do grupo.

### O que está pronto no artigo (`relatorio/secoes/`)

- **03 Problema e modelagem:** contexto do processo, dados, notação, formulação completa e convenção de sobreposição.
- **04 Algoritmo:** procedimento, CBC, heurística (com pseudocódigo), prova de otimalidade e implementação.
- **05 Resultados e análise:** tabelas, três figuras, origem do ganho, gargalos, sensibilidade, propostas e limitações.
- **06 Conclusões.**

Nada disso foi compilado ainda: esta máquina não tem LaTeX. O artigo usa `pgfplots` e `algorithm`/`algpseudocode`, já incluídos em `relatorio/config/pacotes.tex`.

### O que falta, para o resto do grupo

1. **Revisão da literatura** (seção 02): um parágrafo crítico por referência, com modelo, ferramenta e resultados.
2. **Citações nas seções 03 a 05.** Estas afirmações pedem citação de uma fonte real e conferida:
   - o esquema serial (SGS) como "método construtivo clássico do RCPSP";
   - o CBC/COIN-OR e o PuLP;
   - a formulação indexada no tempo.

   Falta ainda o parágrafo marcado com `\preencher` na subseção "Discussão e limitações" da seção 5, que liga os nossos resultados à literatura.
3. **Introdução** (01), **resumo** (00, por último) e **referências** (07 e `bibliografia/referencias.bib`).
4. **Compilar o PDF** (Thales usa MiKTeX), conferir tabelas e figuras e remover as imagens de outro trabalho que vieram do template (`relatorio/imagens/*.png`).
5. **Slides** (`slides-finais/main.tex`): ainda são os da proposta. Os números têm de ser os da tabela acima.
   Já existem cinco gráficos prontos em `slides-finais/figuras/`:
   - prazos 310/307/285/187;
   - efeito de cada mudança na base de 285;
   - emissão contra análise;
   - cadeia que define os 285 dias;
   - equipes nas duas versões.

   Use com `\includegraphics[width=\textwidth]{figuras/01-prazos.png}`. Para gerar de novo: `.\.venv\Scripts\python.exe codigo\graficos_slides.py`. Precisa do matplotlib, que só é usado nos gráficos.
6. **Combinar no grupo:** apresentar 285 como resultado realista e 187 como limite, e decidir se o vínculo da compatibilização é restaurado na base.

Detalhes de todos os testes: [Análise de sensibilidade](analise-sensibilidade.md). Para reproduzir, rode `python codigo/sensibilidade.py` (cerca de 40 s, não usa o CBC). A rodada usada no artigo é `resultados/sensibilidade-20261124T002034Z.json`.

## O que já está pronto

Já definimos o problema, organizamos os dados e revisamos as regras e o programa. Também conferimos um exemplo à mão e verificamos se o programa chegava ao mesmo resultado.

O programa já encontrou um cronograma que respeita as regras e termina em **307 dias**, enquanto o cronograma usado como comparação termina em **310 dias**. Conseguimos, portanto, uma redução de **três dias, cerca de 1%**, sem aumentar as equipes.

Ainda não sabemos se é possível reduzir mais. O programa parou porque chegou ao limite de tempo de busca, antes de comprovar qual seria o menor prazo possível.

**Agora, o principal é explicar esse resultado, escrever o artigo e preparar a apresentação.** Não precisamos começar tudo novamente.

## 1. Entender o que mudou no cronograma

**Feito em 23/11:** ver [Análise de sensibilidade](analise-sensibilidade.md), seções 1 e 2 (cadeia crítica, folgas e carga das equipes). O texto abaixo é o pedido original.

Precisamos comparar o cronograma anterior com o de 307 dias. Quais atividades começaram antes? Quais mudaram de posição? Que mudanças ajudam a explicar a redução do prazo?

Não é preciso discutir todas as atividades no artigo. Podemos escolher alguns exemplos claros e montar uma tabela com o prazo anterior, o prazo encontrado e a diferença entre eles. Uma figura de um trecho do cronograma também pode ajudar.

Os resultados já estão guardados. A explicação e a localização dos arquivos estão em [Registro dos experimentos](experimentos.md).

## 2. Combinar se vale fazer mais testes

**Feito em 23/11:** cenários de equipes, de duração e de prazo de análise em [Análise de sensibilidade](analise-sensibilidade.md), seções 3 e 4. Para rodar novos cenários: `python codigo/sensibilidade.py` (cerca de 40 s, sem CBC). **Também em 23/11:** de onde vêm os 123 dias (esperas do praticado), o efeito das largadas tardias (se forem mantidas, o ótimo vai a 285 dias), as duas cadeias quase empatadas, medidas combinadas e a comparação com o CBC na instância pequena, nas seções 4A a 4F. A conferência no R14 mostrou que as largadas tardias esperavam a arquitetura, então o número realista é 285 dias (ganho de 25 dias, 8,1%) e 187 é o limite com as disciplinas liberadas no início (seção 4F). As perguntas que dependem de quem conhece o processo estão na seção 6.1. O texto abaixo é o pedido original.

Já temos um resultado para apresentar. Se houver tempo, podemos deixar o programa procurar por mais tempo ou testar o que acontece quando uma equipe consegue conduzir mais atividades ao mesmo tempo.

Esses testes ainda precisam ser escolhidos pelo grupo. Se forem feitos, devemos guardar os resultados e explicar o que mudou em cada tentativa. Não devemos alterar o cronograma original só para conseguir um resultado melhor.

**Se o prazo apertar, a prioridade é terminar o artigo e os slides com o resultado que já temos.**

## 3. Escrever o artigo

A estrutura do artigo está na pasta `relatorio`, mas o texto ainda precisa ser escrito. Podemos dividir assim:

| Parte | O que precisamos contar |
| --- | --- |
| Introdução | Qual é o problema e por que vale estudá-lo. |
| Trabalhos relacionados | O que outros autores fizeram e como isso se relaciona com o nosso caso. |
| Problema e modelo | Quais atividades estamos organizando, quais decisões o programa toma e quais regras deve respeitar. |
| Método | Como usamos o programa para procurar um cronograma melhor e conferir o resultado. |
| Resultados | O que encontramos, quais mudanças aconteceram e o que podemos concluir. |
| Conclusão | O que o estudo mostrou e quais limitações permanecem. |
| Referências | As fontes que realmente foram citadas no texto. |

O resumo deve ser escrito por último, quando o restante do texto estiver definido.

Para ajudar na escrita, já temos as [referências comentadas](referencias-comentadas.md), as [decisões do trabalho](decisoes-do-trabalho.md) e a [explicação matemática do modelo](formulacao-matematica.md).

### Cuidados ao explicar o trabalho

- O ganho encontrado pelo CBC foi de **310 para 307 dias**; o ótimo comprovado depois, pela heurística com limite inferior, é **187 dias**. Os 492 dias mencionados em registros antigos incluíam atividades de obra que saíram do nosso estudo; essa diferença não foi produzida pela otimização.
- A duração de uma atividade já inclui suas pausas. A capacidade da equipe representa quantas atividades ela pode manter abertas ao mesmo tempo.
- As capacidades foram estimadas pelo que aconteceu no cronograma anterior. Não sabemos se representam o máximo real das equipes.
- Os dias foram organizados em uma escala comum, sem reconstruir todos os feriados e recessos. Existem também limitações na extração e na preparação dos dados, que precisam ser explicadas.
- O prazo de 307 dias não era o melhor possível; o ótimo de 187 dias foi comprovado em 23/11.
- Os documentos originais do contratante e os dados que permitam identificar o projeto devem continuar fora do repositório público.

## 4. Revisar e gerar o PDF do artigo

Depois de escrever, precisamos conferir se o texto está claro, as equações estão explicadas, os números estão corretos e todas as citações têm referência. Também precisamos substituir os textos provisórios do modelo e gerar um PDF atualizado.

As instruções para montar o PDF estão em `relatorio/README.md`. O professor avaliará escrita, pesquisa bibliográfica, análise dos resultados, conteúdo e apresentação do texto, todos com o mesmo peso.

## 5. Atualizar os slides e ensaiar

Os slides finais estão na pasta `slides-finais`. Eles ainda precisam mostrar o que fizemos e o resultado obtido, em vez de falar apenas da proposta.

Uma divisão possível dos 12 minutos é: problema e objetivo (1,5 min), dados e regras (2 min), modelo e método (3 min), resultados (3,5 min), conclusão e limitações (1 min).

Precisamos dividir as falas, conferir se as figuras estão legíveis e ensaiar com cronômetro. Todos devem conseguir explicar:

- por que 285 e 187 são ótimos: o cronograma viável é igual ao limite inferior;
- por que 285 é o número realista e 187 é o limite;
- por que o CBC parou em 307;
- por que mais equipe não reduz o prazo.

## 6. Conferir a entrega

- [ ] O artigo está completo e o PDF abre corretamente.
- [ ] Os slides apresentam os mesmos números do artigo.
- [ ] Os resultados e as referências que usamos estão identificados.
- [ ] Não ficaram trechos antigos que contradizem o trabalho atual.
- [ ] As falas foram divididas e o ensaio coube em 12 minutos.
- [ ] O grupo confirmou quem enviará os arquivos, em qual formato e até que horário.

Uma divisão possível é deixar uma pessoa com a análise dos resultados, outra com a redação e as referências, e outra com os slides. O grupo ainda precisa combinar os responsáveis e revisar o conjunto.

Os detalhes de execução e o contexto para os agentes dos colegas estão em `roteiro-para-agentes.md`. Para acompanhar as pendências do grupo, este roteiro é suficiente.
