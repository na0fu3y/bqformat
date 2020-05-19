NAME=bqformat

build:
	docker build -t ${NAME} .

doc: build
	docker run -it --rm -v ${PWD}:/usr/src/app -p 8000:8000 ${NAME} mkdocs serve --dev-addr=0.0.0.0:8000
