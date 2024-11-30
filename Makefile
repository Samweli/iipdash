.PHONY: help lint/flake8 lint/sort lint docs servedocs
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help: ## display this message
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

lint/flake8: ## check style with flake8
	flake8 .

lint/isort: ## sort imports with isort
	isort .

lint: lint/isort lint/flake8 ## check style & sort imports

docs: ## generate Sphinx HTML documentation, including API docs
	$(MAKE) -C docs clean
	$(MAKE) -C docs apidocs
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: ## build, watch and serve docs with live reload
	$(MAKE) -C docs livehtml
