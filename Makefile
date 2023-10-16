SOURCE = api db repositories tests services

.PHONY: check
check:
	autoflake $(SOURCE)
	isort $(SOURCE)
	black -l 100 -S $(SOURCE)
	unify -r -i -c $(SOURCE)
	pytest --cov-report term-missing --verbosity=2 --cov=.

.PHONY: test
test:
	pytest --cov-report term-missing --verbosity=2 --cov=.

.PHONY: run
run:
	uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload
