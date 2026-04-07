.PHONY: venv install run debug clean lint lint-strict

PYTHON := python3
VENV := .venv
VENV_BIN := $(VENV)/bin
MAIN := a_maze_ing.py

run: venv
	@echo "Running the project..."
	$(VENV_BIN)/python $(MAIN) config.txt

venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv $(VENV); \
	fi

install: venv
	@echo "Installing dependencies..."
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install -r requirements.txt

debug: venv
	@echo "Running in debug mode..."
	$(VENV_BIN)/python -m pdb $(MAIN)

clean:
	@echo "Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

lint: venv
	@echo "Running lint checks..."
	-$(VENV_BIN)/flake8 $(MAIN) src
	$(VENV_BIN)/mypy $(MAIN) src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: venv
	@echo "Running strict lint checks..."
	-$(VENV_BIN)/flake8 $(MAIN) src
	$(VENV_BIN)/mypy $(MAIN) src --strict
