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

.PHONY: help
help: ## display this message
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

.PHONY: install/dev
install/dev: ## install dependencies for local development
	python -m pip install -U pip
	python -m pip install -r requirements_dev.txt
	python -m pip install -r requirements_docs.txt

.PHONY: install/pre-commit
install/pre-commit: ## install pre-commit for local development
	python -m pip install -U pre-commit
	python -m pre_commit install --install-hooks
	python -m pre_commit install --hook-type commit-msg

.PHONY: install
install: install/dev install/pre-commit ## install and setup dependencies (e.g pre-commit, commitizen etc)

.PHONY: lint/flake8
lint/flake8: ## check style with flake8
	python -m flake8 .

.PHONY: lint/isort
lint/isort: ## sort imports with isort
	python -m isort .

.PHONY: lint
lint: lint/isort lint/flake8 ## check style & sort imports

.PHONY: format/black
format/black: ## format codes using black
	python -m black .

.PHONY: format
format: format/black ## format codes

.PHONY: docs
docs: ## generate Sphinx HTML documentation, including API docs
	$(MAKE) -C docs clean
	$(MAKE) -C docs apidocs
	$(MAKE) -C docs html

.PHONY: servedocs
servedocs: ## build, watch and serve Sphinx HTML documentation with live reload
	$(MAKE) -C docs livehtml

.PHONY: docker/pull
docker/pull: ## pull docker images i.e python etc
	docker pull ubuntu:24.04 # base image for rabbitmq
	docker pull debian:bullseye-slim # base image for postgres and postgis
	docker pull debian:bookworm-slim # base image for python and redis
	docker pull python:3.12.8-slim-bookworm
	docker pull postgres:17.2-bullseye # base image for postgis
	docker pull postgis/postgis:17-3.5
	docker pull rabbitmq:4.0.4-management
	docker pull redis:7.4.2-bookworm

.PHONY: docker/up/dev
docker/up/dev: docker/clean/dangling ## create and start development docker containers, networks etc.
	docker compose -f ./docker-compose-development.yaml up --remove-orphans --build

.PHONY: docker/down/dev
docker/down/dev: docker/clean/dangling ## stop and remove development docker containers, networks etc.
	docker compose -f ./docker-compose-development.yaml down --remove-orphans

.PHONY: docker/clean/dev
docker/clean/dev: docker/clean/dangling ## stop and remove development docker containers, networks, volumes etc.
	docker compose -f ./docker-compose-development.yaml down -v --remove-orphans

.PHONY: docker/clean/dangling
docker/clean/dangling: ## clean dangling docker images
	docker image ls --filter "dangling=true" -a -q | xargs -L1 -r -t docker rmi
