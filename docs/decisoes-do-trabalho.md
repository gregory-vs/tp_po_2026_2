# Decisões do trabalho

Este documento guarda o que combinamos e os motivos das escolhas. Será atualizado quando tomarmos ou revisarmos uma decisão, para facilitar a revisão do trabalho ao final.

## 1. Planejar o projeto desde o início

**Decidido em 21 de novembro de 2026.**

Vamos montar um novo cronograma para o projeto inteiro, incluindo as atividades que já aconteceram na prática. O cronograma praticado será usado para comparar os prazos.

**Por que escolhemos isso:** queremos avaliar quanto tempo poderia ter sido economizado com outra organização das atividades. Planejar desde o início facilita essa comparação e a explicação dos resultados no artigo.

## 2. Manter as atividades, as durações e as equipes responsáveis

**Decidido em 21 de novembro de 2026.**

O modelo escolherá quando cada atividade começa. Vamos manter todas as atividades previstas, a duração de cada uma e a equipe responsável por executá-la. O cronograma calculado deverá respeitar as dependências entre atividades e a capacidade das equipes.

**Por que escolhemos isso:** queremos medir o ganho obtido pela reorganização do cronograma. Mantendo o trabalho e as equipes responsáveis, conseguimos explicar melhor de onde veio uma eventual redução de prazo.

## 3. Interpretar a duração como o prazo entre começar e entregar

**Definição dos dados esclarecida por Thales em 21 de novembro de 2026.**

A duração de uma atividade é o intervalo entre seu início e sua entrega, em dias úteis. As pausas que acontecem durante a atividade já estão incluídas nesse número.

**Por que vamos usar essa interpretação:** ela corresponde ao significado dos dados do cronograma. Considerar todo esse intervalo como trabalho contínuo confundiria prazo com esforço da equipe. Acrescentar novas pausas a esse prazo também poderia contar a mesma espera duas vezes.

Naquele momento, a forma de representar a capacidade ainda estava em discussão; a escolha foi feita na decisão 4, abaixo. Esta definição não significa que a equipe fica dedicada exclusivamente à atividade até a entrega.

## 4. Usar a capacidade como limite de atividades abertas ao mesmo tempo

**Decidido em 21 de novembro de 2026.**

A capacidade de uma equipe será a quantidade máxima de atividades que ela pode conduzir ao mesmo tempo. Cada atividade conta nesse limite desde o início até a entrega, mesmo que existam pausas internas. Por exemplo, capacidade três permite manter até três atividades abertas, alternando o trabalho entre elas.

**Por que escolhemos isso:** as durações disponíveis já incluem as pausas e não mostram os dias de trabalho efetivo. Essa representação faz sentido para a rotina descrita por Thales e permite usar os dados disponíveis sem inventar uma distribuição diária de trabalho.

O modelo não vai medir nem escolher cada pausa interna. Também não vamos interpretar esse limite como número de pessoas ou como dedicação exclusiva a uma atividade. Os valores de capacidade de cada equipe ainda serão conferidos na revisão dos dados.

## 5. Preservar todos os vínculos na primeira versão

**Decidido em 21 de novembro de 2026.**

Vamos manter os vínculos do cronograma, tanto os que representam exigências técnicas quanto os que foram criados para organizar a execução. O modelo poderá ajustar os inícios e aproveitar as possibilidades de execução simultânea que essas regras permitem.

**Por que escolhemos isso:** o cronograma já considera as dependências técnicas, mas seus vínculos misturam essas exigências com escolhas de organização. Preservar todos evita liberar uma ordem sem conhecer seu motivo e permite avaliar a melhoria possível sob as regras existentes.

Isso também limita o ganho possível: uma ordem imposta por um vínculo continuará obrigatória. Se decidirmos estudar uma ordem mais livre dos blocos, identificaremos juntos quais vínculos de organização podem ser alterados. A revisão dos ajustes já feitos na preparação dos dados continua prevista.

## 6. Permitir início no mesmo dia da entrega anterior

**Decidido em 22 de novembro de 2026.**

Uma atividade pode começar no mesmo dia útil em que sua predecessora é entregue, desde que o vínculo não exija uma espera adicional. Por exemplo, uma entrega no dia 207 pode liberar o início da sucessora no próprio dia 207.

**Por que escolhemos isso:** Thales confirmou que essa liberação no mesmo dia é possível na rotina do projeto. A regra também corresponde à convenção já usada nos dados e no código.

Isso não elimina o limite de capacidade. Se as duas atividades pertencem à mesma equipe, ambas contam como abertas naquele dia e precisam caber no limite da equipe.

## 7. Usar a capacidade observada como referência inicial

**Decidido em 22 de novembro de 2026.**

Vamos usar como capacidade inicial de cada equipe o maior número de atividades que ela manteve abertas ao mesmo tempo no cronograma praticado. Esses valores já estão registrados nos arquivos de recursos. Na base completa, por exemplo, arquitetura tem referência sete e estrutura tem referência um.

**Por que escolhemos isso:** esses valores vêm do cronograma disponível e oferecem um ponto de partida para comparar a organização praticada com a calculada. Eles não comprovam a capacidade máxima das equipes, pois pode haver disponibilidade que não foi utilizada no cronograma.

Também vamos analisar o efeito de aumentar as capacidades, mantendo as demais regras. Ainda escolheremos quais equipes e quais aumentos testar. No artigo, explicaremos que as capacidades iniciais são estimadas a partir do cronograma.

## 8. Deixar a escrita do relatório para depois da revisão técnica

**Decidido em 22 de novembro de 2026.**

Vamos verificar o modelo e o código no passo 4 e realizar os experimentos do passo 5 antes de escrever o relatório. As referências já estão organizadas para consulta.

**Por que escolhemos isso:** Thales quer conferir o funcionamento do modelo e os resultados antes de redigir o artigo. A escrita será feita em conjunto pelo chat, etapa a etapa, com um agente separado dedicado à redação, sem edição automática do relatório no repositório.

## 9. Adotar um calendário comum para as equipes

**Decidido em 22 de novembro de 2026. Deve ser ressaltado no artigo e na apresentação.**

Vamos adotar um único calendário de dias úteis para todas as equipes, considerando fins de semana, feriados e recessos definidos para o estudo. A comparação entre o cronograma de referência e o calculado deverá usar o mesmo calendário.

**Por que escolhemos isso:** um calendário comum simplifica a representação do tempo e mantém uma base única para comparar os prazos. É uma hipótese adotada no estudo; não é uma confirmação de que todas as equipes seguem exatamente o mesmo calendário na prática.

**Limitação a explicar:** diferenças de disponibilidade entre equipes não serão representadas nesta versão. A lista de feriados e recessos ainda precisa ser obtida ou definida em conjunto antes de converter as datas. A decisão não autoriza presumir datas, ignorar recessos conhecidos ou considerar os CSVs atuais já conciliados com o original.

**Atualização:** a exigência de obter a lista foi substituída pela decisão 10. Mantemos o registro acima como histórico da escolha inicial.

## 10. Usar o cronograma original como fonte de referência, sem reconstruir o calendário

**Decidido em 22 de novembro de 2026. Deve ser ressaltado no artigo e na apresentação.**

Vamos considerar o cronograma original correto como fonte dos dados e usar as durações nele declaradas. Não vamos levantar uma lista de feriados e recessos nem recalcular as durações contando dias de segunda a sexta. O modelo trabalhará em uma escala comum de dias úteis, sem simular separadamente as exceções de calendário.

**Por que escolhemos isso:** Thales definiu o cronograma fornecido como fonte da verdade e optou por aproveitar as informações consolidadas nele, sem reconstruir seu calendário.

Essa decisão substitui a exigência de obter a lista da decisão 9. Ainda precisamos conferir se os CSVs reproduzem a fonte, porque houve ajustes anteriores de durações e vínculos. Aceitar a fonte não significa aceitar automaticamente essas transformações.

**Limitação a explicar:** o modelo compara prazos nessa escala de planejamento; não reconstrói datas exatas de entrega no calendário civil. Antes de calcular o ganho percentual, a referência e a solução precisam ter prazos expressos na mesma unidade e no mesmo recorte. A decisão não confirma automaticamente o valor de 492 dias registrado na base atual nem garante que a fonte seja viável sob todas as simplificações do modelo.

## 11. Corrigir a base usando as durações do original

**Decidido em 22 de novembro de 2026.**

Thales autorizou aplicar as durações declaradas no cronograma original e corrigir os erros identificados na base que usaremos no estudo.

**Por que escolhemos isso:** a conferência mostrou que a preparação anterior alterou durações e vínculos. Queremos que os parâmetros usados no trabalho tenham uma correspondência explicável com a fonte escolhida.

As correções serão feitas onde houver correspondência conferida. Quando não for possível identificar a linha no PDF, o dado ficará marcado como pendente, sem estimar um valor. Guardaremos os arquivos anteriores e o registro das alterações. As datas convertidas anteriormente não serão ajustadas artificialmente para caber nas novas durações nem usadas como referência validada de prazo.

## 12. Informar erros de cadastro antes de montar o modelo

**Decidido em 22 de novembro de 2026.**

Na leitura de uma instância, uma equipe sem capacidade cadastrada ou uma dependência com atividade ausente deve interromper o carregamento e informar o problema. Não vamos atribuir capacidade um nem descartar a dependência automaticamente.

**Por que escolhemos isso:** esses preenchimentos e descartes podem mudar o problema estudado sem que percebamos. Thales autorizou as duas correções após revisarmos a entrada dos dados. A criação de um recorte continua sendo feita explicitamente, com suas limitações documentadas.

## 13. Separar o código em módulos e centralizar a execução

**Decidido em 22 de novembro de 2026.**

Vamos usar uma `main.py` para coordenar a execução. A instância, o horizonte, o limite de tempo e a exibição dos logs serão editados em `configuracao.py`. Os caminhos dos dados serão montados a partir da pasta do projeto, sem precisar informá-los no terminal a cada execução.

O código ficará separado em leitura dos dados, variáveis, restrições, resolução e validação. A execução usual será `python main.py`. A entrada anterior continuará disponível para compatibilidade.

**Atualização após orientação de Thales:** todo código Python do projeto deve ficar dentro de `codigo/`, incluindo a entrada e a configuração. Os arquivos são agora `codigo/main.py` e `codigo/configuracao.py`, e a execução usual passa a ser `python codigo/main.py`. Essa organização mantém o código reunido em uma única pasta; substitui a localização inicial na raiz descrita acima. Os caminhos dos dados continuam calculados a partir da raiz do repositório.

**Por que escolhemos isso:** Thales quer revisar cada parte separadamente e executar o programa sem repetir caminhos e parâmetros no terminal. A separação permite acompanhar cada regra do trabalho no arquivo correspondente.

## 14. Definir as variáveis e a contagem do tempo

**Decidido em 22 de novembro de 2026.**

A escala começa no dia zero. Um horizonte de H dias contém os dias de zero até H−1.

- `x[a,t]` é binária e indica se a atividade a começa no dia t.
- `Cmax` representa o prazo do projeto e será minimizado.
- `S[a]` é o início calculado a partir de x. Não é uma decisão independente.
- Para duração positiva, a entrega é `F[a] = S[a] + duração − 1`.
- O término exclusivo é `C[a] = S[a] + duração`, usado para contar a ocupação.
- Para duração zero, `S[a] = F[a] = C[a]`: o evento respeita vínculos, mas não ocupa equipe.

O prazo deve ser pelo menos `F[a] + 1` para toda atividade ou evento. Assim, se a última entrega estiver no dia 5, o prazo será de seis dias da escala, mesmo quando essa entrega for um evento de duração zero. Isso conta o dia da entrega no prazo; não transforma o evento em trabalho de um dia.

Uma atividade positiva pode começar entre zero e `H − duração`. Um evento de duração zero pode ocorrer entre zero e `H−1`. Não criaremos variáveis para inícios que ultrapassem esses limites.

**Por que escolhemos isso:** queremos uma única regra de contagem de prazo para todas as entregas e garantir que o horizonte limite o cronograma inteiro. As durações e as equipes continuam fixas; o modelo escolhe os inícios.

**Ainda pendente:** definir como obter automaticamente um horizonte suficientemente grande. O limite dos inícios está decidido, mas a soma das durações, usada provisoriamente quando não há referência validada, pode ser insuficiente quando existem esperas. Não a consideramos um teto garantido.

## 15. Usar a entrada principal com auditoria automática e sem gerador de recortes

**Decidido em 22 de novembro de 2026.**

Vamos executar o projeto por `codigo/main.py`. A auditoria dos dados será uma etapa automática do carregamento; se houver falhas, o modelo não será montado. O arquivo `dados.py` continua responsável pela leitura e `validacao.py` continua responsável por conferir a solução depois da resolução.

Removemos `modelo_minimo.py`, que apenas mantinha o comando antigo, e `gerar_recorte.py`. A instância completa passa a ser a configuração padrão. As bases menores já existentes não foram apagadas, mas não vamos gerar novos recortes nesta etapa. Se isso voltar a ser necessário, discutiremos como refazer a ferramenta.

**Por que escolhemos isso:** Thales definiu que usaremos o conjunto inteiro e autorizou retirar os arquivos auxiliares dispensáveis. Integrar a auditoria evita depender de um comando separado antes de cada execução.

Esta decisão substitui a manutenção da entrada antiga mencionada na decisão 13. Não libera os dados pendentes nem altera as regras matemáticas aprovadas.

## 16. Conferir e restaurar a base da versão R14

**Decidido em 22 de novembro de 2026, após os esclarecimentos de Henrique e o envio do R14.**

O R14 passa a ser a versão de referência da base preparada. Vamos desfazer as alterações feitas exclusivamente pela comparação com o R15 e preservar os dados da preparação R14, conferindo sua consistência.

**Por que escolhemos isso:** Henrique esclareceu que os CSVs vieram do R14. As diferenças de duração encontradas no R15 eram mudanças de versão e não comprovavam erro na base. A conferência do R14 associou as 295 linhas anteriores a durações declaradas iguais e aos mesmos inícios convertidos.

Esta decisão revê a aplicação da decisão 11 ao R15. Continuamos usando durações declaradas; o que mudou foi a identificação correta da fonte. Também preservamos o cronograma normalizado da base R14, em vez de descartá-lo por não acompanhar as durações de outra versão. Seu prazo é uma referência na escala do modelo, sem prometer datas civis exatas.

Os PDFs originais, os mapas de identificadores e os registros detalhados da comparação ficam fora do repositório público. Nele manteremos os CSVs anonimizados e um relatório agregado da conferência. Os registros anteriores foram arquivados de forma privada antes da remoção.

As melhorias do código, incluindo o suporte a duração zero, permanecem; esse suporte não é usado pela base R14 atual. As atividades de obra continuam no conjunto. Três linhas adicionais visíveis no R14 e ausentes da base foram identificadas e permanecem como pendência de escopo; não decidimos incluí-las ou excluí-las nesta restauração.

## 17. Incluir as atividades identificadas e estudar somente o processo de projeto

**Decidido em 22 de novembro de 2026.**

Thales autorizou incluir as três atividades identificadas no R14 e encaminhou as orientações operacionais de Henrique para corrigir as equipes e retirar a execução de obra.

Incluímos a reunião de alinhamento do conceito, a consultoria normativa e a apresentação dos projetos à obra, com as durações declaradas. Preservamos os vínculos com atividades representadas na base. Referências a agrupadores foram expandidas para suas filhas presentes; não criamos tarefas para atividades ocultas no PDF. Três agrupadores referidos pela consultoria não têm filhas representadas, uma limitação que será explicada no trabalho.

As análises que estavam com projetistas passaram para as equipes do cliente: arquitetura/interiores para análise de produto e disciplinas técnicas para análise de engenharia. As quatro análises de estrutura passaram da coordenação para engenharia. Os dois gates atribuídos a projetistas passaram para as equipes de análise correspondentes. As aprovações da diretoria e os trâmites legais foram preservados.

Cinco emissões são briefings ou documentos produzidos pelo cliente e permaneceram com ele. A emissão de plantas de contrato passou para arquitetura. As atribuições de SMOP e os papéis múltiplos das quatro atividades originais foram mantidos. As duas reuniões novas também consomem simultaneamente a capacidade de todas as áreas participantes; cinco áreas adicionais da fonte receberam códigos anônimos de recurso.

Retiramos as duas atividades de execução de obra e seus seis agrupadores. A apresentação dos projetos à obra permanece, pois faz parte da entrega de projeto. Não acrescentamos um marco artificial: as entregas remanescentes já permitem calcular o prazo de projeto.

**Por que escolhemos isso:** o objetivo é reduzir o prazo do processo de projeto, e Henrique esclareceu quem realiza as emissões, análises e aprovações. Contar execução de obra misturava outro processo ao prazo estudado.

Depois das alterações, recalculamos todos os picos e conferimos novamente a referência. A base passou na auditoria com 243 atividades, 1008 vínculos, 39 recursos e prazo normalizado de 310 dias. A referência anterior de 492 dias incluía obra. A diferença entre esses dois números é mudança de escopo, não resultado da otimização. As capacidades continuam sendo estimadas pelos picos, sem comprovar o máximo operacional das equipes.

## 18. Usar um horizonte de 310 dias úteis

**Decidido em 22 de novembro de 2026.**

O horizonte da instância completa será de 310 dias úteis, configurado em `codigo/configuracao.py`. A escala vai do dia zero ao dia 309. Cada atividade só poderá começar em dias que permitam sua entrega dentro desse intervalo, conforme a decisão 14.

**Por que escolhemos isso:** já temos um cronograma de referência viável que termina em 310 dias, conferido contra todas as dependências e capacidades da base atual. Como queremos minimizar o prazo, limitar a busca a esse horizonte não exclui uma solução melhor. O modelo pode terminar antes; não fica obrigado a usar os 310 dias.

Esse teto continua válido nos testes em que apenas aumentamos capacidades, pois a referência permanece viável. Se mudarmos durações, vínculos ou reduzirmos capacidades, precisaremos conferir novamente sua viabilidade antes de usar a mesma justificativa.

Se `HORIZONTE=None`, o código poderá usar automaticamente uma referência validada. Sem referência e sem horizonte informado, a execução será interrompida com uma mensagem. Retiramos a alternativa pela soma das durações, que não garante espaço para as esperas. Um horizonte manual diferente pode ser usado, mas sua viabilidade precisa ser justificada; um valor menor pode excluir soluções.

Esta decisão encerra a pendência de escolha do horizonte da decisão 14. O horizonte é o intervalo do cronograma, distinto do limite de tempo de resolução em segundos.

## 19. Conferir a solução antes de aceitar o resultado do solver

**Decidido em 22 de novembro de 2026.**

Thales autorizou implementar os ajustes identificados na revisão da saída. Vamos extrair o cronograma somente quando houver uma candidata inteira, conferir seus valores e regras e apresentar prazo e ganho apenas depois dessa validação.

Usaremos PuLP 3.3.0, fixado no arquivo de dependências e instalado no ambiente virtual do projeto. Essa versão mantém a interface CBC usada pelo nosso código. A instalação anterior do ambiente estava na série 4 e foi substituída para manter uma versão única e compatível.

Os valores das variáveis devem ser finitos, próximos de zero ou um e escolher exatamente um início por atividade. A tolerância inicial é 0,000001, editável na configuração. Extrairemos o dia escolhido, sem truncar uma soma numérica. O validador também exigirá todas as atividades, sem IDs extras, e conferirá inícios, entregas, vínculos, capacidade e horizonte.

O prazo apresentado será calculado pelas entregas. O objetivo bruto do solver será preservado separadamente. Uma folga acima do prazo não torna o cronograma inviável; um objetivo abaixo do necessário revela inconsistência. Uma alegação de ótimo com dados inconsistentes não será aceita como prova.

Vamos distinguir ótimo comprovado, solução viável sem prova de ótimo, ausência de solução encontrada, inviabilidade informada com evidência, candidata rejeitada e erro de execução. O status isolado do problema não basta: a classificação considera também a situação da solução e o log do CBC. Limites ou gap ausentes não serão preenchidos como zero.

Cada chamada do solver terá log e registro JSON com o cronograma completo quando aceito, versões, parâmetros, tempo e classificação. Pediremos gap relativo e absoluto zero ao solver; uma parada antecipada com candidata válida poderá ser apresentada como viável, sem afirmar ótimo global. O limite de tempo continua sendo o configurado.

**Por que escolhemos isso:** resultados truncados, incompletos ou não conferidos não podem sustentar as conclusões do artigo. Também precisamos aproveitar soluções válidas obtidas dentro do limite de tempo sem confundi-las com ótimos comprovados.

As alterações foram verificadas com 27 testes, incluindo chamadas reais ao CBC somente em casos sintéticos pequenos. Os casos de limite de tempo, com e sem candidata, foram simulados de forma controlada. A referência real também passou no novo validador, sem executar a otimização da base completa.

## 20. Entregar o cronograma praticado ao solver como ponto de partida

**Decidido em 23 de novembro de 2026.**

Usaremos o cronograma praticado de 310 dias como solução inicial, técnica chamada de warm start. Antes de enviá-lo, o programa confere novamente os inícios, dependências, capacidades e o horizonte. O solver continua livre para mudar os inícios e buscar um prazo menor.

**Por que escolhemos isso:** na primeira execução, o CBC não encontrou uma solução inteira dentro do tempo de busca, embora já tivéssemos um cronograma viável conhecido. Fornecer esse cronograma permite que ele tente melhorá-lo a partir de uma solução existente. Isso não garante ganho nem prova de ótimo.

Registraremos se o CBC leu os valores e se confirmou a aceitação da solução. A simples leitura do arquivo não comprova o aceite. A solução final continuará passando pela validação independente antes de ser apresentada como resultado.

O recurso fica ativado em `codigo/configuracao.py`, com `USAR_WARM_START=True`. Se não houver referência completa ou ela violar alguma regra do cenário, o programa interrompe a preparação com uma explicação; podemos desativar o recurso para executar sem referência. A mudança não afeta uma execução já em andamento e não resolve a ultrapassagem do limite de tempo pelo CBC.

Na implementação, um teste pequeno confirmou a aceitação de uma referência de sete dias e sua melhoria para seis. A referência completa foi preparada e validada, sem iniciar uma nova otimização real.
