.PHONY: help install/dev install/pre-commit install lint/flake8 lint/sort lint format/black format docs servedocs
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

install/dev: ## install dependencies for local development
	python -m pip install -U pip
	python -m pip install -r requirements_dev.txt
	python -m pip install -r requirements_docs.txt

install/pre-commit: ## install pre-commit for local development
	python -m pip install -U pre-commit
	python -m pre_commit install --install-hooks
	python -m pre_commit install --hook-type commit-msg

install: install/dev install/pre-commit ## install and setup dependencies (e.g pre-commit, commitizen etc)

lint/flake8: ## check style with flake8
	python -m flake8 .

lint/isort: ## sort imports with isort
	python -m isort .

lint: lint/isort lint/flake8 ## check style & sort imports

format/black: ## format codes using black
	python -m black .

format: format/black ## format codes

docs: ## generate Sphinx HTML documentation, including API docs
	$(MAKE) -C docs clean
	$(MAKE) -C docs apidocs
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: ## build, watch and serve Sphinx HTML documentation with live reload
	$(MAKE) -C docs livehtml
