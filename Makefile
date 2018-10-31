.PHONY: pip-compile pip-install type

pip-compile:
	source venv/bin/activate; pip-compile requirements.in

pip-install:
	source venv/bin/activate; pip install -r requirements.txt

type:
	source venv/bin/activate; mypy --ignore-missing-imports .;

build: pip-install type