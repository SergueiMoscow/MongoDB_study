SOURCE = api db repositories tests services

.PHONY: check
check:
	autoflake $(SOURCE)
	isort $(SOURCE)
	black -l 100 -S $(SOURCE)
	unify -r -i -c $(SOURCE)
	pytest

.PHONY: test
test:
	pytest

.PHONY: run
run:
	uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload
