SHELL := /bin/bash

run:
	docker-compose up -d
	npm start

test:
	docker-compose run web py.test --capture=no

build:
	docker-compose build
	npm install