# Referências para o artigo

Esta organização reúne os nove trabalhos que lemos para orientar a escrita do artigo. A importância indica quanto cada um ajuda no nosso problema, não uma avaliação geral da qualidade da publicação. Não precisamos citar todos: cada referência deve cumprir uma função clara no texto.

Nosso estudo busca reduzir o prazo de projetos de arquitetura e engenharia mantendo atividades, durações, equipes responsáveis e vínculos. A capacidade limita as atividades abertas simultaneamente, e as durações já incluem pausas. Essas escolhas orientam a comparação com a literatura.

## Nível 1 — Base principal

São os primeiros trabalhos a usar na fundamentação e na revisão da literatura.

### 1. Ding, Zhuang e Liu — 2023

**Extensions of the resource-constrained project scheduling problem.** Revisão publicada em Automation in Construction, volume 153, artigo 104958. DOI: 10.1016/j.autcon.2023.104958.

**Vai ajudar a:** definir RCPSP, explicar por que precedências e capacidade precisam ser consideradas juntas e situar nosso modelo entre as variantes do problema.

**Onde usar:** introdução, fundamentação do problema e justificativa das hipóteses. Começar pela introdução e pelas seções 4.1.1, 4.2 e 4.3.

**Diferença a explicar:** o RCPSP padrão descrito trata de processamento e consumo de recursos durante a execução. Nós contamos atividades abertas, com pausas incluídas no intervalo até a entrega. O artigo organiza a literatura; não apresenta um solver próprio cujos resultados possamos atribuir aos autores da revisão.

[Abrir o PDF](<referencias/1-s2.0-S0926580523002182-main.pdf>)

### 2. Kong e Dou — 2020

**RCPSP with Combined Precedence Relations and Resource Calendars.** Journal of Construction Engineering and Management, 146(12), 04020133. DOI: 10.1061/(ASCE)CO.1943-7862.0001929.

**Vai ajudar a:** explicar os diferentes vínculos entre atividades e a relação entre prazo, precedências e disponibilidade de recursos em projetos de construção. É uma referência próxima para discutir a representação matemática das dependências.

**Onde usar:** revisão da literatura, modelagem e comparação das hipóteses. Ler Problem Description, Model e Computational Experiments.

**Diferença a explicar:** usam relações combinadas, calendários por recurso e interrupções explícitas, com solução por algoritmo genético adaptado. Nós ainda não adotamos esses calendários ou interrupções como decisões. Estudar a execução de uma obra também difere de coordenar a elaboração dos projetos de arquitetura e engenharia.

[Abrir o PDF](<referencias/kong-dou-2020-rcpsp-with-combined-precedence-relations-and-resource-calendars.pdf>)

### 3. Colares — 2010

**Alocação de Equipes e Desenvolvimento de Cronogramas em Projetos de Software Utilizando Otimização.** Dissertação de mestrado, UFMG.

**Vai ajudar a:** aproximar o planejamento de projetos de software do nosso contexto, discutir os quatro tipos de dependência, a organização dos recursos e a redução do prazo. O estudo de caso e a análise de recursos versus prazo ajudam a organizar nossos experimentos.

**Onde usar:** contexto, trabalhos relacionados e planejamento da análise de resultados. Priorizar as seções 3.2.3, 3.3.6, 3.4, 5.2 e 5.4.3.

**Diferença a explicar:** considera escolha de equipes, produtividade e vários objetivos; usa NSGA-II. Nós mantemos equipes e durações e concentramos o objetivo no prazo. Consultar a modelagem sem copiar suas equações automaticamente.

[Abrir o PDF](<referencias/Colares - ALOCAÇÃO DE EQUIPES E DESENVOLVIMENTO DE CRONOGRAMAS EM PROJETOS DE SOFTWARE UTILIZANDO OTIMIZAÇÃO.pdf>)

## Nível 2 — Comparação e discussão

Complementam a base principal e ajudam a explicar escolhas, resultados e limites do nosso trabalho.

### 4. Ngo-The e Ruhe — 2009

**Optimized Resource Allocation for Software Release Planning.** IEEE Transactions on Software Engineering, 35(1), 109–123. DOI: 10.1109/TSE.2008.80.

**Vai ajudar a:** mostrar a importância de construir um cronograma viável ao planejar entregas e distribuir recursos. Também ajuda na discussão de qualidade das soluções e comparação com uma referência.

**Onde usar:** trabalhos relacionados e metodologia de avaliação. Ler as seções 2.1, 4, 6.5 e 7.

**Diferença a explicar:** escolhe funcionalidades para entregas com datas definidas e maximiza valor. Combina programação inteira e algoritmo genético. Nós executamos todas as atividades e minimizamos o prazo, sem alterar a equipe responsável.

[Abrir o PDF](<referencias/An Ngo-The e Ruhe - 2009 - Optimized Resource Allocation for Software Release Planning.pdf>)

### 5. Duggan, Byrne e Lyons — 2004

**A Task Allocation Optimizer for Software Construction.** IEEE Software, maio/junho, 76–82.

**Vai ajudar a:** discutir como dependências influenciam o prazo e mostrar como apresentar os resultados com cronogramas de Gantt. A aplicação relaciona distribuição de trabalho, competências e sequenciamento.

**Onde usar:** trabalhos relacionados e escolha das figuras para os resultados. Ler Optimizer for software construction e Experimental results.

**Diferença a explicar:** busca equilibrar prazo e defeitos estimados, alterando a distribuição do trabalho entre desenvolvedores. Usa algoritmo evolutivo e exemplos ilustrativos, sem comprovação de ótimo global. Nosso foco é prazo com equipes já definidas.

[Abrir o PDF](<referencias/Duggan et al. - 2004 - A task allocation optimizer for software construction.pdf>)

### 6. Pass-Lanneau, Bendotti e Brunod-Indrigo — 2024

**Exact and heuristic methods for Anchor-Robust and Adjustable-Robust RCPSP.** Annals of Operations Research, 337, 649–682. DOI: 10.1007/s10479-023-05537-6. Publicação online em 2023; volume de 2024.

**Vai ajudar a:** explicar o que fica fora do nosso modelo ao manter durações fixas. Também oferece um exemplo de avaliação computacional que distingue solução viável, ótimo comprovado, tempo e gap.

**Onde usar:** discussão das hipóteses, limitações, apresentação dos resultados computacionais e trabalhos futuros. Priorizar a seção 2.1 e as seções 5 e 6.

**Diferença a explicar:** considera incerteza nas durações, pior prazo e garantia de início de atividades. Não estamos implementando otimização robusta nem garantindo o comportamento do cronograma sob atrasos.

[Abrir o PDF](<referencias/s10479-023-05537-6.pdf>)

## Nível 3 — Apoio e uso opcional

Podem ser úteis, mas não são necessários para sustentar a parte central do nosso modelo.

### 7. Procopio e colaboradores — 2025

**Alocação ótima de tarefas em equipes Scrum usando Programação Linear Inteira.** Artigo do ENMC/ECTM e exemplo fornecido pelo professor.

**Vai ajudar a:** organizar a exposição das variáveis, restrições, ferramentas e experimentos de um artigo com programação inteira. É nossa principal referência de apresentação do trabalho.

**Onde usar:** preparação do artigo e comparação de aplicações de otimização na revisão. Consultar especialmente a metodologia e os resultados.

**Diferença a explicar:** seleciona tarefas e pessoas; sua restrição de dependência condiciona a seleção da predecessora, mas não programa a ordem temporal. Não usar como fundamento único das nossas equações de precedência. Sua importância como exemplo de escrita é alta, embora sua proximidade com nosso modelo seja menor.

[Abrir o PDF](<referencias/Alocacao de tarefas scrum.pdf>)

### 8. Faria e colaboradores — ano a confirmar

**Distribuição de Tarefas em uma Fábrica de Software: Equilibrando entregas e lucro em otimização Mono-Objetivo.** Ano e veículo de publicação ainda precisam ser confirmados.

**Vai ajudar a:** exemplificar distribuição de tarefas com capacidade e especialidades, além de mostrar como a escolha dos objetivos muda a solução.

**Onde usar:** comparação secundária de problemas de alocação, se essa discussão acrescentar algo à revisão.

**Diferença a explicar:** trata de lucro e atendimento aos clientes, sem construir cronograma temporal ou representar precedências entre tarefas. Não é base principal para nossa formulação ou para explicar o funcionamento do solver.

[Abrir o PDF](<referencias/Faria et al. - Distribui¸ca˜o de Tarefas em uma Fa´brica de Software Equilibrando entregas e lucro em otimiza¸ca˜o.pdf>)

### 9. Fulgencio — 2025

**Otimização da Distribuição de Carga de Trabalho em Equipes.** Trabalho de conclusão de curso, UFMG.

**Vai ajudar a:** discutir fatores humanos que não representamos, como motivação, competência, aprendizado e carga cognitiva.

**Onde usar:** limitações ou trabalhos futuros, caso haja espaço e relação clara com a discussão. Pode ficar fora da seleção final.

**Diferença a explicar:** atribui funcionários a tarefas com lógica fuzzy e algoritmos evolutivos multiobjetivo. Não constrói o sequenciamento temporal do nosso problema. Limitar o total de tarefas por funcionário não equivale a limitar atividades abertas simultaneamente.

[Abrir o PDF](<referencias/Fulgencio - 2025 - OTIMIZAÇÃO DA DISTRIBUIÇÃO DE CARGA DE TRABALHO EM EQUIPES.pdf>)

## Como transformar a seleção em revisão da literatura

Começar por Ding para apresentar o problema, depois Kong e Dou para discutir precedências e recursos. Usar Colares como ponte para o planejamento de projetos de software. Acrescentar Ngo-The e Ruhe e Duggan quando suas diferenças ajudarem a situar nossa aplicação. Pass-Lanneau ajuda a explicar a opção por um modelo com durações fixas e a discutir continuidade.

Para cada referência incluída, escrever um parágrafo com o problema estudado, o modelo, o método, os resultados pertinentes e a relação com nosso trabalho. No caso de Ding, descrever a síntese da revisão, sem atribuir a ele experimentos dos autores revisados.

Não precisamos criar ou reproduzir os algoritmos dos artigos. Nosso artigo pode contribuir pela modelagem e avaliação do caso estudado. As pausas incluídas nas durações e a capacidade como atividades abertas devem ser apresentadas como hipóteses da nossa aplicação, sem afirmar que as referências comprovam essas escolhas.
