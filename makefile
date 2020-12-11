MODULENAME = jupyterinstruct 

help:
	@echo "JupyterInstruct Makefile"
	@echo ""
	@cat ./makefile
	

init:
	conda env create --prefix ./envs --file environment.yml

docs:
	pdoc3 --force --html --output-dir ./docs $(MODULENAME)
	python makeindex.py ./README.md > docs/index.html

lint:
	pylint $(MODULENAME)

doclint:
	pydocstyle $(MODULENAME)

test:
	pytest -v tests

UML:
	pyreverse -ASmy -o png $(MODULENAME)
	mv *.png ./docs/images

.PHONY: UML init docs lint test 

