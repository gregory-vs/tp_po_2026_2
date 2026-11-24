# Análise de sensibilidade: o que limita o prazo e o que vale mudar

Atualizado em 23/11/2026, por Henrique (Jascolka). Os números deste documento vêm de `codigo/sensibilidade.py`, que não chama o CBC e não altera os CSVs. O registro completo da rodada está em `resultados/sensibilidade-20261124T002034Z.json` (a rodada `sensibilidade-20261123T131548Z.json` tem os mesmos números das seções 1 a 4, sem as seções 4A a 4F; a de 23/11 às 19h foi substituída por esta, que só acrescenta o cenário sem a T026 da seção 4C).

> **Atualização de 23/11, noite.** A conferência no R14 original (seção 4F) mostrou que a maioria das atividades que começam tarde depende de entregas do estudo preliminar de arquitetura que não estão na base. Por isso o **número realista é 285 dias (ganho de 25 dias, 8,1%)**, e 187 é o limite da reordenação se as disciplinas fossem liberadas no início. As seções 1 a 4 continuam corretas para o modelo com largadas livres. Como apresentar isso no artigo ainda precisa ser combinado com o grupo.

Este documento traz **resultados verificados** (seções 1 a 5, incluindo 4A a 4F) e **interpretações e propostas para discutir no grupo** (seções 6 e 7). As propostas não são decisões tomadas.

---

## 1. O ótimo da base completa é 187 dias

| Item | Valor |
| --- | --- |
| Referência praticada (normalizada) | 310 dias |
| Melhor resultado do CBC (36 min, sem prova) | 307 dias |
| Limite inferior (caminho crítico, sem equipes) | 187 dias |
| **Cronograma encontrado pela heurística** | **187 dias** |
| Validação pelo verificador do repo (`validacao.py`) | aprovada, zero erros |
| **Redução sobre a referência** | **123 dias (39,7%)** |

**Por que 187 é ótimo, e não só "um resultado bom":**

1. **187 é um limite inferior.** É o comprimento da maior cadeia de vínculos da rede, calculado como se toda equipe tivesse capacidade infinita. Com capacidade limitada o prazo só pode ficar igual ou maior. O próprio CBC chegou a esse limite (`Lower bound: 187` nos logs das duas rodadas).
2. **Existe um cronograma viável de 187 dias.** A heurística montou um cronograma que respeita os 1.008 vínculos e as 39 capacidades, conferido pelo mesmo `verificar_solucao` que aprova as soluções do CBC.
3. Se existe um cronograma viável igual ao limite inferior, nenhum outro pode ser menor. **O gap é zero.**

Os inícios desse cronograma estão no campo `inicios` do JSON da rodada.

### Por que o CBC não achou

O problema não estava no modelo nem na base, e sim no método de solução. A formulação indexada no tempo tem 72.381 variáveis binárias. O CBC gastou quase todo o tempo no nó raiz (relaxação, cortes e heurísticas internas) e explorou poucos nós da árvore. Partindo do cronograma praticado (310), ele só encontrou melhorias pequenas (308 e 307).

A heurística é o **esquema serial de geração de cronogramas** (*serial SGS*), método clássico do RCPSP. As atividades são escolhidas uma a uma por uma regra de prioridade (aqui, o menor início mais tarde do caminho crítico, com pequenas perturbações aleatórias de semente fixa). Cada uma é posta no primeiro dia em que os vínculos e as equipes permitem. O resultado é sempre viável. Quando o prazo coincide com o limite inferior, fica provado que é ótimo.

Para o artigo, isso conversa com a revisão de literatura: as heurísticas de regra de prioridade são o ponto de partida padrão do RCPSP justamente porque modelos exatos indexados no tempo não escalam bem. Aqui, a combinação "limite inferior + heurística" resolveu o que o solver sozinho não fechou em 36 minutos.

---

## 2. O que limita o prazo: a cadeia de vínculos, não as equipes

Como o ótimo **com** equipes (187) é igual ao ótimo **sem** limite de equipes (187), **a capacidade das equipes não segura o prazo**. Quem define os 187 dias é a sequência obrigatória de entregas e análises.

Na linguagem de dualidade e folgas complementares: a restrição de capacidade não está ativa no ótimo, então o "preço-sombra" dela é zero. Aumentar equipe não reduz prazo. As restrições de precedência da cadeia crítica é que estão ativas, e cada dia a menos nelas vale um dia a menos no projeto.

### A cadeia que define o prazo

São 21 atividades encadeadas, quase todas de **interiores (ARI)**, do início até o fim do anteprojeto:

| Trecho | O que é | Equipes |
| --- | --- | --- |
| Geral (dias 0–47) | 4 emissões de interiores intercaladas com 2 análises do cliente | `PROJ-INT`, `ANL-PRODUTO` |
| EP (dias 47–99) | 4 emissões (R00, R01, R02) e 3 análises, incluindo uma análise de 22 dias | `PROJ-INT`, `ANL-PRODUTO` |
| AP (dias 99–163) | 5 emissões por zona e 1 análise | `PROJ-INT`, `ANL-PRODUTO` |
| Final (dias 163–187) | luminotécnico e análise da consultoria ambiental | `PROJ-LUM`, `CONS-AMBIENTAL` |

Na cadeia somam-se ~139 dias de **emissão** e ~63 dias de **análise**. A soma passa de 187 porque, na convenção do modelo, uma atividade TI com lag zero pode começar no mesmo dia em que a anterior entrega (seção 8).

### Folgas

| Folga total da atividade | Atividades |
| --- | --- |
| zero (crítica) | 29 de 243 |
| até 5 dias | 51 |
| até 10 dias | 83 |
| até 20 dias | 128 |

Há muitas atividades **quase críticas**. Das 51 com folga de até 5 dias, 26 são de interiores e 15 de arquitetura (ARQ). Por isso o ganho de encurtar uma única disciplina acaba rápido: logo atrás de interiores vem uma cadeia de arquitetura do anteprojeto (emissões de ARQ, fundação e análises), que vira a crítica.

---

## 3. Cenários de equipes (capacidade)

| Cenário | Prazo | Variação | Ótimo comprovado |
| --- | --- | --- | --- |
| Todas as equipes +1 | 187 | 0 | sim |
| Todas as equipes −1 (mínimo 1) | ≤ 194 | até +7 | não |
| Todas as equipes com capacidade 1 | ≤ 614 | até +427 | não |
| −1 só em `PROJ-INT` (interiores) | ≤ 189 | até +2 | não |
| −1 só em `ANL-ENGENHARIA`, `PROJ-HID` ou `PROJ-PSG` | ≤ 188 | até +1 | não |
| −1 em qualquer outra equipe com capacidade > 1 | 187 | 0 | sim |

**Leitura:**
- **Contratar mais gente não reduz o prazo.** Com +1 em todas as equipes, o prazo fica em 187.
- **As equipes atuais têm pouca sobra, mas têm sobra.** Tirar uma frente de todas custa no máximo 7 dias. A capacidade de cada equipe foi estimada pelo pico do cronograma praticado, e o ótimo usa essa capacidade quase inteira sem ser travado por ela.
- **Trabalhar uma atividade por vez em cada equipe é desastroso** (≈ 614 dias). Ter frentes em paralelo é o que segura o prazo nos 187.

Quando o cenário diz "não" em ótimo comprovado, o número é um **limite superior**: existe cronograma com esse prazo, mas pode existir um menor. Isso não muda a leitura, porque a variação já é pequena.

---

## 4. Cenários de duração (tempo de cada atividade)

As durações foram reduzidas por percentual e arredondadas para cima, sempre com no mínimo 1 dia.

| Cenário | Prazo | Variação | Ótimo comprovado |
| --- | --- | --- | --- |
| Análise do cliente 10% mais rápida | 184 | −3 | sim |
| Análise do cliente 20% mais rápida | 182 | −5 | sim |
| Análise do cliente 50% mais rápida | 181 | −6 | sim |
| Análise do cliente em até 10 dias (SLA) | 183 | −4 | sim |
| Análise do cliente em até 5 dias (SLA) | 183 | −4 | sim |
| Análise do cliente em até 3 dias (SLA) | 181 | −6 | sim |
| **Emissão 10% mais rápida** | **177** | **−10** | sim |
| **Emissão 20% mais rápida** | **≤ 165** | **−22** | não (LB 163) |
| Emissão 30% mais rápida | ≤ 162 | −25 | não (LB 155) |
| Emissão 50% mais rápida | ≤ 152 | −35 | não (LB 144) |
| Tudo 10% mais rápido | 173 | −14 | sim |
| Tudo 20% mais rápido | 149 | −38 | sim |
| Tudo 30% mais rápido | 133 | −54 | sim |
| Interiores (ARI) 20% mais rápido | 183 | −4 | sim |
| Qualquer outra disciplina 20% mais rápida | 187 ou 188 | 0 ou +1 | — |

**Leitura:**
- **A alavanca principal é o tempo de emissão do projetista**, não o tempo de análise do cliente. Emitir 10% mais rápido vale 10 dias. Analisar 50% mais rápido vale 6.
- **Encurtar só uma disciplina rende pouco.** Interiores 20% mais rápido dá só 4 dias, porque a cadeia de arquitetura do anteprojeto está logo atrás (seção 2). As outras disciplinas sozinhas não mudam nada: não estão na cadeia crítica. O +1 em PSG é efeito da heurística, não piora real, porque o limite inferior continua 187.
- **Melhoria geral rende muito.** Tudo 20% mais rápido cai para 149 dias. O ganho vem de encurtar várias cadeias ao mesmo tempo, e não só a crítica.

### Marginal: "preço-sombra" de cada atividade da cadeia

Tirando 1 dia de cada atividade da cadeia, uma por vez, 17 das 21 reduzem o prazo em 1 dia. As outras 4 não reduzem nada, porque outra cadeia de mesmo comprimento as acompanha. O preço-sombra é 1 dia de projeto por dia de atividade, até a cadeia deixar de ser a única crítica. A lista está em `marginal_cadeia` no JSON.

---

## 4A. De onde vêm os 123 dias: esperas no cronograma praticado

Para cada atividade do praticado, a **espera** é quantos dias ela começou depois do que os vínculos permitiam, dadas as datas praticadas das predecessoras. O caminho que fecha os 310 dias do praticado é este:

| Atividade | Equipe | Início praticado | Duração | Espera |
| --- | --- | ---: | ---: | ---: |
| T072 Emissão PCI, AP, zona 4 | `PROJ-PCI` | 75 | 28 | **75** |
| T135 a T139 Emissões ARQ, AP, 5 zonas em sequência | `PROJ-ARQ` | 110–187 | 96 no total | 13 |
| T154 Análise ARQ, AP | `ANL-PRODUTO` | 209 | 5 | 3 |
| T160 Emissão ARQ, AP, R01 | `PROJ-ARQ` | 214 | 5 | 1 |
| T211 Emissão fundação, AP | `PROJ-FUN`, `PROJ-COM` | 220 | 20 | 2 |
| T244 Compatibilização (clash) | `ANL-ENGENHARIA` | 270 | 15 | **31** |
| T245 Análise da compatibilização | `ANL-PRODUTO` | 290 | 10 | 6 |
| T247 Retrabalho da compatibilização | todas | 300 | 10 | 1 |
| **Soma** | | | | **132** |

**Leitura:** no caminho que define o prazo praticado, 132 dias são de espera e não de trabalho. Desses, **75 são na largada** (a primeira emissão do caminho só começou no dia 75, sem nenhuma predecessora na base) e **31 são antes da compatibilização**. Esses 31 dias são aparentes: a compatibilização espera o R01 de estrutura de todas as zonas, mas na base só a primeira zona está ligada a ela (ver 6.2, pergunta 5). A otimização recupera essas esperas e, de quebra, troca o caminho crítico: no praticado ele passa por arquitetura e compatibilização; no ótimo, por interiores.

Somando todas as atividades, as esperas se concentram em ARQ (970 dias-atividade), GERAL (537) e acústica (382). O valor completo por disciplina está em `praticado_espera_por_disciplina` no JSON.

## 4B. Largadas tardias: a hipótese que mais pesa no resultado

O modelo deixa toda atividade sem predecessora começar no dia 0. No praticado, **27 atividades sem predecessora começaram depois do dia 0**. Se essa espera tinha motivo real que não está na base (contrato da disciplina ainda não assinado, briefing não liberado, decisão do cliente, vínculo perdido na limpeza dos dados), o ótimo de 187 é otimista.

Prendendo cada uma na data praticada, uma por vez (efeito no limite inferior):

| Atividade | Equipe | Início praticado | Efeito se presa nessa data |
| --- | --- | ---: | ---: |
| T141 a T144 Emissões ARQ, **EP**, zonas 1 a 4 (52 dias cada) | `PROJ-ARQ` | 120 | **+98** |
| T277 Emissão GERAL (8) | `PROJ-ARQ` | 220 | +88 |
| T007 Emissão ARI, GERAL (início da cadeia de interiores) | `PROJ-INT` | 75 | +75 |
| T072 Emissão PCI, AP, zona 4 | `PROJ-PCI` | 75 | +71 |
| T054, T055 Análises ARQ, AP, zona 1 | `ANL-PRODUTO`, `ANL-ENGENHARIA` | 100 | +67 |
| T066, T067 Emissões fundação e contenção, AP | `PROJ-FUN`, `PROJ-COM` | 75 | +66 |
| outras 9 (ELE, CLI, PISC, AUT, GAS, HID, análise geral) | | 41–141 | +26 a +56 |
| 8 restantes | | | 0 |

| Cenário | Prazo | Variação | Ótimo comprovado |
| --- | ---: | ---: | --- |
| Todas as 27 presas na data praticada (cenário conservador) | 285 | +98 | sim |
| Só as 4 emissões de ARQ do EP presas | 285 | +98 | sim |
| Só T007 presa (dia 75) | 262 | +75 | sim |
| Só T072 presa (dia 75) | 258 | +71 | sim |

**Leitura:**
- **O ganho real fica entre 25 dias (8%) e 123 dias (40%)**, dependendo de as largadas tardias terem ou não motivo real. Os 25 dias do cenário conservador vêm só da reordenação, mantendo as datas de largada do praticado.
- Quem decide onde fica o ganho dentro dessa faixa são **as 4 emissões de arquitetura do EP**: sozinhas, elas levam o ótimo a 285. Tem algo estranho nelas. São emissões de EP com 52 dias cada, que começaram no dia 120, **depois** das emissões de arquitetura do AP (dia 110), e alimentam a CXO. Precisa da confirmação de quem conhece o processo: é um segundo EP (outro produto, outra torre)? Elas dependiam de alguma coisa? O vínculo se perdeu entre os 37 retirados por incompatibilidade com as datas?
- Pergunta provável na arguição: "por que interiores pode começar no dia 0 se no real começou no 75?". A resposta honesta é essa faixa.

## 4C. Medidas pontuais nas duas cadeias críticas

Atrás da cadeia de interiores (187) existe uma **segunda cadeia, de arquitetura do AP, com 183 dias**: PCI (T072) → 5 emissões de ARQ por zona em sequência (T135 a T139, 96 dias somados) → análise → R01 → fundação → análise de engenharia → emissão e análise finais de ARQ. É a mesma cadeia que fechou o praticado (seção 4A). Por isso qualquer melhoria só em interiores para em −4.

| Cenário | Prazo | Variação | Ótimo comprovado |
| --- | ---: | ---: | --- |
| Zonas do AP de interiores em paralelo (T114 a T117) | 183 | −4 | sim |
| Zonas do AP de arquitetura em paralelo (T135 a T139) | 187 | 0 | sim |
| Zonas do AP em paralelo nas duas disciplinas | ≤ 179 | −8 | não (LB 178) |
| Análise T026 do EP de interiores em 10 dias (era 22) | 183 | −4 | sim |
| Emissão R01 do AP de interiores T166 em 10 dias (era 20) | 183 | −4 | sim |
| Zonas em paralelo nas duas + T166 em 10 dias | ≤ 179 | −8 | não (LB 178) |
| Zonas em paralelo nas duas + T026 e T166 em 10 dias² | 172 | −15 | sim |
| Sem a R02 do EP de interiores (T027) e sua análise (T030)¹ | 183 | −4 | sim |
| Sem nenhuma das 4 emissões R02 da base¹ | 187 | 0 | sim |

¹ Rodado só no script exploratório, não está no `sensibilidade.py`: retira a atividade e liga as predecessoras dela direto às sucessoras.

² **Limite superior, não medida.** A T026 (análise da consultoria wellness, 22 dias) é uma janela de decisão do cliente específica deste empreendimento (seção 6.2). Combinado com o Henrique em 23/11: ela não entra como medida proposta; o −15 serve só como teto do ganho do pacote.

"Em paralelo" quer dizer: retirar os vínculos entre zonas consecutivas e dar a cada zona as mesmas predecessoras da primeira. Isso só faz sentido se a ordem entre as zonas não for técnica.

**Leitura:** uma medida sozinha rende no máximo 4 dias, porque a outra cadeia assume. Para passar disso é preciso **atacar as duas cadeias juntas**. O pacote "zonas em paralelo + encurtar a R01 de 20 dias" dá 8 dias. Encurtar também a análise de 22 dias da consultoria levaria a 15, mas isso é só limite superior (nota 2).

## 4D. Combinações de medidas gerais

| Cenário | Prazo | Variação | Ótimo comprovado |
| --- | ---: | ---: | --- |
| Emissão de ARI e ARQ 20% mais rápida | ≤ 172 | −15 | não (LB 169) |
| Emissão de ARI e ARQ 20% + SLA de análise de 5 dias | 161 | −26 | sim |
| Emissão de todas as disciplinas 20% mais rápida (seção 4) | ≤ 165 | −22 | não (LB 163) |

**Leitura:** acelerar a emissão só de interiores e arquitetura entrega quase o mesmo que acelerar todas as disciplinas (−15 contra −22). Somar o SLA de análise, que sozinho dava −4, rende mais 8 a 11 dias nessa combinação, porque com as emissões mais curtas as análises passam a pesar mais na cadeia.

## 4E. Comparação entre métodos

| Instância | Atividades | Limite sem equipes | Heurística | CBC (PLI indexada no tempo) |
| --- | ---: | ---: | ---: | --- |
| Pequena | 12 | 44 | 45 | **45, ótimo comprovado, ~1–6 s** |
| Completa | 243 | 187 | **187, ótimo comprovado, ~10 s** | 307, parou por tempo em 36 min, gap 39% |

Registros: `resultados/20261123T155939347642Z-be325763.json` (CBC na pequena) e `resultados/20261123T034835057589Z-8a258fda.json` (CBC na completa).

**Leitura:** os dois métodos se completam. Na pequena, a capacidade segura o prazo (45 contra 44 sem equipes), a heurística não consegue provar nada sozinha e o CBC prova o ótimo. Na completa acontece o contrário: o CBC não dá conta do tamanho, e a heurística prova o ótimo porque bate no limite inferior. A instância média é um recorte histórico e a auditoria bloqueia o uso dela; não foi rodada.

## 4F. Conferência no R14 e base com liberações (285 dias)

**O que o cronograma original mostra.** A conferência foi feita no PDF do R14, que fica fora do repositório. Lá, as emissões R00 do AP de fundação, contenção, PCI, elétrica, gás, SMOP, climatização e acústica, assim como os mapas de esquadrias, têm predecessoras dentro do bloco do **estudo preliminar**. Esse bloco está recolhido no PDF e, por isso, não entrou na base. Na base não há nenhuma atividade de arquitetura antes do dia 75, que corresponde aproximadamente a 04/05/2026 (o dia 0 corresponde a 19/01/2026 e o dia 120 a 06/07/2026). As largadas tardias são, portanto, em grande parte, **espera pela arquitetura**, e não folga do planejamento.

**As "emissões ARQ EP" T141 a T144 são os mapas de esquadrias** das três torres e do embasamento. No original, ficam num grupo nomeado como EP, mas posicionado dentro do AP inicial de arquitetura. Têm 52 dias cada e liberam a análise do mapa e o AP R00 de caixilhos (CXO) de cada torre. O rótulo EP vem do nome no cronograma original.

**Base com liberações.** As 27 largadas tardias ficam presas na data praticada, como substitutas das predecessoras ausentes. O resultado é **285 dias, com ótimo comprovado** (LB = UB = 285) e cronograma validado: um ganho de **25 dias (8,1%)** sobre 310. É uma estimativa conservadora: se as entregas ausentes terminaram antes da data praticada, a liberação real era mais cedo.

**Cadeia que define o prazo nessa base**, que é o ciclo de AP da arquitetura descrito na seção 6.2:

| Trecho | Atividades | Dias |
| --- | --- | ---: |
| Mapas de esquadrias (liberados no dia 120) | T141 | 52 |
| Análise do mapa ("liberar caixilhos") | T145 | 5 |
| AP R00 de caixilhos, por torre | T238 | 30 |
| ARQ emite o AP de cada torre e do embasamento, um após o outro, depois de receber as disciplinas | T255 → T256 → T257 → T258 | 20 + 20 + 20 + 15 |
| Análise final da arquitetura | T261 | 10 |

**Cenários sobre a base de 285** (variação em relação a 285; todos com ótimo comprovado):

| Cenário | Prazo | Variação |
| --- | ---: | ---: |
| Todas as equipes +1 | 285 | 0 |
| Todas as equipes −1 | 285 | 0 |
| Análise do cliente 10% / 50% mais rápida | 285 / 283 | 0 / −2 |
| Análise do cliente em até 5 dias (SLA) | 285 | 0 |
| **Emissão 10% mais rápida** | **270** | **−15** |
| Emissão 20% / 30% / 50% mais rápida | 264 / 259 / 248 | −21 / −26 / −37 |
| Tudo 10% / 20% mais rápido | 270 / 264 | −15 / −21 |
| ARQ 20% mais rápida | 275 | −10 |
| Caixilhos (CXO) 20% mais rápida | 279 | −6 |
| Interiores 20% mais rápida | 285 | 0 |
| Mapas de esquadrias 10% / 20% mais rápidos | 280 / 275 | −5 / −10 |
| Torres do AP final de ARQ em paralelo (T255 a T258) | 275 | −10 |
| Emissão de ARQ e CXO 10% mais rápida | 275 | −10 |

**Leitura:**
- As conclusões principais das seções 3 e 4 se mantêm: **equipes não seguram o prazo** e **a alavanca é o tempo de emissão**, não o de análise do cliente.
- O que muda é **onde agir**. Na base de 285, a cadeia é toda de arquitetura e caixilhos. Interiores sai da cadeia.
- Com a cadeia dominada pelo ciclo de AP da arquitetura, encurtar o mapa de esquadrias, os caixilhos ou as emissões finais de ARQ por torre tem efeito direto. A partir de −10, outra cadeia de mesmo comprimento assume (275 aparece em quatro cenários diferentes).

---

## 5. Resumo numérico para o artigo e os slides

- Referência praticada: **310** dias.
- CBC, indexado no tempo, 36 min: **307** dias, sem prova (gap 39%).
- Heurística + limite inferior, ~10 s: **187** dias, **ótimo comprovado**. Ganho de **123 dias (39,7%)** com as mesmas atividades, durações, vínculos e equipes.
- O prazo é definido pela **cadeia de emissões e análises de interiores**, não pela capacidade das equipes.
- **+1 em todas as equipes: 0 dia.** **Emissão 10% mais rápida: −10 dias.** **Tudo 20% mais rápido: −38 dias.**
- No praticado, **132 dias** do caminho que fecha os 310 são espera, sendo **75 na largada**.
- **Base com liberações** (as 27 largadas tardias mantidas nas datas praticadas, porque dependem do estudo preliminar ausente da base): **285 dias**, ótimo comprovado, **ganho de 25 dias (8,1%)**. É o número realista. 187 é o limite com todas as disciplinas liberadas no início.
- Na base de 285: equipes ±1 = 0; emissão 10% mais rápida = −15; análise do cliente 50% mais rápida = −2; ARQ 20% = −10; torres do AP final de ARQ em paralelo = −10.
- Há **duas cadeias quase empatadas**: interiores (187) e arquitetura do AP (183). Medida em uma só rende até −4; o pacote nas duas rende −8 (−15 se a análise de 22 dias da consultoria também caísse, valor tratado só como limite superior).
- Métodos: CBC prova o ótimo na pequena (45, segundos) e não fecha na completa; a heurística prova o ótimo na completa (187, 10 s).

---

## 6. O que isso sugere para o processo real (para discutir)

Estas são interpretações dos cenários. **Não foram testadas no projeto real.** Servem como discussão e trabalho futuro no artigo.

1. **O ganho de 123 dias vem da ordem, não de esforço extra.** O cronograma praticado foi montado com uma fila manual de entregas. Reordenar, liberando cada atividade assim que os vínculos permitem e usando as frentes paralelas que as equipes já têm, elimina esperas que não são obrigatórias. É a resposta direta para "pra que serve otimizar isso?".
2. **Contratar mais gente não é a primeira medida.** O prazo não depende das equipes. Mais pessoas só ajudariam se fossem usadas para encurtar atividades da cadeia crítica, o que é diferente de abrir mais frentes.
3. **Atacar o tempo de emissão nas cadeias críticas e quase críticas** (interiores e arquitetura). Exemplos de medidas que reduzem duração de emissão:
   - **predefinições de projeto**: bibliotecas de famílias, padrões de layout e de especificação de interiores definidos antes do EP, para cada revisão começar adiantada;
   - **automação de tarefas repetitivas** de modelagem e documentação (folhas, tabelas, numeração, compatibilização de parâmetros), comum em fluxos BIM;
   - **entregas por zona em paralelo**, quando a dependência entre zonas não for técnica.
4. **Diminuir ciclos de revisão.** Cada volta "emissão → análise → reemissão" da cadeia de interiores soma dias. Briefing mais fechado na largada e reuniões de alinhamento antes da emissão tendem a reduzir R01 e R02. O modelo atual trata o número de revisões como dado. Tratar como decisão está nas extensões em `docs/03-modelagem-completa.pdf`.
5. **Prazo máximo para a análise do cliente** (SLA) ajuda pouco sozinho (−4 a −6 dias). Vale como complemento, não como medida principal. Combinado com emissão mais rápida, rende mais (seção 4D).
6. **Liberar as disciplinas cedo** (seção 4B). Se as largadas tardias foram por contratação tardia de disciplina ou briefing atrasado, a medida de maior efeito é de gestão do contrato e não de produção: contratar e dar o briefing de interiores, PCI, fundação e contenção junto com arquitetura. É a diferença entre 285 e 187.
7. **Entregar zonas em paralelo nas duas cadeias** (seção 4C), quando a ordem entre zonas não for técnica. Sozinha em uma disciplina não rende nada ou quase nada; nas duas, rende −8.
8. **Atacar a atividade mais longa da cadeia de interiores**: a R01 do AP com 20 dias (T166), o dobro das emissões vizinhas. Junto com zonas em paralelo, −8. A análise de 22 dias da consultoria (T026) **não entra como medida**: é específica deste empreendimento (janela de decisão do cliente). Encurtá-la daria −15 no pacote, valor usado só como limite superior.
9. ~~Compatibilizar por zona.~~ **Retirada em 23/11.** A proposta partia da espera de 31 dias antes da compatibilização final (T244). A conferência no R14 mostrou que essa espera é um vínculo ausente da base, e o Henrique confirmou que a compatibilização não toma esses dias na prática. Fica só como observação de dados (seção 6.2 e limitações do artigo).

### 6.1 Perguntas para quem conhece o processo (parte humana)

As respostas decidem como o resultado é apresentado. As respostas de Henrique, de 23/11, estão na seção 6.2.

1. **Por que interiores (T007), PCI (T072), fundação e contenção (T066, T067) só começaram no dia 75?** Contrato da disciplina, briefing, espera do cliente, ou dependência de arquitetura que não está na base?
2. **O que são as 4 emissões de ARQ do EP que começam no dia 120** (T141 a T144, 52 dias cada, depois do AP de arquitetura, alimentando a CXO)? Se dependiam de algo, o ótimo vai para perto de 285.
3. **A ordem das zonas no AP é técnica?** Interiores (T114 a T117) e arquitetura (T135 a T139) emitem zona por zona em sequência. Dá para emitir zonas em paralelo, ou a sequência vem de dependência real (pavimento tipo antes dos demais, por exemplo)?
4. **Por que a análise T026 levou 22 dias** e a R01 T166 levou 20? É prazo normal desse tipo de entrega ou houve problema específico (mudança de escopo, espera de decisão)?
5. **Por que a compatibilização (T244) esperou 31 dias?** Faltava alguma disciplina, era lote programado, ou era fila da equipe de coordenação?
6. **Quais medidas são realistas na projetista** e quanto cada uma reduz de verdade uma emissão: predefinições e bibliotecas de interiores, automação de folhas e tabelas, templates de AP? Um número aproximado (por exemplo, "uma R01 cai de 20 para 12 dias") vira um cenário em segundos.
7. **As capacidades fazem sentido?** O ótimo usa `PROJ-ARQ` em 6 frentes e `ANL-PRODUTO` em 7 ao mesmo tempo. Na prática, a equipe de arquitetura toca 6 entregas em paralelo?

### 6.2 Como o processo funciona, segundo quem trabalha nele

Relato de Henrique, de 23/11, que trabalha com BIM numa projetista. É **conhecimento do processo**, não dado do cronograma. Serve para interpretar os resultados e montar as propostas de melhoria.

- **As disciplinas só começam depois da arquitetura.**
  - No estudo inicial, a ARQ elabora, as disciplinas elaboram em cima dela e a ARQ absorve. Daí segue para o AP.
  - No AP, a ARQ manda e as disciplinas (climatização, interiores, PCI e outras) fazem a primeira emissão. A ARQ recebe junto com a construtora, que faz a análise técnica e a compatibilização. A ARQ gera a análise e uma nova emissão, e começa o segundo ciclo da etapa, em que as disciplinas respondem a tudo e emitem de novo. **A ARQ sempre tem mais revisões, porque precisa atender a todos: é um ciclo da ARQ até fechar tudo.** Depois a etapa muda para o executivo.
  - No executivo, algumas disciplinas só começam quando a ARQ já está mais madura, por exemplo interiores.
  - Isso confirma a seção 4F: as largadas tardias são espera pela ARQ. A cadeia da base de 285 é exatamente esse ciclo do AP.
- **Fundação e contenção** começam com o AP de estrutura, que só sai depois do primeiro AP de arquitetura. Quase nunca mudam, mesmo com revisões da estrutura. Isso é coerente com elas não aparecerem na cadeia crítica.
- **Zonas** (pergunta 3): se o projeto é dividido em zonas, cada etapa costuma andar zona por zona, uma após a outra (torre A, depois B, depois C). São tarefas separadas porque o volume de trabalho é grande, mas no planejamento podem funcionar como **uma grande entrega**. A sequência não é necessariamente técnica.
- **Capacidade** (pergunta 7): depende do projeto. Neste, 6 frentes de arquitetura são plausíveis: torres A, B e C e embasamento, com as torres A e B divididas em 2 setores cada.
- **Redução realista com padronização** (pergunta 6): com um template bem montado, uma emissão de 7 dias já caiu para 3, mas isso depende do nível de modelagem. Para não sair do chão, **10% de redução é uma hipótese razoável**. Mais importante que o número é saber **o que reduzir e quando**: template não é número mágico. As propostas só fazem sentido depois desta análise, que mostra onde a redução vira prazo.
- **Perguntas 4 e 5**, respondidas pela conferência no R14 (o Henrique não sabia responder pelo processo):
  - **T026, análise da consultoria wellness, 22 dias.** Não é uma análise técnica de desenho comum. As outras análises do cliente sobre pacotes de interiores no mesmo trecho levam de 1 a 5 dias. As duas análises de **consultoria** do cronograma levam bem mais: 20 dias (análise da consultoria e direcionamento de interiores) e 22 (esta). Ela acontece junto com a validação do conceito pela diretoria e com a atualização do briefing de produto. Na data do R14, ela está com 0%, embora estivesse prevista para começar quatro semanas antes. A leitura provável é que os 22 dias são uma janela de decisão do produto (o que entra no spa, na academia e no tênis), e não tempo de revisão. Isso é interpretação, não confirmação. **Encaminhamento (Henrique, 23/11):** por ser específica demais deste projeto, a T026 sai das medidas propostas e o cenário com ela vira limite superior do ganho (seção 4C, nota 2).
  - **T244, compatibilização final do AP, espera de 31 dias.** É um vínculo ausente na base. No R14, a compatibilização depende de todo o grupo de estrutura AP R01 (formas completo), que termina com a análise do R01 do embasamento. No praticado, a T244 começa no dia 270, logo depois dessa análise (T236, dias 265 a 269). Na base, só o R01 da primeira zona (T229) está ligado à T244. Restaurando os vínculos das zonas 2 a 4 e das análises (T231 a T236 → T244), a espera no praticado cai para **1 dia**. Efeito no ótimo: com largadas livres, de 187 para **196**; com liberações, **285, sem mudança**. A base não foi alterada: corrigir o vínculo é decisão do grupo. **Henrique confirmou (23/11):** a compatibilização não toma esses 31 dias na prática. A proposta de compatibilizar por zona foi retirada (item 9 da seção 6).

**Encaminhamento combinado:** os gargalos e as ideias de melhoria não serão tratados agora no modelo. Entram no artigo como **levantamento e propostas de melhoria**, apoiados nos cenários.

---

## 7. Próximos testes possíveis

Já executados em 23/11 (seções 4A a 4E): combinações de medidas, retirada de revisões R02, zonas em paralelo, largadas tardias e comparação com o CBC na instância pequena.

Ainda não executados:

- Cenários com números reais de redução vindos da pergunta 6 da seção 6.1.
- Cenário intermediário de largadas: prender só as que tiverem motivo real confirmado (pergunta 1 e 2 da seção 6.1).
- Confirmar o 187 pelo CBC: usar o cronograma de 187 como solução inicial (warm start) com horizonte 187. O solver deve fechar gap zero rapidamente, mas a prova acima já é suficiente. Não rodar sem combinar, porque é uma rodada longa.
- A instância média é recorte histórico bloqueado pela auditoria; usá-la exigiria liberar o bloqueio, o que não foi discutido.

---

## 8. Cuidados e limitações

- **Convenção TI com lag zero:** a sucessora pode começar no mesmo dia da entrega da predecessora, com um dia de sobreposição por vínculo. A referência de 310 dias e o ótimo de 187 usam a mesma regra, então a comparação é justa. A convenção precisa estar escrita no artigo.
- **Largadas livres:** atividades sem predecessora podem começar no dia 0. Se os atrasos de largada do praticado tinham motivo real, o ótimo é 285 e não 187 (seção 4B). É a hipótese com maior efeito no resultado.
- **Capacidades estimadas** pelo pico do cronograma praticado, não pela capacidade real comprovada das equipes.
- **Reduções percentuais uniformes** são cenários hipotéticos. Não dizem quanto custa, nem se é possível, emitir 10% mais rápido.
- **Calendário abstrato** de dias úteis, sem feriados. Cobertura incompleta de tarefas escondidas em agrupadores do PDF. As limitações da base em `docs/roteiro-para-agentes.md` continuam valendo.
- **Cenários com "não"** são limites superiores. O ótimo pode ser menor, nunca maior.
- O replanejamento parte do zero e inclui tarefas já executadas na realidade. É uma comparação de planejamento, não uma reprogramação do projeto em andamento.

---

## Como reproduzir

A partir da raiz do projeto, com o ambiente do `codigo/requirements.txt`:

```bash
python codigo/sensibilidade.py
```

O script lê a instância definida em `codigo/configuracao.py`, roda a auditoria, calcula o limite inferior, monta o cronograma da base, valida, roda todos os cenários e grava `resultados/sensibilidade-<data>.json`. Leva cerca de 40 segundos. Para criar cenários novos, edite as funções do bloco `# cenarios` em `codigo/sensibilidade.py`. As reduções e os SLAs testados ficam no topo do arquivo.
