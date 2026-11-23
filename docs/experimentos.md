# Registro dos experimentos

Este documento reúne resultados observados e propostas de continuação. Não substitui o artigo nem autoriza novos cenários automaticamente.

## 1. Primeira execução da base completa — 23/11/2026

Execução realizada por Thales, após a validação manual A/B/C. Cenário: atividades, durações, vínculos e capacidades atuais, sem aumento de recursos.

| Item | Valor observado |
| --- | --- |
| Atividades / vínculos / recursos | 243 / 1008 / 39 |
| Horizonte e referência viável | 310 dias úteis normalizados |
| Variáveis | 72381 binárias de início e uma contínua de prazo |
| Restrições | 13584 |
| Coeficientes não nulos lidos pelo CBC | 1696037 |
| PuLP / CBC | 3.3.0 / 2.10.3 |
| Limite solicitado | 120 segundos, com gap relativo e absoluto zero |
| Tempo medido pela aplicação na chamada | 534,459 segundos |
| Tempo de resolução informado pelo CBC | 531,32 segundos |
| Resultado | Nenhuma solução inteira encontrada; parada por tempo |
| Limite inferior final informado no log | 187 dias |
| Nós enumerados na árvore principal | 0 |
| Iterações | 396954 |

Evidências: `../resultados/20261123T032556146188Z-248df388.json` e `../resultados/20261123T032556146188Z-248df388.log`.

### Interpretação

A execução não comprovou inviabilidade. A referência de 310 dias continua sendo um cronograma conhecido e validado independentemente. O solver, nessa rodada, não encontrou uma candidata inteira por sua própria busca. O código atual usa o prazo da referência para justificar o horizonte, mas ainda não envia seus inícios como solução inicial ao CBC.

Os 187 dias são um limite inferior da busca, não um cronograma encontrado. Considerando esse limite e a referência viável externa, o ótimo do modelo está entre 187 e 310 dias. Não há redução de prazo obtida por essa rodada para reportar. O JSON registra corretamente ausência de candidata, prazo e gap, mas não preserva o limite inferior disponível no log; essa lacuna de registro deverá ser corrigida.

O log confirma que `-sec 120` e tempo decorrido foram passados ao CBC. A ultrapassagem ocorreu dentro do executável: ele informou aproximadamente 531 segundos. O processamento da raiz, com relaxação, heurística e cortes, consumiu a busca sem enumerar nós da árvore principal. Isso explica onde a demora apareceu; o log não identifica sozinho cada causa interna. O limite solicitado não funcionou como prazo rígido de encerramento nesta execução.

### Continuação proposta após a primeira rodada

O item 1 foi autorizado e implementado posteriormente, conforme a seção 2 abaixo. Os demais itens continuam pendentes de implementação ou avaliação.

1. Enviar ao CBC o cronograma normalizado de 310 dias como solução inicial, conferindo novamente sua viabilidade e verificando no log se foi aceito. Essa técnica é chamada de warm start. Não fixar os inícios: o solver deve continuar podendo melhorá-los.
2. Preservar no JSON o limite inferior mesmo quando não houver candidata, mantendo prazo e gap da busca indisponíveis nesse caso.
3. Se necessário, estudar redução segura dos dias admissíveis por precedências e ajustes da estratégia de busca, sem alterar o problema matemático. Não remover vínculos ou atividades para obter uma solução.
4. Registrar tempo solicitado e observado separadamente. Qualquer nova configuração será combinada com Thales antes de executar.

## 2. Preparação do warm start — 23/11/2026

Thales autorizou usar o cronograma praticado como solução inicial. O programa confere novamente todas as atividades, dependências, capacidades e o horizonte antes de enviar os valores. Cada variável binária recebe zero ou um, e a variável de prazo recebe a última entrega mais um. Os inícios continuam livres para o solver melhorar o cronograma.

Configuração atual em `codigo/configuracao.py`: instância completa, horizonte de 310 dias, limite de 1.800 segundos e `USAR_WARM_START=True`. A nova execução completa ainda não foi feita por este agente; a configuração só vale para uma nova chamada do programa.

**Verificações realizadas:**

- A referência completa passou na conferência, com 243 atividades e prazo de 310 dias. Foram preenchidos 72.382 valores iniciais, sem chamar o solver para a base completa.
- Em um teste sintético com três atividades, o CBC leu os 22 valores iniciais, aceitou o prazo de sete dias e o melhorou para seis. Isso confirma que os inícios não ficaram fixos. Não é resultado do projeto real.
- Os 32 testes passaram, incluindo rejeição de referência ausente ou incompatível com dependências, capacidade ou horizonte.

O teste detectou que o CBC 2.10.3 para Windows não abriu o caminho absoluto do arquivo inicial: acrescentou `.\\` ao nome. O adaptador passou a usar caminhos relativos, sem espaços, em uma pasta temporária exclusiva, removida depois da chamada. A aceitação foi confirmada após essa correção.

O JSON registra separadamente a referência validada, a quantidade de valores lidos pelo CBC e a confirmação de aceitação. Somente ler o arquivo não comprova que a solução foi aceita. Ao final, o terminal informa `Warm start aceito pelo CBC: custo 310.` se o log confirmar esse aceite na base completa. Sem confirmação, apresenta um aviso.

O warm start não garante melhoria nem prova de ótimo. Também não transforma o limite de tempo do CBC em um prazo rígido de encerramento. Se o solver não devolver uma candidata, o programa continua distinguindo a referência conhecida de um resultado obtido na busca.

## 3. Execução completa com warm start — 23/11/2026

Execução realizada por Thales. JSON e log conferidos: `../resultados/20261123T034835057589Z-8a258fda.json` e `../resultados/20261123T034835057589Z-8a258fda.log`.

O CBC leu os 72.382 valores e aceitou a referência com custo de 310 dias. A busca encontrou 308 dias aos 815,25 segundos e 307 dias aos 924,12 segundos, nos tempos informados pelo CBC. Encerrou por limite de tempo com 823 nós enumerados e 634.163 iterações.

| Indicador | Resultado |
| --- | --- |
| Referência / horizonte | 310 dias |
| Melhor cronograma encontrado | 307 dias, validado, sem erros ou avisos |
| Redução observada | 3 dias, aproximadamente 0,97% |
| Limite inferior final | 187 dias |
| Gap do estudo | (307−187)/307 = 39,0879% |
| Limite solicitado | 1.800 segundos |
| Tempo medido pela aplicação | 2.183,904 segundos, aproximadamente 36 min 24 s |
| Tempo de resolução informado pelo CBC | 2.180,41 segundos |
| Classificação | Solução viável sem prova de ótimo |

O intervalo conhecido passou a ser 187 ≤ ótimo ≤ 307 dias. O ganho de três dias foi obtido com as mesmas atividades, durações, vínculos e capacidades da referência. Não podemos afirmar que essa é a maior redução possível. O limite inferior permaneceu em 187, deixando uma distância grande até a melhor solução encontrada.

O CBC mostra `Gap: 0.64`, enquanto a aplicação mostra 39,0879%: os denominadores diferem. Aqui adotamos a fórmula registrada no JSON, (307−187)/307; usando o limite inferior no denominador, (307−187)/187 é aproximadamente 64,17%. Não misturar essas medidas nas tabelas do artigo.

O warm start foi aceito e houve melhoria nesta rodada. Como o tempo solicitado também aumentou de 120 para 1.800 segundos, a comparação com a primeira execução não isola o efeito do warm start. A ultrapassagem do tempo solicitado persistiu. Nenhuma nova rodada foi iniciada pelo agente ao analisar esse resultado.
