.PHONY: install run

install:
	pip install -r requirements.txt

run:
	PYTHONPATH=. ./venv/bin/adk web agents
