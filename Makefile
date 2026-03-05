all:
	
install:
	pip install -r requirements.txt

run:
	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb a_maze_ing.py

clean:
	rm -rf .mypy_cache __pycache__

lint:
	python3.10 -m flake8 . && mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	python3.10 -m flake8 . && mypy . --strict

.PHONY: all install run debug clean lint lint-strict