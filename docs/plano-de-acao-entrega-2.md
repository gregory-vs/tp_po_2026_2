# Plano para concluir a entrega 2

**Continuidade com os colegas, em 23/11/2026:** Thales encerrou sua participação nesta condução. O roteiro atual de pendências, com prioridades, arquivos e instruções, está em [Roteiro para concluir a entrega](roteiro-para-concluir-a-entrega.md). Ele é o ponto de partida para o restante do grupo. Já existe solução validada de 307 dias; os relatos de preparação abaixo preservam o histórico.

Queremos descobrir quanto podemos reduzir o prazo de um projeto de arquitetura e engenharia reorganizando suas atividades, sem desrespeitar as dependências entre elas nem sobrecarregar as equipes.

A entrega será um artigo e uma apresentação. Vamos usar o trabalho de Scrum enviado pelo professor como referência para explicar o modelo e apresentar os resultados. Faremos cada etapa juntos.

**Artigo e apresentação: quarta-feira, 25 de novembro de 2026. A apresentação dura 12 minutos.** O professor não pediu ajustes na primeira apresentação.

## 1. Decidir o que vamos estudar — escopo inicial definido

**Já decidimos manter as atividades, suas durações e as equipes responsáveis.** O modelo escolherá quando cada atividade começa, respeitando as dependências e a capacidade das equipes. Assim, vamos avaliar o ganho obtido pela reorganização do cronograma.

**Já decidimos planejar o projeto desde o início.** Todas as atividades poderão ser programadas novamente, inclusive as que já foram executadas no projeto real. O cronograma praticado servirá de comparação.

**Na primeira versão, vamos manter todos os vínculos do cronograma**, tanto as dependências técnicas quanto as escolhas de organização. Vamos avaliar a melhoria possível respeitando essas regras. A conferência dos dados continua necessária para entender os ajustes já feitos na preparação.

**A duração já inclui as pausas:** é o intervalo entre começar e entregar, em dias úteis. Ela não informa quantos dias de trabalho efetivo a equipe dedica à atividade.

**A capacidade será o limite de atividades abertas ao mesmo tempo por equipe.** Por exemplo, capacidade três permite conduzir até três atividades simultâneas, alternando o trabalho entre elas. Cada atividade conta nesse limite do início até a entrega. As pausas internas não serão medidas separadamente.

**Usaremos os picos observados no cronograma como capacidades de referência.** São estimativas baseadas no que aconteceu, não máximos comprovados das equipes. Também vamos testar o efeito de aumentar essas capacidades, mantendo as demais regras.

**Escopo definido:** buscar um prazo menor reorganizando os inícios, com as atividades, durações, equipes e vínculos existentes, respeitando o limite de atividades abertas por equipe.

## 2. Conferir os dados — base R14 restaurada

Henrique esclareceu que os CSVs vieram do R14. A comparação anterior com o R15 misturava versões. Recebemos o R14, conferimos a cópia preservada e restauramos os seis CSVs anteriores às alterações feitas pelo R15.

Na conferência da base de origem, as 295 linhas tinham duração igual à declarada em linhas associadas do R14. Eram 242 atividades, 53 agrupadores, 994 vínculos e 34 recursos. Não há duração zero nessa base. O prazo de referência na escala normalizada é 492 dias; os 34 picos de capacidade coincidem com os cadastrados. A auditoria interna confere essa referência, mas não comprova datas civis exatas ou capacidade máxima real das equipes.

A leitura identificou três atividades adicionais no R14. Após autorização, incluímos a reunião de alinhamento do conceito, a consultoria normativa e a apresentação de projetos à obra. Também corrigimos as equipes conforme as orientações de Henrique e retiramos a execução de obra. A base atual tem 243 atividades, 1008 vínculos e 39 recursos. A auditoria de entrada passou.

Segundo Henrique, os 79 ajustes antigos foram nas datas, preservando as durações. Os 59 vínculos removidos na preparação ainda não têm lista individual; explicaremos esse tratamento e suas limitações. As correções aprovadas trataram 15 atribuições de equipe; as demais imputações antigas não têm registro individual. Referências a agrupadores foram expandidas somente para filhas presentes, sem reconstruir tarefas ocultas no PDF.

**A referência atual é 310 dias úteis normalizados.** Os 492 dias pertenciam ao conjunto anterior, com obra. Essa diferença é mudança de escopo, não ganho da otimização. Recalculamos as capacidades: arquitetura passou de sete para seis, elétrica de três para uma; os demais recursos antigos mantiveram seus picos. As cinco áreas participantes adicionadas têm pico de uma atividade.

**Confirmamos que uma entrega pode liberar a sucessora no mesmo dia útil**, quando não há espera adicional. Se pertencem à mesma equipe, ambas contam na capacidade nesse dia.

**Usaremos as durações declaradas do R14, sem reconstruir feriados e recessos.** Compararemos prazos na escala normalizada de dias úteis, sob o mesmo conjunto de atividades e regras. Essa simplificação deve ser ressaltada no artigo e na apresentação.

Os PDFs e mapas de identificadores ficam fora do repositório público. O registro agregado está em [Conferência do cronograma original](</C:/Users/Thales Vasconcelos/Documents/Repos/tp_po_2026_2/docs/conferencia-cronograma-original.md>). As instâncias menores já existentes foram preservadas; a execução padrão usa a completa.

**Situação:** os ajustes aprovados foram aplicados e a base de projeto passou na auditoria. As limitações da preparação e dos agrupadores fechados devem ser explicadas no artigo. Continuaremos a revisão do modelo antes de executar os experimentos.

## 3. Estudar trabalhos parecidos — referências organizadas

Vamos buscar artigos sobre organização de projetos com equipes limitadas. Para cada um, explicar qual problema resolveu, como resolveu, quais resultados obteve e como se relaciona com o nosso.

Já avaliamos nove trabalhos da coletânea. Ding e colaboradores (2023) ajudam a explicar o RCPSP e suas variações. Kong e Dou (2020) são especialmente próximos por tratar de precedências e recursos em projetos de construção. Colares, Ngo-The e Ruhe e Duggan ajudam a comparar aplicações em projetos de software. O artigo de Scrum continua útil como exemplo de exposição; Faria e Fulgencio são referências secundárias.

Pass-Lanneau e colaboradores estudam cronogramas resistentes a mudanças nas durações. Esse trabalho ajuda na discussão das limitações e de possíveis extensões, mas sua otimização robusta vai além das durações fixas que escolhemos. A recomendação atual é priorizar Ding, Kong e Dou e Colares; a seleção definitiva ainda será discutida.

Um trabalho pode ajudar mesmo usando algoritmos híbridos: podemos discutir seu problema, modelo e resultados sem adotar seu algoritmo. A coletânea agora inclui referências diretamente sobre RCPSP e construção. Precisamos explicar as diferenças: nosso estudo trata da coordenação de projetos de arquitetura e engenharia, com atividades abertas até a entrega e pausas já incluídas nas durações.

A organização das nove referências, com importância, contribuição para o artigo e diferenças, está em [Referências para o artigo](</C:/Users/Thales Vasconcelos/Documents/Repos/tp_po_2026_2/docs/referencias-comentadas.md>). A base principal recomendada é Ding, Kong e Dou e Colares. Ngo-The e Ruhe, Duggan e Pass-Lanneau complementam a discussão. Scrum, Faria e Fulgencio ficam como apoio.

As referências já estão organizadas. A redação da revisão ficará para o final, junto com o restante do artigo, depois de verificarmos o modelo e os experimentos.

## 4. Revisar o modelo e o código — concluído

Concluímos a revisão lógica das variáveis, do horizonte de 310 dias e das quatro famílias de restrições: início único, dependências, capacidade e prazo final. As equações e os exemplos estão em [Formulação matemática](</C:/Users/Thales Vasconcelos/Documents/Repos/tp_po_2026_2/docs/formulacao-matematica.md>).

O código foi separado em módulos, a auditoria de entrada foi integrada e o tratamento dos resultados foi corrigido. A solução é conferida antes de apresentar prazo e ganho; a classificação distingue viabilidade e prova de ótimo. Os 27 testes passaram, incluindo CBC em casos sintéticos. A referência real de 310 dias passou no validador, sem otimização.

**Em 23/11/2026, concluímos a validação conjunta:** resolvemos A/B/C à mão, justificamos o ótimo de seis dias e Thales executou o mesmo caso no programa. O solver inverteu A e B, manteve as regras e comprovou o mesmo prazo de seis dias. Conferimos o JSON e o log; não houve erros. O registro está em [Validação manual](</C:/Users/Thales Vasconcelos/Documents/Repos/tp_po_2026_2/dados/validacao_manual/LEIA-ME.md>).

A revisão do passo 4 está encerrada para o modelo atual. As limitações dos dados continuam documentadas e devem acompanhar o artigo. Depois da validação manual, Thales selecionou `instancia_completa` e horizonte 310 e realizou a primeira execução real, registrada na etapa 5.

## 5. Fazer os testes e entender os resultados

**Resultado com solução inicial, em 23/11/2026:** o CBC aceitou a referência de 310 dias e encontrou um cronograma válido de 307 dias. A redução foi de três dias, aproximadamente 0,97%, sem aumentar capacidades. A busca terminou por tempo, sem provar ótimo; o limite inferior ficou em 187 dias e o gap do estudo em 39,09%. Foram solicitados 30 minutos e a chamada levou aproximadamente 36 minutos e 24 segundos. A próxima análise será entender as mudanças do cronograma e combinar se faremos novas buscas ou testes de capacidade. O relato abaixo preserva o histórico da primeira rodada e da preparação.

**Primeira execução real realizada em 23/11/2026:** o CBC terminou por tempo sem encontrar uma solução inteira. Foram solicitados 120 segundos, mas a chamada levou aproximadamente 534 segundos. O log informa limite inferior de 187 dias; a referência viável continua em 310. Não houve ganho de prazo calculado nessa rodada, nem prova de inviabilidade.

O registro está em [Experimentos](</C:/Users/Thales Vasconcelos/Documents/Repos/tp_po_2026_2/docs/experimentos.md>). Decidimos fornecer o cronograma de referência como solução inicial, preservando a liberdade de reorganizá-lo. Esse recurso já está implementado e ativado. Após os testes pequenos, Thales executou a base completa e obteve os 307 dias registrados acima. Ainda precisamos guardar o limite inferior quando a busca termina sem candidata; esse ajuste permanece pendente e não afeta o limite e o gap preservados na rodada atual.

Vamos escolher juntos os testes. A proposta é responder:

- O cronograma calculado termina antes do praticado? Quanto?
- Aumentar a capacidade de alguma equipe ajuda? Qual equipe faz diferença?
- O programa consegue resolver a instância completa dentro do tempo disponível? Que solução e limites consegue obter?

Em uma possível análise posterior, poderemos discutir a liberação de vínculos de organização para mudar a ordem dos blocos. Isso exigirá identificar juntos quais vínculos podem ser alterados.

**Ao terminar:** teremos tabelas e figuras com os resultados e uma explicação do que eles significam. Vamos distinguir uma solução viável de uma solução comprovadamente ótima.

## 6. Concluir o artigo e preparar a apresentação

Depois de verificarmos o modelo e os experimentos, vamos escrever o relatório em conjunto pelo chat, com auxílio de um agente separado, e reunir o texto nestas partes:

1. Introdução: problema, importância e objetivo.
2. Revisão da literatura: trabalhos relacionados.
3. Problema e modelagem: dados, regras e equações.
4. Método de solução: ferramentas e funcionamento do programa.
5. Resultados e análise: testes, comparações e limitações.
6. Conclusões e referências.

Depois adaptaremos os slides para mostrar o que fizemos e ensaiaremos a apresentação.

**Ao terminar:** teremos artigo revisado e apresentação pronta.

## Próximo passo

### O que temos e o que falta

| Parte | O que temos | O que falta para concluir |
| --- | --- | --- |
| Escopo | Objetivo, decisões e hipóteses principais registrados. | Incorporar eventuais ajustes que a validação exigir. |
| Dados | Três instâncias e verificações internas aprovadas. | Comparar com o original e justificar vínculos removidos e durações ajustadas. |
| Bibliografia | Nove trabalhos avaliados, PDFs no repositório e referências organizadas por importância. | Escolher as citações finais, conferir metadados e escrever a revisão no artigo. |
| Modelo matemático | Formulação proposta e núcleo implementado em Python. | Revisar equações, índices e limites de tempo, conferindo correspondência com o código. |
| Código | Leitura, auditoria dos dados, modelo mínimo e verificação de soluções. | Revisar os pontos identificados, executar exemplo pequeno e validar o resultado. |
| Experimentos | Comparações de prazo e aumentos de capacidade planejados. | Definir cenários e parâmetros; executar, guardar resultados e interpretar. |
| Relatório | Estrutura LaTeX em `relatorio/`, separada por seções, com orientações de preenchimento. | Redigir o conteúdo, cadastrar referências e inserir equações, tabelas e figuras; compilar e revisar. |
| Apresentação | Proposta original e estrutura em `slides-finais/`. | Atualizar para o trabalho realizado, incluir resultados e ensaiar para 12 minutos. |
| Entrega | Data e duração da apresentação confirmadas. | Conferir instruções finais de envio/formato e combinar responsabilidades. |

O relatório ainda contém marcadores de preenchimento; a bibliografia BibTeX ainda não tem entradas. Os slides finais ainda apresentam proposta e resultados esperados. Os resultados citados no README não foram reproduzidos e validados nesta condução conjunta.

Vamos discutir os achados da revisão do modelo e conferir a transformação de datas e marcos com o cronograma recebido. Depois aplicaremos as correções acordadas e validaremos um exemplo pequeno. A escrita do artigo fica para depois dos passos 4 e 5.

Também precisamos combinar a divisão de tarefas e conferir o formato exigido. A quantidade de páginas e de testes será definida conforme as orientações do professor e o tempo disponível. Os slides e o ensaio precisam caber nos 12 minutos de apresentação.
