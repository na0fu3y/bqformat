NAME=bqformat
DEBUG=debug

build docker:
	docker build -t ${NAME}:${DEBUG} .

doc: build
	docker run -it --rm -v ${PWD}:/usr/src/app -p 8000:8000 ${NAME}:${DEBUG} mkdocs serve --dev-addr=0.0.0.0:8000

update: build
	docker run -it --rm -v ${PWD}:/usr/src/app ${NAME}:${DEBUG} python scripts/dictionary_fetcher.py

test: build docker
	docker run -it --rm ${NAME}:${DEBUG} pytest .

vet: build
	docker run -it --rm ${NAME}:${DEBUG} mypy --ignore-missing-imports /usr/src/app/src

fmt: build
	docker run -it --rm -v ${PWD}:/usr/src/app/ ${NAME}:${DEBUG} autoflake -ri /usr/src/app
	docker run -it --rm -v ${PWD}:/usr/src/app/ ${NAME}:${DEBUG} isort -rc /usr/src/app
	docker run -it --rm -v ${PWD}:/usr/src/app/ ${NAME}:${DEBUG} black /usr/src/app

lint: build
	docker run -it --rm ${NAME}:${DEBUG} textlint **/*.md

zetasql:
	docker build -f Dockerfile.zetasql -t zetasql .

run: zetasql
	echo 'select 1' | docker run -i --rm zetasql
