# Análise de sensibilidade: o que limita o prazo e o que vale mudar

Atualizado em 23/11/2026, por Henrique (Jascolka). Os números deste documento vêm de `codigo/sensibilidade.py`, que não chama o CBC e não altera os CSVs. O registro completo da rodada está em `resultados/sensibilidade-20261123T131548Z.json`.

Este documento traz **resultados verificados** (seções 1 a 5) e **interpretações e propostas para discutir no grupo** (seções 6 e 7). As propostas não são decisões tomadas.

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

## 5. Resumo numérico para o artigo e os slides

- Referência praticada: **310** dias.
- CBC, indexado no tempo, 36 min: **307** dias, sem prova (gap 39%).
- Heurística + limite inferior, ~10 s: **187** dias, **ótimo comprovado**. Ganho de **123 dias (39,7%)** com as mesmas atividades, durações, vínculos e equipes.
- O prazo é definido pela **cadeia de emissões e análises de interiores**, não pela capacidade das equipes.
- **+1 em todas as equipes: 0 dia.** **Emissão 10% mais rápida: −10 dias.** **Tudo 20% mais rápido: −38 dias.**

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
5. **Prazo máximo para a análise do cliente** (SLA) ajuda pouco sozinho (−4 a −6 dias). Vale como complemento, não como medida principal.

---

## 7. Próximos testes possíveis

Nada disso foi executado. Cada um leva segundos com o script.

- Combinar medidas, por exemplo emissão de ARI e ARQ 20% mais rápida mais SLA de 5 dias.
- Testar um ciclo de revisão a menos nas atividades R02 da cadeia crítica (zerar ou retirar a atividade e religar os vínculos), deixando a mudança explícita no texto.
- Confirmar o 187 pelo CBC: usar o cronograma de 187 como solução inicial (warm start) com horizonte 187. O solver deve fechar gap zero rapidamente, mas a prova acima já é suficiente.
- Rodar a heurística nas instâncias média e pequena, para comparar com os resultados do CBC nelas.

---

## 8. Cuidados e limitações

- **Convenção TI com lag zero:** a sucessora pode começar no mesmo dia da entrega da predecessora, com um dia de sobreposição por vínculo. A referência de 310 dias e o ótimo de 187 usam a mesma regra, então a comparação é justa. A convenção precisa estar escrita no artigo.
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

O script lê a instância definida em `codigo/configuracao.py`, roda a auditoria, calcula o limite inferior, monta o cronograma da base, valida, roda todos os cenários e grava `resultados/sensibilidade-<data>.json`. Leva cerca de 10 segundos. Para criar cenários novos, edite as funções do bloco `# cenarios` em `codigo/sensibilidade.py`. As reduções e os SLAs testados ficam no topo do arquivo.
