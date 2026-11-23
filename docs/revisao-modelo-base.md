# Revisão do modelo e do código

**Encerramento da revisão em 23/11/2026:** o exemplo A/B/C foi resolvido à mão e executado por Thales. JSON e log confirmam o ótimo de seis dias com B0–1, A2–4, C4–5, sem violações. A inversão de A/B preserva o ótimo manual. Com as quatro famílias revisadas e os 27 testes, o passo 4 foi concluído no escopo atual. A otimização da base real continua pendente. Evidências e instruções em `../dados/validacao_manual/LEIA-ME.md`. Os diagnósticos abaixo preservam a evolução anterior da revisão.

A descrição matemática completa para revisão conjunta está em [Formulação matemática](formulacao-matematica.md), com variáveis, parâmetros, objetivo e restrições. Este arquivo mantém a avaliação da implementação e suas pendências.

Situação em 22/11/2026, após conciliar a versão de origem com o R14. A revisão inicial usou por engano o R15 para corrigir uma base extraída do R14; essas alterações dos dados foram desfeitas. A conferência atual está em conferencia-cronograma-original.md. O registro detalhado anterior foi arquivado fora do repositório por conter mapas de identificadores.

## Modelo aprovado

Planejar desde o início, com atividades, durações e equipes fixas. Minimizar o prazo respeitando início único, vínculos e limite de atividades abertas. As pausas já integram a duração; capacidade não representa número de pessoas.

O código está em codigo/, com entrada em main.py, configuração em configuracao.py e módulos separados para dados, auditoria de entrada, variáveis, restrições, resolução e validação da solução. A auditoria usa os mesmos dados lidos, antes de montar o modelo.

## Variáveis e tempo

- x[a,t] é binária e escolhe o início.
- S[a] é a soma dos dias multiplicados por x.
- F[a]=S[a]+max(d[a],1)-1 é o dia da entrega.
- C[a]=S[a]+d[a] é o término exclusivo para contar ocupação.
- Cmax representa o prazo e é minimizado, com Cmax>=F[a]+1.
- Positivos têm início admissível de zero a H-d[a]; eventos, de zero a H-1.

Os eventos de duração zero têm S=F=C e não ocupam equipe. O código mantém esse suporte, mas não há tais eventos na base R14 restaurada. O prazo final conta todos os dias da escala desde zero, inclusive o dia de um evento terminal.

## Dependências e capacidade

TI: S[b]>=F[a]+lag. II: S[b]>=S[a]+lag. TT: F[b]>=F[a]+lag. IT: F[b]>=S[a]+lag. Igualdade é permitida quando o lag é zero; II e TT não obrigam igualdade.

Uma atividade positiva ocupa cada equipe listada em todos os dias de S até F, inclusive. Duas atividades podem contar no dia da entrega e início compartilhado. A soma por equipe e dia não pode superar a capacidade. O código acessa apenas variáveis dos inícios admissíveis.

## Dados e referência

A base atual usa o R14 com os ajustes de projeto aprovados na decisão 17: 243 atividades, 1008 vínculos, 39 recursos e prazo de referência normalizado de 310 dias. Foram incluídas três atividades, corrigidas 15 atribuições de equipe e retiradas duas atividades de execução de obra e seis agrupadores.

Os inícios e durações das atividades remanescentes foram preservados. Os picos de capacidade foram recalculados e a referência passa em todos os vínculos e limites da auditoria. A diferença da referência anterior de 492 dias vem da mudança de escopo, não de otimização.

Persistem limitações da preparação: 59 vínculos removidos sem lista individual, imputações sem marcação por linha e referências a agrupadores com tarefas ocultas. As relações novas foram expandidas apenas para folhas presentes; três agrupadores citados pela consultoria não têm folhas representadas. Não se afirma cobertura integral do projeto real. As três linhas adicionais antes pendentes já foram incluídas e a auditoria libera o recorte aprovado.

## Pontos ainda em revisão

1. Horizonte definido e aplicado: 310 dias, justificado pela referência viável da base atual. Os domínios limitam as entregas ao dia 309. No modo automático, só usar referência validada; sem ela, exigir um valor explícito. O fallback pela soma das durações foi removido (decisão 18).
2. Distinguir solução encontrada de prova de ótimo, especialmente sob limite de tempo.
3. Conferir integralidade antes de converter números com int() e fazer erros da validação impedirem aceitar resultados.
4. Reforçar mensagens para entradas malformadas; equipe sem capacidade e vínculo com ponta ausente já são rejeitados.
5. Explicar a seleção da base e as limitações dos agrupadores ocultos e das imputações; as três inclusões e as correções operacionais já foram aplicadas.
6. Alinhar o artigo à formulação efetiva. O PDF antigo de modelagem inclui replanejamento, revisões variáveis e outras extensões não aprovadas.

## Verificação realizada

### Implementação dos ajustes da saída — decisão 19

As recomendações abaixo foram autorizadas e implementadas. PuLP 3.3.0 foi fixado e instalado no ambiente virtual. O novo módulo `codigo/resultados.py` confere os valores antes de escolher um início por atividade e classifica a saída usando status do problema, situação da solução e evidência do log.

`codigo/validacao.py` agora verifica o conjunto completo de atividades, integralidade, horizonte, precedências e capacidades, retornando erros sem imprimir aceitação antecipada. A resolução rejeita candidatas inválidas antes de mostrar ganho e devolve um resultado estruturado à entrada principal. Cmax bruto é preservado; o prazo do cronograma é calculado por maior entrega mais um. Resultados sem prova continuam classificados como viáveis quando passam na conferência.

Cada rodada grava log e JSON com classificação, ambiente, parâmetros, tempo e cronograma aceito. O CBC recebe gap relativo e absoluto zero. Um limite inferior só é usado se disponível e consistente; o gap do estudo tem fórmula explícita e não é preenchido como zero quando desconhecido. O código também prepara o caminho temporário curto no Windows, pois a interface usada pelo CBC separa argumentos por espaços.

**Verificação:** 27 testes aprovados, incluindo quatro testes com CBC em problemas sintéticos, casos controlados de limite de tempo com e sem candidata, precisão numérica, valores ausentes/fracionários, atividade faltante, objetivo com folga e erro de execução. A referência real de 243 atividades foi novamente conferida e continua viável em 310 dias. A otimização da base real não foi executada. Os achados seguintes preservam o diagnóstico anterior à implementação.

### Revisão da extração e aceitação dos resultados

**Diagnóstico anterior à decisão 19:** os achados desta seção motivaram os ajustes registrados acima. A formulação matemática não precisou mudar. As propostas deixaram de ser apenas recomendações após a autorização e implementação; o texto abaixo preserva as razões da mudança.

#### 1. O status atual não basta para declarar ótimo

`resolucao.py` imprime `modelo.status` e só extrai valores quando esse número é um. Precisamos distinguir a existência de uma solução inteira da prova de que nenhuma solução melhor existe.

No adaptador CBC do PuLP 3.3.0, uma interrupção com solução pode produzir status de problema associado a ótimo enquanto o status da solução indica apenas solução inteira viável. Isso está explícito em `get_status`, no [código oficial dessa versão](https://raw.githubusercontent.com/coin-or/pulp/3.3.0/pulp/apis/coin_api.py). Portanto, o teste atual isolado não documenta prova de ótimo.

**Proposta:** interpretar o status do problema, a situação da solução e o motivo de parada na versão escolhida. Preservar o log e os limites disponíveis. Parada por tempo, nós ou gap deve ser descrita pelo que efetivamente comprovou; ausência de prova de ótimo não invalida uma solução viável.

#### 2. A dependência precisa de uma versão definida

`requirements.txt` contém `pulp>=2.7`. O código usa a API de variáveis e CBC da série 3.x. A série 4 alterou criação de variáveis, resultados e interface do CBC; a instalação sem limite de versão pode exigir migração. Ver [guia oficial de migração](https://www.coin-or.org/pulp/guides/how_to_migrate_to_v4.html).

**Proposta:** fixar uma versão compatível antes de preparar o ambiente. PuLP 3.3.0 é uma candidata, cuja [versão oficial](https://github.com/coin-or/pulp/releases/tag/3.3.0) e adaptador CBC foram consultados. A instalação e a disponibilidade efetiva do executável ainda precisarão ser verificadas. Fixar essa versão é recomendação, não decisão já aplicada.

#### 3. Não truncar os números antes de conferir a solução

Hoje o código usa `int()` no objetivo e no início calculado. Por exemplo, `int(4.999999999)` retorna quatro, embora o valor esteja numericamente próximo de cinco. Além disso, um início inteiro calculado como média não prova que os x eram binários: valores fracionários podem se combinar e resultar em uma soma inteira.

**Proposta:** primeiro confirmar valores presentes, numéricos e finitos; conferir os limites e a proximidade de cada x a zero ou um, usando tolerância explícita; exigir exatamente um início escolhido por atividade; então extrair o índice escolhido e conferir as expressões derivadas. Não usar arredondamento para transformar uma solução efetivamente fracionária em inteira.

#### 4. Conferir também se todas as atividades foram extraídas

O argumento de atividades de `verificar_solucao` não é usado para comparar o conjunto esperado com os inícios recebidos. Em uma chamada pontual, um cronograma vazio passou quando a instância continha uma atividade obrigatória sem vínculos. Isso demonstra uma lacuna do validador isolado, não que o executor tenha produzido esse caso numa otimização.

**Proposta:** conferir igualdade entre os IDs esperados e os extraídos, rejeitando faltantes, extras e valores inválidos. Depois, verificar integralidade dos inícios, domínio por atividade, durações, todas as precedências, capacidade e prazo. A soma única das binárias também precisa ser conferida antes da conversão para o cronograma.

#### 5. Separar o prazo efetivo do objetivo bruto devolvido

O prazo do cronograma extraído é `max(F[a])+1`. O valor bruto de Cmax pode conter folga numa solução sem prova de ótimo. Uma chamada pontual mostrou que o validador atual rejeita essa diferença mesmo quando os inícios e as entregas formam um cronograma viável.

**Proposta:** preservar ambos os valores, conferir se o objetivo bruto cobre todas as entregas e usar o prazo calculado do cronograma para apresentar sua duração. Um objetivo abaixo do necessário revela inconsistência. Uma folga acima do necessário não torna os inícios inviáveis; ela também não autoriza declarar ótimo. Se a saída alegar ótimo e houver diferença relevante, investigar a inconsistência antes de aceitar a classificação. Só apresentar limites e gap quando compatíveis com os valores reportados e disponíveis de forma confiável.

#### 6. Validar antes de mostrar ganho e aceitar a execução

Atualmente, o programa imprime prazo, comparação e cronograma antes da validação. O validador retorna uma lista de erros, mas `resolver` ignora esse retorno. A função principal também não recebe um resultado estruturado que diferencie solução aceita, ausência de solução e erro.

**Proposta:** concluir a conferência antes de mostrar resultados como válidos. Se houver erro, rejeitar a candidata e não apresentar ganho como resultado do trabalho. Retornar uma classificação explícita para a entrada principal, sinalizando falhas de execução ou validação. Terminar sem solução deve ser distinguido de comprovar inviabilidade.

#### Fluxo proposto para a saída

1. Executar o solver e registrar ambiente, tempo e motivo de parada.
2. Verificar se há uma candidata inteira disponibilizada; valores de relaxação não bastam.
3. Conferir valores brutos e extrair um início válido por atividade.
4. Conferir independentemente o cronograma e calcular seu prazo efetivo.
5. Confrontar objetivo bruto, prazo, limites e evidências de término.
6. Classificar e só então apresentar ou guardar prazo, ganho e cronograma aceitos.

| Classificação proposta | Condição |
| --- | --- |
| Ótimo comprovado | Cronograma válido e evidência de otimalidade, com tolerâncias declaradas. |
| Viável sem prova de ótimo | Cronograma válido, mas a busca parou sem essa comprovação. |
| Sem solução encontrada | Nenhuma candidata inteira válida disponibilizada; não prova inviabilidade. |
| Inviável comprovado pelo solver | Término com prova de inviabilidade. Na base atual, que tem referência viável, exigiria investigar divergência entre formulação e referência. |
| Candidata rejeitada | Valores ou cronograma não passam na validação. |
| Erro de execução | Biblioteca, executável ou chamada não funcionou. |

O registro deve guardar pelo menos classificação, motivo de parada, prazo calculado, objetivo bruto, tempo e erros. Quando houver limite inferior e gap confiáveis, guardá-los; quando não houver, indicar indisponibilidade, sem preencher zero automaticamente.

#### Evidência desta revisão

Foram lidos `codigo/resolucao.py`, `codigo/validacao.py`, `codigo/main.py` e `codigo/requirements.txt`. Em chamadas pontuais do validador atual, sem solver: atividade obrigatória ausente retornou lista vazia; objetivo com folga gerou erro de prazo; sobreposição acima da capacidade foi detectada. Também foi verificado o exemplo de truncamento. Não foram instaladas bibliotecas ou executados CBC e otimização. A próxima implementação deve cobrir esses casos e paradas com e sem candidata antes de usar os resultados no artigo.

Compilação, leitura, auditoria integrada, domínios, quatro vínculos, ocupação e prazo de eventos foram conferidos sem executar solver. Após a restauração, os seis CSVs foram comparados byte a byte com a cópia preservada e a auditoria interna foi repetida com aprovação para completa e média. Após as inclusões, as correções operacionais e o corte de obra, a auditoria foi repetida com sucesso e os metadados liberam a base do recorte aprovado. A otimização continua sem execução nesta revisão; PuLP não foi encontrado no Python consultado.

As fontes originais e os mapas permanecem privados. A documentação pública apresenta apenas os resultados agregados e os identificadores anônimos usados pelo modelo.
