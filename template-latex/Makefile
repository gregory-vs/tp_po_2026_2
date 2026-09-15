MAIN=main.tex

.PHONY: all pdf watch clean

all: pdf

pdf:
	latexmk -pdf -shell-escape -interaction=nonstopmode -synctex=1 -outdir=build $(MAIN)

watch:
	latexmk -pdf -shell-escape -interaction=nonstopmode -synctex=1 -pvc -outdir=build $(MAIN)

clean:
	latexmk -c
	rm -rf build
