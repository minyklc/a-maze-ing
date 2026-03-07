all:
	
install:
	pip install -r requirements.txt

run:
	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb a_maze_ing.py

clean:
	rm -rf .mypy_cache __pycache__ build dist *.egg-info

lint:
	python3 -m flake8 . --exclude=src,build,setup.py && python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude src --exclude build --exclude setup

lint-strict:
	python3 -m flake8 . --exclude=src,build,setup.py && python3 -m mypy . --strict --exclude src --exclude build --exclude setup

.PHONY: all install run debug clean lint lint-strict