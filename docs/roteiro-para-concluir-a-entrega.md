# O que falta para terminar o trabalho

Atualizado em 23/11/2026. **A entrega é na quarta-feira, 25/11, com apresentação de 12 minutos.**

## O que já está pronto

Já definimos o problema, organizamos os dados e revisamos as regras e o programa. Também conferimos um exemplo à mão e verificamos se o programa chegava ao mesmo resultado.

O programa já encontrou um cronograma que respeita as regras e termina em **307 dias**, enquanto o cronograma usado como comparação termina em **310 dias**. Conseguimos, portanto, uma redução de **três dias, cerca de 1%**, sem aumentar as equipes.

Ainda não sabemos se é possível reduzir mais. O programa parou porque chegou ao limite de tempo de busca, antes de comprovar qual seria o menor prazo possível.

**Agora, o principal é explicar esse resultado, escrever o artigo e preparar a apresentação.** Não precisamos começar tudo novamente.

## 1. Entender o que mudou no cronograma

Precisamos comparar o cronograma anterior com o de 307 dias. Quais atividades começaram antes? Quais mudaram de posição? Que mudanças ajudam a explicar a redução do prazo?

Não é preciso discutir todas as atividades no artigo. Podemos escolher alguns exemplos claros e montar uma tabela com o prazo anterior, o prazo encontrado e a diferença entre eles. Uma figura de um trecho do cronograma também pode ajudar.

Os resultados já estão guardados. A explicação e a localização dos arquivos estão em [Registro dos experimentos](experimentos.md).

## 2. Combinar se vale fazer mais testes

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

- O ganho encontrado foi de **310 para 307 dias**. Os 492 dias mencionados em registros antigos incluíam atividades de obra que saíram do nosso estudo; essa diferença não foi produzida pela otimização.
- A duração de uma atividade já inclui suas pausas. A capacidade da equipe representa quantas atividades ela pode manter abertas ao mesmo tempo.
- As capacidades foram estimadas pelo que aconteceu no cronograma anterior. Não sabemos se representam o máximo real das equipes.
- Os dias foram organizados em uma escala comum, sem reconstruir todos os feriados e recessos. Existem também limitações na extração e na preparação dos dados, que precisam ser explicadas.
- O prazo de 307 dias respeita o modelo, mas ainda não foi comprovado como o melhor possível.
- Os documentos originais do contratante e os dados que permitam identificar o projeto devem continuar fora do repositório público.

## 4. Revisar e gerar o PDF do artigo

Depois de escrever, precisamos conferir se o texto está claro, as equações estão explicadas, os números estão corretos e todas as citações têm referência. Também precisamos substituir os textos provisórios do modelo e gerar um PDF atualizado.

As instruções para montar o PDF estão em `relatorio/README.md`. O professor avaliará escrita, pesquisa bibliográfica, análise dos resultados, conteúdo e apresentação do texto, todos com o mesmo peso.

## 5. Atualizar os slides e ensaiar

Os slides finais estão na pasta `slides-finais`. Eles ainda precisam mostrar o que fizemos e o resultado obtido, em vez de falar apenas da proposta.

Uma divisão possível dos 12 minutos é: problema e objetivo (1,5 min), dados e regras (2 min), modelo e método (3 min), resultados (3,5 min), conclusão e limitações (1 min).

Precisamos dividir as falas, conferir se as figuras estão legíveis e ensaiar com cronômetro. Todos devem conseguir explicar por que comparamos 310 com 307 dias e por que ainda não podemos afirmar que encontramos o melhor prazo possível.

## 6. Conferir a entrega

- [ ] O artigo está completo e o PDF abre corretamente.
- [ ] Os slides apresentam os mesmos números do artigo.
- [ ] Os resultados e as referências que usamos estão identificados.
- [ ] Não ficaram trechos antigos que contradizem o trabalho atual.
- [ ] As falas foram divididas e o ensaio coube em 12 minutos.
- [ ] O grupo confirmou quem enviará os arquivos, em qual formato e até que horário.

Uma divisão possível é deixar uma pessoa com a análise dos resultados, outra com a redação e as referências, e outra com os slides. O grupo ainda precisa combinar os responsáveis e revisar o conjunto.

Os detalhes de execução e o contexto para os agentes dos colegas estão em `roteiro-para-agentes.md`. Para acompanhar as pendências do grupo, este roteiro é suficiente.
