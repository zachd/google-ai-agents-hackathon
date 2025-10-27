.PHONY: install run

install:
	pip install -r requirements.txt

run:
	./venv/bin/adk web game_master user_persona planning
