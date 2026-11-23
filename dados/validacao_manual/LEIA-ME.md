# Exemplo da validação conjunta

Caso didático independente da base real, preparado em 23/11/2026 para execução manual por Thales. Thales executou o caso e a comparação com a solução manual foi concluída em 23/11/2026. O resultado observado está registrado abaixo.

## Dados e solução manual

A dura três dias e B dura dois; ambas usam PROJETO, de capacidade um. C dura dois dias e usa ANÁLISE, também de capacidade um. C depende das entregas de A e B, com TI e defasagem zero.

| Atividade | Início manual | Entrega manual |
| --- | ---: | ---: |
| A | 0 | 2 |
| B | 3 | 4 |
| C | 4 | 5 |

O prazo é seis dias. A e B precisam de cinco dias da mesma equipe sem sobreposição; a última dessas entregas ocorre no mínimo no dia quatro. C pode começar nesse dia e entrega no dia cinco. Portanto, nenhum cronograma desse caso termina em menos de seis dias da escala. Inverter a ordem de A e B também pode produzir um ótimo válido.

## Como executar pelo programa

1. Abra `codigo/configuracao.py`.
2. Altere somente `INSTANCIA` para `"validacao_manual"` e `HORIZONTE` para `10`.
3. Salve o arquivo. O horizonte dez dá espaço ao caso sem fixar seu prazo em seis. É uma configuração didática; o horizonte aprovado da base real continua sendo 310.
4. No PowerShell, na raiz do repositório, execute:

```powershell
.\.venv\Scripts\python.exe codigo\main.py
```

5. Confira: auditoria aprovada, situação de ótimo comprovado, validação aprovada e prazo calculado de seis dias. As atividades A e B podem aparecer em ordem inversa à solução manual.
6. Confira os inícios, entregas e capacidades. A última entrega deve estar no índice cinco. O programa informa o caminho do JSON com todos os inícios e do log do CBC em `resultados/`.

Este caso não possui cronograma praticado histórico cadastrado; não haverá cálculo de ganho percentual contra a base real.

Após concluir a comparação, restaure `INSTANCIA = "instancia_completa"` e `HORIZONTE = 310` na configuração. A execução da instância completa será feita na etapa dos experimentos, depois de combinarmos o cenário.

## Resultado obtido e conferido em 23/11/2026

| Atividade | Início obtido | Entrega obtida |
| --- | ---: | ---: |
| B | 0 | 1 |
| A | 2 | 4 |
| C | 4 | 5 |

A e B foram invertidas em relação à primeira solução manual, sem mudar o prazo ótimo de seis dias. PROJETO usa uma vaga por dia de zero a quatro; ANÁLISE usa uma vaga nos dias quatro e cinco. C começa no próprio dia da última entrega, em outra equipe, como permitido.

O JSON informa solução validada, ótimo comprovado, objetivo bruto 6, limite inferior 6, gap zero e nenhuma lista de erros ou avisos. O log contém o término de ótimo do CBC. Tempo medido pela aplicação: aproximadamente 0,037 segundo. Ambiente: PuLP 3.3.0, CBC 2.10.3 e Python 3.13.5.

Evidências da execução pelo usuário:

- `../../resultados/20261123T031257183085Z-b0cc1c21.json`
- `../../resultados/20261123T031257183085Z-b0cc1c21.log`

Essa comparação encerra a validação conjunta do exemplo principal. Os 27 testes automatizados complementam a revisão. Ela não é um experimento da base real e não fornece ganho percentual para o projeto.
