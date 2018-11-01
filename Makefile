.PHONY: pip-compile pip-install type install-pre-commit run-pre-commit

pip-compile:
	source venv/bin/activate; pip-compile requirements.in

pip-install:
	source venv/bin/activate; pip install -r requirements.txt

install-pre-commit: pip-install
	source venv/bin/activate; pre-commit install

run-pre-commit:
	source venv/bin/activate; pre-commit run

type:
	source venv/bin/activate; mypy --ignore-missing-imports .;

build: pip-install run-pre-commit
