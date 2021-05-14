LATEX_CMD = pdflatex
SRC = report4tb3.tex

RMDIR = rm -rf

all: latex clean

latex: 
	$(LATEX_CMD) $(SRC)

clean:	
	@- $(RMDIR) *.ps *.dvi *.aux *.toc *.idx *.ind *.ilg *.log *.out *.brf *.blg *.bbl
