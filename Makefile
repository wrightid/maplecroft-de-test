.PHONY: init clean build run db-migrate db-upgrade db-remove db-revision test tox

init:  build run
	docker-compose exec web flask db upgrade
	docker-compose exec web flask api init
	@echo "Init done, containers running"

clean:  db-remove
	docker-compose down -v
   
build:
	docker-compose build

run:
	docker-compose up -d

db-migrate:
	docker-compose exec web flask db migrate

db-upgrade:
	docker-compose exec web flask db upgrade

# e.g. make db-revision ARGS='-m "create sites table"'
db-revision:
	docker-compose exec web flask db revision $(ARGS)

db-remove:
	docker-compose exec web rm /db/api.db

test:
	docker-compose run -v $(PWD)/tests:/code/tests:ro web tox -e test

tox:
	docker-compose run -v $(PWD)/tests:/code/tests:ro web tox -e py38

lint:
	docker-compose run web tox -e lint
