# Conferência da base com o cronograma R14

Atualização de 22/11/2026, após receber o R14 e os esclarecimentos de Henrique.

## Situação após as inclusões e correções aprovadas

A decisão 17 autorizou incluir as três linhas adicionais, corrigir as equipes conforme as orientações operacionais e retirar a execução de obra. A base atual tem **243 atividades, 47 agrupadores, 1008 vínculos e 39 recursos**. Seu prazo de referência normalizado é **310 dias**. A auditoria completa de durações, precedências e capacidades passou. Não foi executada otimização.

Foram corrigidas 15 atribuições de equipe e mantidas cinco emissões de documentos do cliente. As quatro atividades compartilhadas originais e as atribuições de SMOP foram preservadas. As duas reuniões incluídas listam todas as áreas participantes com códigos anônimos. O registro dos valores anteriores e atuais, das inclusões, dos vínculos e do corte está em `../dados/ajustes-projeto/registro.json`.

Os quinze vínculos adicionados seguem as relações declaradas para as atividades incluídas. A consultoria cita agrupadores; só foram expandidas filhas presentes no conjunto. Três desses agrupadores estão fechados e não têm filhas representadas, portanto sua cobertura não foi reconstruída. Essa limitação deve ser explicada, sem inventar tarefas ou afirmar cobertura integral do PDF.

O corte retirou duas atividades e seis agrupadores de obra. A diferença de 492 para 310 dias decorre desse recorte, não de melhoria calculada pelo solver. A pendência de incluir as três linhas foi resolvida; o restante deste documento preserva a conferência da base anterior, antes da decisão 17.

## Conferência da base de origem, antes da decisão 17

**A versão de origem da base é o R14. Restauramos os seis CSVs anteriores às alterações feitas pelo R15.** A comparação anterior misturava versões e não justificava alterar a base original. Os registros daquela comparação e os mapas de identificadores foram preservados fora do repositório público.

## O que foi conferido

Associamos as 295 linhas da base anterior a linhas do R14, pela ordem, duração e início convertido para a escala adotada. Em todas, a duração coincide com a declaração no PDF e o início coincide com a conversão usada na base. São 242 atividades e 53 agrupadores. Não há duração zero na fonte extraída nem na base restaurada.

O batimento detalhado é privado. Este documento e `../dados/conferencia-r14.json` contêm somente os resultados agregados, sem relacionar identificadores do PDF a identificadores anônimos.

As duas esperas, as duas equipes, os percentuais e as durações que havíamos alterado pelo R15 voltaram aos valores da preparação R14. As atribuições de equipes preenchidas por padrão continuam dependendo da validação operacional; a restauração não comprova que todas estão corretas.

## O cronograma de comparação

O cronograma praticado da base foi normalizado: usa inícios convertidos e términos coerentes com as durações declaradas. Não é uma reprodução exata das datas civis do PDF e não reconstrói feriados ou recessos.

Na escala do modelo, o prazo da base completa é 492 dias. A auditoria da cópia anterior aprovou durações, vínculos e capacidades; a restauração foi conferida byte a byte. Os 34 picos de capacidade da completa também foram recalculados e coincidem com os cadastrados. Isso estabelece consistência interna para o recorte preparado, não capacidade máxima real das equipes ou cobertura integral do empreendimento.

Segundo Henrique, os “79 ajustes” do relatório antigo se referem às datas praticadas, não às durações. A contagem individual desses ajustes não foi reconstruída. A atribuição anterior de 79 alterações às durações fica corrigida.

## Diferença de cobertura que ainda precisa ser esclarecida

A extração atual encontrou 307 linhas visíveis com nome e duração. O relatório antigo registra 304. Essa diferença não foi explicada pelo simples retorno ao R14.

Doze linhas do PDF ficam fora do alinhamento com as 295 linhas da base. Nove correspondem a níveis ou agrupamentos externos ao conjunto preparado. Outras três apresentam conteúdo de atividade e foram conferidas visualmente:

| Descrição genérica | Duração declarada |
| --- | ---: |
| Reunião de alinhamento do conceito | 3 dias |
| Consultoria normativa | 20 dias |
| Apresentação de projetos para a obra | 5 dias |

Não incluímos essas linhas automaticamente. Precisamos confirmar se ficaram fora por um critério de escopo ou por uma omissão na extração. Portanto, não devemos afirmar que a base contém todas as atividades visíveis do R14.

## Dependências e escopo

Mantivemos os 994 vínculos da preparação anterior. O relatório informa 22 remoções por ciclos e 37 por incompatibilidade com o cronograma normalizado. A lista individual não foi recuperada. Isso deve ser descrito como tratamento da base, sem afirmar que todos os descartes eram erros de extração ou foram tecnicamente validados.

Serviços preliminares e escavação permanecem no conjunto. A retirada dessas atividades e a eventual criação de um marco final são propostas ainda não decididas.

## Situação atual

Não há mais 52 durações pendentes: esse diagnóstico vinha da comparação com o R15. As durações da base foram conciliadas com o R14. O bloqueio dos experimentos reais agora registra a diferença de cobertura ainda sem explicação. A próxima discussão é confirmar o tratamento das três linhas adicionais e depois concluir a revisão do modelo antes dos experimentos.
