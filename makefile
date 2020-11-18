MODULENAME = jupyterinstruct 

help:
	@echo ""
	@echo "Welcome to my project!!!"
	@echo "To get started create an environment using:"
	@echo "	make init"
	@echo "	conda activate ./envs"
	@echo ""
	@echo "To generate project documentation use:"
	@echo "	make docs"
	@echo ""
	@echo "To Lint the project use:"
	@echo "	make lint"
	@echo ""
	@echo "To run pydocstyle on the project use:"
	@echo "	make doclint"
	@echo ""
	@echo "To run unit tests use:"
	@echo "	make test"
	@echo ""
	

init:
	conda env create --prefix ./envs --file environment.yml

docs:
	pdoc3 --force --html --output-dir ./docs $(MODULENAME)

lint:
	pylint $(MODULENAME)

doclint:
	pydocstyle $(MODULENAME)

test:
	pytest -v tests

UML:
	pyreverse -ASmy -o png $(MODULENAME)

.PHONY: UML init docs lint test 

