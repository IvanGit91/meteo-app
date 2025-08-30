#!/usr/bin/make

api_svc := api

db-init:
	docker-compose run $(api_svc) python app.py db init
db-migrate:
	docker-compose run $(api_svc) python app.py db migrate
db-upgrade:
	docker-compose run $(api_svc) python app.py db upgrade
db-downgrade:
	docker-compose run $(api_svc) python app.py db downgrade
# Fix the error of an empty database: Target database is not up to date.
db-stamp-head:
	docker-compose run $(api_svc) python app.py db stamp head