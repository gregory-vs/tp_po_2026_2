# Base de dados do estudo

A base anonimizada foi preparada a partir do cronograma R14. Em 22/11/2026, restauramos os seis CSVs anteriores às alterações feitas com base no R15, após confirmar a versão correta. Nenhuma duração foi recalculada nessa restauração. Depois, incluímos três atividades e adaptamos equipes e escopo conforme as orientações operacionais encaminhadas por Thales. O estado atual está em `ajustes-projeto/registro.json`.

## Conjuntos existentes

| Pasta | Atividades | Vínculos | Referência na escala da base |
| --- | ---: | ---: | ---: |
| instancia_pequena | 12 | 24 | Exemplo manual, sem praticado |
| instancia_media | 28 | 98 | 138 dias; recorte anterior preservado |
| instancia_completa | 243 | 1008 | 310 dias; execução principal após os ajustes |

Não geraremos novos recortes nesta etapa. A média omite vínculos com atividades externas e usa capacidades herdadas da completa; não reproduz todas as condições do projeto.

## Arquivos de entrada

Os CSVs usam UTF-8 e ponto e vírgula como separador.

- `atividades.csv`: identificador e nome anônimos, nível, tipo, entregável, disciplina, fase, revisão, zona, equipe (`papel`), duração, índices do cronograma normalizado, percentual e estado.
- `precedencias.csv`: predecessora, sucessora, tipo de vínculo (TI, II, TT ou IT) e espera (`lag_dias`).
- `recursos.csv`: papel, categoria, número de atividades e capacidade. A pequena usa `capacidade`; as reais usam `capacidade_observada` e `capacidade_sugerida`.

Na completa, `nivel=ATIVIDADE` seleciona as 243 atividades. Os 47 `AGRUPADOR` ficam fora do modelo. A pequena já vem sem agrupadores.

Vários papéis em uma atividade são separados por ponto e vírgula dentro do campo CSV, que fica entre aspas. Cada equipe listada conta uma atividade aberta durante a janela positiva. Há seis atividades compartilhadas na completa: as quatro originais e duas reuniões adicionadas. As cinco áreas participantes adicionais são representadas por códigos CLIENTE-01 a CLIENTE-05; seus nomes originais ficam somente no mapa privado.

As durações da base de origem coincidiram com as declaradas no R14 nas 295 linhas associadas. As três atividades adicionadas usam as durações declaradas de 3, 20 e 5 dias. Não há duração zero nessa base. O código mantém suporte a eventos de duração zero para uso futuro, sem ocupação de equipe.

## O que significa o cronograma praticado

`inicio_praticado` e `fim_praticado` são índices em uma escala normalizada de dias úteis. Os términos são coerentes com `fim = inicio + duracao - 1`. Eles servem para comparação no mesmo recorte e sob as mesmas regras; não são restrições que congelam as atividades.

Esses índices não prometem datas civis exatas. A preparação converteu datas e normalizou intervalos; não vamos reconstruir a lista de feriados e recessos. Segundo Henrique, os 79 ajustes do relatório antigo foram de datas, preservando durações. O histórico individual desses ajustes não foi recuperado.

## Capacidades

As capacidades da completa são os picos de atividades abertas no cronograma normalizado. Após incluir atividades, corrigir equipes e retirar obra, recalculamos os 39 picos e os cadastramos. Arquitetura passou de sete para seis e elétrica de três para uma atividade simultânea; os demais recursos antigos mantiveram seus picos. As cinco áreas adicionadas têm pico de uma atividade. São estimativas, não máximos operacionais comprovados. As atribuições de papéis preenchidas por regra ainda precisam ser validadas com quem conhece o processo.

A referência é viável internamente na base preparada: a auditoria confere durações, precedências e capacidades. Somente sob o mesmo conjunto de dados e regras um ótimo comprovado não pode ser pior que essa referência.

## Preparação anterior e limitações

O relatório antigo informa expansão de 156 referências a agrupadores, remoção de duplicatas e descarte de 22 arcos por ciclos e 37 por incompatibilidade com as datas normalizadas. A lista individual não foi salva. Não afirmar que todos eram erros de extração ou que as dependências reais foram integralmente validadas.

Henrique informou preenchimento de 34 papéis, 44 disciplinas e 58 fases por regra. O CSV não identifica individualmente esses preenchimentos. Há quatro atividades isoladas; elas não são todas marcos. A execução de obra foi retirada: duas atividades e seis agrupadores. A apresentação de projetos à obra permanece como entrega do processo de projeto. Os quinze vínculos novos preservam as relações declaradas das atividades incluídas, expandindo agrupadores somente para as filhas representadas. Três agrupadores fechados não têm filhas na base; essa limitação de cobertura permanece documentada.

A extração atual do R14 encontrou 307 linhas visíveis, enquanto o relatório antigo contabiliza 304. As três linhas adicionais foram incluídas após autorização. O arquivo `conferencia-r14.json` preserva a conferência inicial e aponta o estado atual; `validacao.json` registra a aprovação da base de projeto na auditoria. A cobertura de atividades ocultas do PDF não foi reconstruída. Não há mais 52 durações pendentes do R15.

## Execução

Edite `codigo/configuracao.py` e execute `python codigo/main.py`. A instância completa é o padrão. A auditoria de entrada roda automaticamente antes da montagem do modelo. A base de projeto passou na auditoria de entrada. O ambiente virtual do projeto agora tem PuLP 3.3.0 e foi testado com CBC em casos sintéticos. A otimização da base real ainda depende da continuação conjunta da validação técnica; nenhum experimento dessa base foi executado.

Para executar somente a auditoria, use `python codigo/verificar.py`. A validação da solução, depois de resolver, fica em `codigo/validacao.py`.

## Privacidade e evidências

Os PDFs do contratante, os mapas de identificadores e a comparação detalhada ficam fora do repositório público. O estado anterior à restauração foi arquivado de forma privada. O repositório mantém somente dados anonimizados e resultados agregados; o script obsoleto que reaplicava alterações do R15 foi removido.

`relatorio_qualidade.txt` é o registro da preparação anterior. Não foi reescrito para fingir que sua contagem foi reproduzida. A auditoria atual deve ser consultada em conjunto com `conferencia-r14.json` e com a conferência em `docs/conferencia-cronograma-original.md`.

## Prazo depois do corte de obra

O prazo atual de referência é 310 dias úteis normalizados. Os 492 dias descreviam o conjunto anterior, com execução de obra. A diferença de 182 dias resulta da mudança de escopo, não de uma solução otimizada. Os inícios e durações das atividades de projeto existentes foram preservados. As alterações de equipe abrangem oito análises com projetistas, quatro análises de estrutura, dois gates e a emissão de plantas de contrato. Cinco emissões de briefing/documentos do cliente foram mantidas com ele. As atribuições de SMOP e as quatro atividades compartilhadas originais foram preservadas.
