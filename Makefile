SHELL := /bin/bash
PWD := $(shell pwd)


.PHONY: init
init:
	@poetry shell

.PHONY: setup
setup:
	@cp -Rf ./contrib/env-sample .env
	@poetry install
	@mkdir -p $(PWD)/static

.PHONY: serve
serve:
	@python manage.py runserver

.PHONY: docs
docs:
	@cd docs && mkdocs serve

migrate:
	@python manage.py migrate

makemigrations:
	@python manage.py makemigrations

.PHONY: docker-run
docker-run:
	@docker-compose up -d --build

.PHONY: docker-destroy
docker-destroy:
	@echo "Destroying containers and volumes..."
	@docker-compose rm -vsf studyrooms studyrooms-db
	@docker volume rm studyrooms_postgres_data

.PHONY: generate-requirements
generate-requirements:
	@poetry export -f requirements.txt --output requirements.txt
