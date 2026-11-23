# Formulação matemática: variáveis, objetivo e restrições

Documento de trabalho para nossa revisão conjunta. Descreve o modelo implementado, considerando as decisões já aprovadas. Não significa que a validação pelo solver foi concluída. Atualizado em 22/11/2026.

Queremos escolher quando cada atividade de projeto começa, para terminar o conjunto no menor prazo possível. As atividades, durações, equipes responsáveis e dependências são dados fixos. O modelo não escolhe quais atividades executar nem altera quem as realiza.

## 1. Conjuntos e índices

| Símbolo | Significado |
| --- | --- |
| $A$ | Conjunto de atividades incluídas na otimização, sem os agrupadores do CSV. |
| $A^+$ | Atividades com duração positiva: $A^+=\{a\in A:d_a>0\}$. |
| $A^0$ | Eventos de duração zero: $A^0=\{a\in A:d_a=0\}$. O código os suporta, mas a base atual não contém nenhum. |
| $K$ | Conjunto de equipes ou recursos cadastrados. |
| $T$ | Dias disponíveis: $T=\{0,1,\ldots,H-1\}$. |
| $T_a$ | Dias em que a atividade $a$ pode começar e ainda ser entregue dentro do horizonte. |
| $P$ | Conjunto de vínculos de precedência. Cada vínculo $e$ informa predecessora $i$, sucessora $j$, tipo e espera. |
| $P^{TI},P^{II},P^{TT},P^{IT}$ | Subconjuntos de vínculos, separados por tipo. |

Usaremos $a$ para uma atividade, $k$ para uma equipe, $t$ para o dia observado e $\tau$ para um possível dia de início. Os índices $i$ e $j$ identificam as duas atividades de um vínculo.

## 2. Parâmetros: informações que entram prontas

| Símbolo | Informação | Efeito no modelo |
| --- | --- | --- |
| $d_a$ | Duração inteira e não negativa de $a$, em dias úteis. | Determina a entrega e a janela durante a qual a atividade fica aberta. |
| $R_k$ | Capacidade da equipe $k$, em atividades abertas simultaneamente. | Limita a sobreposição das atividades atribuídas à equipe. |
| $q_{ak}$ | Vale 1 se a equipe $k$ participa de $a$; vale 0 caso contrário. | Define quais capacidades a atividade utiliza. Pode valer 1 para várias equipes na mesma atividade. |
| $\ell_e$ | Espera ou defasagem declarada no vínculo $e$, em dias úteis. | Impõe o afastamento entre os inícios ou entregas envolvidos. Na base atual, os valores são não negativos. |
| $H$ | Horizonte de planejamento. Atualmente, $H=310$. | Limita os dias em que os inícios e as entregas podem ocorrer. |

Esses parâmetros não são decisões do solver. As capacidades atuais são estimadas pelos picos do cronograma normalizado, sem comprovar o máximo operacional das equipes. As durações são as declaradas na fonte e já incluem as pausas internas.

## 3. Variáveis de decisão

### 3.1. Escolha do dia de início

$$
x_{a\tau}=\begin{cases}
1, & \text{se a atividade }a\text{ começa no dia }\tau,\\
0, & \text{caso contrário.}
\end{cases}
\qquad a\in A,\;\tau\in T_a.
$$

$$
x_{a\tau}\in\{0,1\}.
$$

**Como influencia o cronograma:** escolher outro valor igual a 1 desloca o início da atividade e, com ele, sua entrega e sua ocupação das equipes. O modelo pode deslocar o intervalo inteiro, mas não escolher suas pausas internas separadamente.

Por exemplo, $x_{a,5}=1$ significa que $a$ começa no dia 5. A restrição de início único, apresentada adiante, impede escolher vários dias ou deixar a atividade sem início.

### 3.2. Prazo do projeto

$$
C_{\max}\in\mathbb{R}_{\geq0}.
$$

Essa variável representa um limite superior para o prazo das entregas. As restrições a obrigam a acompanhar a última entrega, e a minimização evita que ela fique maior do que o necessário.

**Como influencia o resultado:** é o valor que queremos reduzir. Não precisa ser declarado inteiro no código: em uma solução ótima, coincide com o maior dia inteiro de entrega mais um. A extração numérica ainda precisará respeitar as tolerâncias do solver.

## 4. Expressões derivadas: não são decisões independentes

O código não cria variáveis independentes para início e término. Ele calcula as expressões abaixo a partir de $x$.

### Início

$$
S_a=\sum_{\tau\in T_a}\tau x_{a\tau},\qquad a\in A.
$$

Como exatamente um início será escolhido, essa soma retorna o dia selecionado.

### Dia da entrega

$$
F_a=S_a+\max(d_a,1)-1,\qquad a\in A.
$$

Para duração positiva, isso equivale a $F_a=S_a+d_a-1$. Para um evento de duração zero, $F_a=S_a$.

### Término exclusivo para contar ocupação

$$
C_a=S_a+d_a,\qquad a\in A.
$$

Uma atividade positiva fica aberta nos dias que satisfazem $S_a\leq t<C_a$, equivalentes aos dias de $S_a$ até $F_a$, inclusive.

**Exemplo:** duração de três dias e início no dia 2 resultam em $S_a=2$, $F_a=4$ e $C_a=5$. A atividade ocupa os dias 2, 3 e 4. O número 5 é a fronteira após essa ocupação, não o dia da entrega.

No evento de duração zero, $S_a=F_a=C_a$. Não existe dia que satisfaça $S_a\leq t<C_a$, portanto não há ocupação de equipe.

O símbolo $C_a$ não deve ser confundido com $C_{\max}$: o primeiro é uma expressão de ocupação de uma atividade; o segundo é a variável do prazo do projeto.

## 5. Função objetivo

$$
\min C_{\max}.
$$

Queremos o menor prazo total. Essa função não procura automaticamente equilibrar equipes, reduzir custos ou diminuir a quantidade de atividades simultâneas. Dois cronogramas com o mesmo prazo podem ser igualmente bons para o objetivo atual.

## 6. Domínio dos inícios e horizonte

$$
T_a=\{0,1,\ldots,H-\max(d_a,1)\},\qquad a\in A.
$$

Na leitura dos dados, uma duração maior que $H$ é rejeitada. Para duração positiva, o último início permitido é $H-d_a$. Para duração zero, é $H-1$.

Essa escolha dos dias admissíveis impõe, junto com o início único:

$$
0\leq S_a,\qquad F_a\leq H-1,\qquad a\in A.
$$

**Efeito:** nenhuma entrega fica fora do intervalo de dias do cronograma. Não é necessário criar uma restrição adicional de horizonte no código, pois o limite já está embutido nos dias para os quais existe $x_{a\tau}$.

Com $H=310$, os dias vão de zero a 309. Uma atividade de dez dias pode começar, no máximo, no dia 300. Um evento de duração zero pode ocorrer até o dia 309.

O horizonte foi justificado pelo cronograma de referência viável de 310 dias. Ele limita a busca sem obrigar o resultado a durar 310 dias. Essa justificativa precisa ser revista se as regras ou os dados mudarem de modo a invalidar a referência.

## 7. Restrições de início único

$$
\sum_{\tau\in T_a}x_{a\tau}=1,\qquad a\in A.
$$

**Em palavras:** cada atividade, inclusive um evento de duração zero, deve ter exatamente um dia de início escolhido.

**Efeito:** todas as atividades do conjunto são obrigatórias. O modelo não pode omitir uma atividade para reduzir o prazo nem escolher dois inícios para a mesma atividade.

### Revisão conjunta: início único

**Regra do projeto:** cada atividade incluída deve ser programada uma única vez. Isso também vale para eventos de duração zero, que precisam de um dia definido para respeitar seus vínculos.

Na equação, fixamos uma atividade a e somamos suas variáveis de início em todos os dias admissíveis. Como cada variável só pode valer zero ou um, soma igual a um significa escolher exatamente um dia. O resultado é uma equação por atividade: 243 na base atual.

**Exemplo didático:** considere H=5 e uma atividade A de duração três. Esse exemplo não altera a configuração do projeto. Seus dias admissíveis são zero, um e dois; a equação é:

$$
x_{A,0}+x_{A,1}+x_{A,2}=1.
$$

| $x_{A,0}$ | $x_{A,1}$ | $x_{A,2}$ | Soma | Avaliação |
| ---: | ---: | ---: | ---: | --- |
| 1 | 0 | 0 | 1 | Permitido por esta restrição: começa no dia zero. |
| 0 | 1 | 0 | 1 | Permitido por esta restrição: começa no dia um. |
| 0 | 0 | 0 | 0 | Impedido: a atividade ficaria sem início. |
| 1 | 1 | 0 | 2 | Impedido: haveria dois inícios escolhidos. |
| 0,5 | 0,5 | 0 | 1 | Impedido pelo domínio binário, embora satisfaça a soma. |

No segundo caso, S=1, F=3 e C=4: a atividade fica aberta nos dias 1, 2 e 3. A duração determina a janela depois que o início foi escolhido.

**Por que usamos igualdade:** se fosse menor ou igual a um, o modelo poderia não programar a atividade. Se fosse maior ou igual a um, poderia escolher vários inícios. A igualdade combinada ao domínio binário representa a escolha única desejada.

**Conferência no código:** `adicionar_inicio_unico`, em `codigo/restricoes.py`, percorre cada atividade e adiciona a soma das suas variáveis igual a um. Em `codigo/variaveis.py`, essas variáveis são criadas com `cat="Binary"` e somente para os dias admissíveis. Os três componentes — domínio binário, dias admissíveis e igualdade — estão presentes.

**Interação com as outras regras:** um início aceito por essa equação ainda pode violar uma dependência ou a capacidade. Essas restrições atuarão em conjunto para selecionar os dias que atendem a todas elas. Não basta passar no início único para o cronograma inteiro ser viável.

**Conclusão da revisão lógica:** a equação é coerente com o escopo de atividades obrigatórias e corresponde à implementação atual. Não foi identificado ajuste necessário nessa família. Essa conclusão se baseia na leitura do código e no exemplo manual; não houve execução do solver nem conclusão da validação das demais famílias.

## 8. Restrições de dependência

Para cada vínculo $e$ entre predecessora $i$ e sucessora $j$, aplicamos a desigualdade correspondente ao seu tipo.

### 8.1. Término–início: TI

$$
S_j\geq F_i+\ell_e,\qquad e\in P^{TI}.
$$

A sucessora só pode começar a partir da entrega da predecessora mais a espera. Com espera zero, pode começar no próprio dia da entrega, conforme a decisão aprovada.

**Exemplo:** se $F_i=10$ e $\ell_e=2$, então $S_j\geq12$.

### 8.2. Início–início: II

$$
S_j\geq S_i+\ell_e,\qquad e\in P^{II}.
$$

Limita o início da sucessora em relação ao início da predecessora. Não exige que a predecessora tenha terminado.

### 8.3. Término–término: TT

$$
F_j\geq F_i+\ell_e,\qquad e\in P^{TT}.
$$

Limita a entrega da sucessora em relação à entrega da predecessora. A sucessora pode começar antes, desde que respeite a desigualdade e suas outras regras.

### 8.4. Início–término: IT

$$
F_j\geq S_i+\ell_e,\qquad e\in P^{IT}.
$$

A entrega da sucessora não pode ocorrer antes do início da predecessora mais a espera.

**Ponto importante para a interpretação:** II não obriga inícios iguais e TT não obriga entregas iguais. São desigualdades, não exigências de simultaneidade. A ordem é a declarada no vínculo; não deve ser deduzida apenas do nome da atividade.

Essas regras também valem para eventos, usando $F_a=S_a$ quando $d_a=0$.

### 8.5. Revisão conjunta: dependências

**Regra do projeto:** uma atividade deve respeitar todos os vínculos declarados para ela. O tipo do vínculo determina quais pontos do cronograma estão relacionados; o modelo não transforma todos os vínculos em uma fila de atividades completas.

Para ler a notação: i é a predecessora, j é a sucessora, S é o início, F é o dia da entrega e a defasagem é o valor declarado no vínculo. As duas letras indicam, nessa ordem, o ponto usado da predecessora e o ponto usado da sucessora.

**Exemplo manual comum aos quatro tipos:** A começa no dia 4, dura cinco dias e termina no dia 8. B dura quatro dias. A defasagem do vínculo é de dois dias. Avaliamos um tipo de vínculo por vez, considerando apenas a regra indicada na linha.

| Tipo | Substituição na equação | Exemplo permitido por esse vínculo | Exemplo impedido por esse vínculo |
| --- | --- | --- | --- |
| TI | $S_B\geq8+2=10$ | B começa em 10 e termina em 13. | B começa em 9 e termina em 12. |
| II | $S_B\geq4+2=6$ | B começa em 6 e termina em 9. | B começa em 5 e termina em 8. |
| TT | $F_B\geq8+2=10$ | B começa em 7 e termina em 10. | B começa em 6 e termina em 9. |
| IT | $F_B\geq4+2=6$ | B começa em 3 e termina em 6. | B começa em 2 e termina em 5. |

No caso IT, o exemplo permitido mostra que B pode começar antes de A. O vínculo limita a entrega de B em relação ao início de A. Se outras regras impedirem esse início, elas também precisarão ser respeitadas.

**Como contar a defasagem:** somamos seu valor diretamente ao índice do dia usado na equação. Na convenção aprovada, TI com entrega em 8 e defasagem zero libera início em 8; com defasagem dois, libera início em 10. A defasagem representa essa diferença entre índices; não se acrescenta automaticamente um dia extra. Essa convenção precisa acompanhar a descrição das equações no artigo.

**Quando existem várias predecessoras:** todos os vínculos são aplicados. Se dois vínculos TI exigem, respectivamente, início a partir dos dias 10 e 12, a sucessora só pode começar a partir de 12. O modelo não escolhe qual exigência atender. Para predecessoras todas TI:

$$
S_j\geq\max_{e=(i,j)\in P^{TI}}\{F_i+\ell_e\}.
$$

Essa expressão resume o efeito das desigualdades individuais quando há pelo menos um vínculo TI de entrada. O código mantém uma desigualdade por vínculo, preservando a linearidade. II, TT e IT também continuam obrigatórios quando presentes.

**Interação com a capacidade:** uma entrega de A no dia 8 pode liberar B no próprio dia 8 por TI sem espera. Se A e B usam a mesma equipe, ambas ocupam capacidade nesse dia. Se o limite não comportar as duas, B terá que começar depois, mesmo estando liberada pela precedência.

**Eventos de duração zero:** mantêm início e entrega no mesmo dia e podem participar de qualquer um dos quatro tipos. Eles não ocupam capacidade, mas seus vínculos continuam limitando o cronograma. A base R14 atual não contém esses eventos; o comportamento está previsto no código.

**Conferência no código:** `adicionar_precedencias`, em `codigo/restricoes.py`, percorre os registros, lê predecessora, sucessora, tipo e defasagem e cria exatamente a desigualdade correspondente. Tipo inválido gera erro. Na base atual, são 1008 restrições: 1003 TI, duas II, duas TT e uma IT.

**Conclusão da revisão lógica:** as quatro equações correspondem à implementação e à convenção de entrega inclusiva aprovada. Não foi identificado ajuste necessário nessa família pela leitura e pelos exemplos manuais. Isso não comprova que cada vínculo do mundo real foi extraído corretamente: as limitações dos agrupadores e os descartes da preparação continuam documentados. Nenhum código foi alterado nem solver executado nesta revisão.

## 9. Restrições de capacidade das equipes

$$
\sum_{a\in A^+}q_{ak}
\sum_{\substack{\tau\in T_a\\\tau\leq t\leq\tau+d_a-1}}
x_{a\tau}
\leq R_k,
\qquad k\in K,\;t\in T.
$$

Para entender a expressão:

1. Fixamos uma equipe $k$ e um dia $t$.
2. Para cada atividade, verificamos se o início escolhido faz com que ela esteja aberta nesse dia.
3. Contamos a atividade somente se $q_{ak}=1$, isto é, se a equipe participa dela.
4. A quantidade total não pode ultrapassar $R_k$.

**Efeito:** impede abrir mais atividades do que o limite da equipe permite. A capacidade é contada durante todo o intervalo, mesmo que a equipe alterne o esforço entre tarefas e existam pausas internas.

Uma atividade com duas ou mais equipes consome uma unidade de capacidade de cada uma ao mesmo tempo. Os eventos de duração zero ficam fora da soma, pois não possuem intervalo de ocupação.

**Exemplo:** A ocupa os dias 2, 3 e 4; B ocupa os dias 4 e 5. Se pertencem à mesma equipe, ambas contam no dia 4. A precedência TI com espera zero pode permitir esse início de B, mas capacidade igual a um impede a sobreposição. Capacidade igual a dois permite esse caso, se não houver outra restrição.

Os rótulos de tipo ou disciplina não criam uma regra especial de capacidade. O consumo depende da duração e das equipes registradas em `papel`.

### 9.1. Revisão conjunta: capacidade das equipes

**Regra do projeto:** em cada dia, uma equipe só pode manter abertas até R atividades. Esse limite mede atividades simultâneas, não pessoas, horas de trabalho ou dedicação exclusiva. A janela inclui as pausas internas já incorporadas à duração.

**Como ler a equação:** a soma interna verifica se o início escolhido mantém a atividade aberta no dia observado. Para uma atividade positiva:

$$
\tau\leq t\leq\tau+d_a-1
\quad\Longleftrightarrow\quad
t-d_a+1\leq\tau\leq t.
$$

É essa segunda forma que aparece no código. O domínio admissível de cada atividade limita quais inícios realmente existem.

Para explicar a contagem, podemos chamar a soma interna de ocupação:

$$
u_{at}=\begin{cases}
\displaystyle\sum_{\substack{\tau\in T_a\\\tau\leq t\leq\tau+d_a-1}}x_{a\tau}, & a\in A^+,\\
0, & a\in A^0.
\end{cases}
$$

Então a mesma regra pode ser lida como:

$$
\sum_{a\in A}q_{ak}u_{at}\leq R_k,
\qquad k\in K,\;t\in T.
$$

**u é apenas uma expressão auxiliar para explicar a soma, não uma nova variável de decisão.** Com o início único binário, vale um quando a atividade positiva está aberta e zero nos outros dias. O código faz a soma diretamente, sem criar variáveis u.

**Exemplo manual:** considere três atividades da mesma equipe, com capacidade dois. A começa em 2 e dura três dias; B e C começam em 4 e duram dois dias cada.

| Atividade aberta | Dia 2 | Dia 3 | Dia 4 | Dia 5 |
| --- | ---: | ---: | ---: | ---: |
| A | 1 | 1 | 1 | 0 |
| B | 0 | 0 | 1 | 1 |
| C | 0 | 0 | 1 | 1 |
| Total | 1 | 1 | 3 | 2 |

O cronograma viola a capacidade no dia 4, porque três atividades ultrapassam o limite dois. A e B, sozinhas, atenderiam ao limite. Uma possibilidade para resolver a sobreposição é deslocar C para os dias 5 e 6: o pico passa a dois. Esse deslocamento também precisará respeitar os vínculos e o horizonte; a capacidade, sozinha, não garante viabilidade global.

**Entrega e novo início no mesmo dia:** A termina em 4 e B começa em 4. As duas contam nesse dia. A deixa de ocupar a equipe no dia 5. A liberação por precedência TI não elimina essa contagem compartilhada.

**Atividade com várias equipes:** cada papel listado recebe uma unidade adicional durante toda a janela positiva. Usando as capacidades atuais de análise de produto (sete) e análise de engenharia (quatro), considere uma atividade X que exige ambas:

| Equipe | Outras atividades abertas no dia | X acrescenta | Total | Capacidade | Avaliação |
| --- | ---: | ---: | ---: | ---: | --- |
| Análise de produto | 6 | 1 | 7 | 7 | Atende. |
| Análise de engenharia | 4 | 1 | 5 | 4 | Viola. |

X não pode começar nesse dia, pois todas as equipes precisam ter espaço simultaneamente. O modelo não pode transferir sua responsabilidade, retirar uma equipe ou alterar a duração. Ele precisa encontrar outros inícios para X ou para atividades que disputam os mesmos recursos.

**Eventos e reuniões:** duração zero não ocupa capacidade, mesmo se houver equipe cadastrada. Uma reunião de três ou cinco dias, como as incluídas na base, possui duração positiva e ocupa todas as equipes listadas. Ser do tipo GATE não isenta uma atividade da capacidade.

**Conferência no código:** `adicionar_capacidade`, em `codigo/restricoes.py`, percorre as equipes e todos os dias de zero a H−1, seleciona somente atividades positivas da equipe e soma os inícios entre `t-duracao+1` e t. O teste `if tau in variaveis.x[a]` preserva apenas os inícios admissíveis. A comparação final usa a capacidade cadastrada da equipe. São 39 × 310 = 12090 restrições na base atual.

**Conclusão da revisão lógica:** a soma corresponde à ocupação inclusiva aprovada, considera simultaneamente todos os papéis e exclui corretamente eventos de duração zero. Não foi identificado ajuste necessário nessa família pela leitura do código e pelos exemplos manuais. Isso não demonstra a capacidade operacional real: os parâmetros continuam sendo estimativas pelos picos da referência normalizada. Nenhum código foi alterado nem solver executado nesta revisão.

## 10. Restrições que vinculam o prazo às entregas

$$
C_{\max}\geq F_a+1,\qquad a\in A.
$$

**Em palavras:** o prazo deve cobrir a entrega de toda atividade. Somamos um porque os dias começam em zero: entrega no dia 5 corresponde a seis dias da escala.

Em uma solução ótima:

$$
C_{\max}=\max_{a\in A}\{F_a+1\}.
$$

A igualdade acima é consequência da minimização e não uma restrição adicional criada no código. Um valor maior apenas aumentaria o objetivo sem necessidade.

A regra também conta corretamente um evento que seja a última entrega, sem transformar sua duração em um dia de trabalho. O código não impõe separadamente $C_{\max}\leq H$; os domínios das entregas e a minimização garantem um ótimo de, no máximo, $H$ quando o modelo é viável.

### 10.1. Revisão conjunta: prazo final e objetivo

**Regra do projeto:** o prazo precisa alcançar todas as entregas. Quando uma atividade é deslocada para depois, o prazo deve acompanhá-la se ela passar a ser a última entrega.

**Exemplo manual:** considere as entregas fixadas abaixo e avalie somente esta família de restrições.

| Atividade | Dia da entrega F | Restrição para o prazo |
| --- | ---: | --- |
| A | 4 | $C_{\max}\geq5$ |
| B | 7 | $C_{\max}\geq8$ |
| C | 5 | $C_{\max}\geq6$ |

As três desigualdades precisam ser atendidas. Portanto, o menor prazo compatível com essas entregas é oito dias, correspondentes aos índices de zero a sete.

| Valor de Cmax | Avaliação para essas entregas |
| ---: | --- |
| 7 | Impedido: não atende à entrega de B. |
| 8 | Permitido e é o menor valor para esse cronograma fixo. |
| 10 | Atende às desigualdades, mas é maior que o necessário e a minimização favorece oito para o mesmo cronograma. |

O solver também decide os inícios. Se conseguir antecipar as últimas entregas sem violar as outras restrições, poderá reduzir o prazo. Obter oito para as entregas do exemplo não prova que oito seja o ótimo global do problema: outros cronogramas ainda poderiam existir.

**Por que há uma restrição por atividade:** assim toda entrega pode determinar o prazo final. Escolher previamente apenas uma tarefa como a última poderia deixar de contar outra que terminasse depois. Na base atual, são 243 desigualdades de prazo.

**Por que somamos um:** o prazo é medido desde a origem zero da escala, incluindo o último dia de entrega. Não é a diferença entre a maior entrega e o menor início. A referência termina no índice 309 e corresponde a 310 dias.

**Evento de duração zero:** se um evento terminal acontecer no dia 9, F=9 e C=9, mas o prazo deverá ser pelo menos dez dias da escala. A restrição usa F+1, preservando a contagem aprovada. O evento não ocupa equipe; o prazo registra quando ocorre a última entrega.

**Papel da função objetivo:** as desigualdades garantem que Cmax cubra as entregas. Minimizar Cmax faz o modelo procurar o menor prazo viável. Sem essa ligação, uma variável de prazo isolada não acompanharia o cronograma; somente as desigualdades, sem minimizar, também permitiriam valores maiores que o necessário.

**Interação com as demais regras:** o objetivo não autoriza omitir atividades, antecipar entregas além do permitido pelas durações, desrespeitar vínculos ou ultrapassar capacidades. A busca por prazo menor acontece dentro do conjunto de cronogramas que atendem simultaneamente a todas as restrições. Custos e equilíbrio de equipes não são objetivos adicionais.

**Conferência no código:** em `codigo/variaveis.py`, Cmax é uma variável contínua não negativa. Em `definir_prazo_e_objetivo`, de `codigo/restricoes.py`, a primeira linha define a minimização dessa variável e o laço cria `Cmax >= F[a] + 1` para cada atividade. O sentido de minimização é definido na criação do problema em `codigo/resolucao.py`. A implementação corresponde à formulação.

**Conclusão da revisão lógica:** a ligação entre prazo e entregas e a função objetivo estão coerentes com as decisões aprovadas. Não foi identificado ajuste necessário nessa família pela leitura e pelo exemplo manual. Com isso, as quatro famílias foram revisadas logicamente. Ainda precisamos conferir a extração e a aceitação dos resultados, distinguir solução viável de ótimo comprovado e realizar a validação numérica. Para um cronograma extraído, o prazo efetivo pode ser calculado diretamente por maior F+1; uma declaração de ótimo global depende da evidência do solver. Nenhum código foi alterado nem solver executado nesta revisão.

## 11. Resumo das quatro famílias

| Família | O que garante | Função no código |
| --- | --- | --- |
| Início único | Uma escolha de início para cada atividade obrigatória. | `adicionar_inicio_unico` |
| Dependências | Respeito aos quatro tipos de vínculo e às esperas. | `adicionar_precedencias` |
| Capacidade | Limite de atividades abertas por equipe e dia. | `adicionar_capacidade` |
| Prazo final | O prazo cobre todas as entregas; a função objetivo o minimiza. | `definir_prazo_e_objetivo` |

As quatro funções ficam em `codigo/restricoes.py`. As variáveis e seus domínios ficam em `codigo/variaveis.py`. As expressões S, F e C são definições; a função objetivo e os domínios devem ser apresentados separadamente das quatro famílias de restrições.

## 12. Tamanho da formulação na base atual

Com 243 atividades, 39 recursos e horizonte de 310 dias, os domínios do código resultam em **72.381 variáveis binárias de início**, além da variável contínua $C_{\max}$. Essa contagem foi obtida pelos domínios, sem executar o solver.

| Família | Quantidade de restrições |
| --- | ---: |
| Início único | 243 |
| Dependências | 1008: 1003 TI, 2 II, 2 TT e 1 IT |
| Capacidade por equipe e dia | 39 × 310 = 12090 |
| Prazo por atividade | 243 |
| Total dessas quatro famílias | 13584 |

Os limites e a natureza binária das variáveis não foram contados como linhas adicionais nessa tabela. Aumentar H cria mais possibilidades de início e mais dias de verificação de capacidade; por isso sua escolha influencia o tamanho do modelo.

## 13. Hipóteses e limites que precisam acompanhar as equações

- O planejamento começa do início; percentuais concluídos não fixam o cronograma.
- As durações incluem pausas e não medem esforço diário de pessoas.
- O modelo mantém as equipes atribuídas e suas capacidades constantes no cenário.
- A escala é normalizada em dias úteis e não reconstrói datas civis ou calendários específicos por equipe.
- Os vínculos são os da base preparada e ajustada; não há variável que libere a ordem dos blocos.
- As limitações de extração, dos agrupadores fechados e dos vínculos removidos na preparação permanecem, mesmo que as equações sejam atendidas.
- As tarefas de execução de obra foram retiradas. A apresentação dos projetos à obra permanece como entrega de projeto.
- Custos, contratação, mudança de duração e número de revisões como decisão ficam fora da formulação atual.

## 14. Por que a formulação é linear

O modelo é de programação linear inteira mista: x é binária e Cmax é contínua. As somas e desigualdades usam coeficientes constantes e expressões lineares dessas variáveis.

O termo $\max(d_a,1)$ não introduz uma decisão não linear, pois a duração é um parâmetro conhecido. A expressão com o máximo das entregas descreve o valor ótimo; no código, ela é representada pelas desigualdades de prazo e pela minimização de Cmax.

Este documento será atualizado ao revisarmos cada família. Registrar uma equação já implementada não significa aprovar automaticamente uma nova hipótese nem concluir a validação numérica da solução.
