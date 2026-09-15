# Template LaTeX

Projeto base para reutilizar na criacao de novos documentos, seguindo a mesma
estrutura usada em `repos/latex/latex`.

## Estrutura

```text
template-latex/
├── main.tex
├── Makefile
├── latexmkrc
├── referencias.bib
├── capa/
│   └── capa.tex
├── relatorio/
│   └── conteudo.tex
├── imagens/
│   └── logos/
├── gerais/
│   ├── pacotes.tex
│   └── comandos.tex
└── build/
```

## Como reutilizar

1. Copie a pasta `template-latex/` para o nome do novo projeto.
2. Edite `gerais/comandos.tex` com titulo, disciplina, autores e data.
3. Ajuste `capa/capa.tex` se quiser trocar o layout da capa.
4. Escreva o texto principal em `relatorio/conteudo.tex`.
5. Coloque imagens em `imagens/` e logos em `imagens/logos/`.
6. Atualize `referencias.bib` se houver bibliografia.

## Compilacao

```bash
make
```

O PDF sera gerado em `build/main.pdf`.

## Compilacao continua

```bash
make watch
```

Esses comandos usam `latexmk` com `-shell-escape`, igual ao projeto base.

## Limpeza

```bash
make clean
```
