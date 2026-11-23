# Artigo

Modelo LaTeX modular para o artigo do trabalho de Pesquisa Operacional.
A primeira página reúne título, autores, afiliação, resumo e palavras-chave.
O texto usa uma coluna, fonte serifada, margens de 2,5 cm e seções numeradas,
sem capa institucional, matrículas, sumário ou folha de identificação.

## Estrutura editorial

| Arquivo em `secoes/` | Conteúdo |
| --- | --- |
| `00-resumo.tex` | Resumo e palavras-chave |
| `01-introducao.tex` | (i) Introdução |
| `02-revisao-literatura.tex` | (ii) Revisão da literatura |
| `03-problema-modelagem.tex` | (iii) Descrição do problema e modelagem |
| `04-algoritmo.tex` | (iv) Descrição do algoritmo |
| `05-resultados-analise.tex` | (v) Resultados e análise |
| `06-conclusoes.tex` | (vi) Conclusões |
| `07-referencias.tex` | (vii) Referências bibliográficas |

As referências ficam sem numeração, como é usual em artigos. Os trechos em
cinza são orientações de redação: substitua cada chamada `\preencher{...}`
pelo texto definitivo. O modelo não contém resultados ou referências fictícias.
As subdivisões propostas podem ser ajustadas durante a escrita.

## Organização dos arquivos

- `main.tex`: documento principal e ordem das seções.
- `config/metadados.tex`: título, autores e afiliação.
- `config/pacotes.tex`: tipografia, margens, figuras, tabelas e links.
- `config/comandos.tex`: comandos de apoio à redação.
- `secoes/`: um arquivo por tópico, além do resumo.
- `bibliografia/referencias.bib`: base de referências do BibTeX.
- `imagens/`: figuras; os recursos herdados do template estão preservados,
  mas não são inseridos automaticamente no artigo.
- `build/`: PDF e arquivos auxiliares gerados, ignorados pelo Git.

## Referências e citações

A referência fictícia do template foi retirada. Para iniciar a bibliografia:

1. Cadastre as referências reais em `bibliografia/referencias.bib`.
2. Cite-as no texto com `\cite{chave}`. O documento
   `docs/referencias-comentadas.md`, na raiz do repositório, ajuda a localizar
   as fontes; confira os dados bibliográficos nos originais.
3. Em `secoes/07-referencias.tex`, retire o título e o marcador provisórios
   e descomente `\bibliographystyle{plain}` e
   `\bibliography{bibliografia/referencias}`.
4. Recompile com `latexmk`, que executa o BibTeX e atualiza as citações.

O marcador provisório permite compilar o modelo mesmo antes de haver citações.
Na versão final, a bibliografia deve listar somente as fontes citadas.

## Compilação

Dentro de `relatorio/`, execute:

```bash
latexmk -pdf main.tex
```

A saída é `build/main.pdf`. É necessário ter uma distribuição LaTeX com
`latexmk`, BibTeX e os pacotes declarados em `config/pacotes.tex`.
O modelo usa pacotes LaTeX usuais e não depende de `minted` ou Pygments.

Com GNU Make, use `make`, `make watch` ou `make clean`. No VS Code com
LaTeX Workshop, abra `main.tex` e use a receita configurada. Os módulos
incluem a indicação do documento principal para o editor.

O PDF herdado do template em `build/` não representa o artigo atual;
é preciso recompilar antes de revisar ou compartilhar o documento.
