.PHONY: venv install run debug clean lint build

PYTHON := python3
VENV := .venv
VENV_BIN := $(VENV)/bin
MAIN := a_maze_ing.py
PACKAGE := mazegen-1.0.0.tar.gz
GEN_PATH := src/mazegen
MAZEGEN := $(GEN_PATH)/mazegen.py
INSTALL := $(VENV)/.install_done

all: run

$(PACKAGE): $(MAZEGEN)
	$(VENV_BIN)/python -m pip install --upgrade build
	$(VENV_BIN)/python -m build $(GEN_PATH) --sdist
	@mv $(GEN_PATH)/dist/$(PACKAGE) .
	@rmdir $(GEN_PATH)/dist

$(INSTALL): requirements.txt $(PACKAGE)
	@echo "Installing dependencies..."
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install -r requirements.txt
	$(VENV_BIN)/pip install $(PACKAGE)
	@touch $(INSTALL)

run: install
	@echo "Running the project..."
	$(VENV_BIN)/python $(MAIN) config.txt

venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv $(VENV); \
	fi

install: venv $(INSTALL)

debug: install
	@echo "Running in debug mode..."
	$(VENV_BIN)/python -m pdb $(MAIN)

clean:
	@echo "Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

fclean: clean
	find . -type d -name ".venv" -exec rm -r {} +
	find . -type f -name "mazegen-*" -delete

lint: install
	@echo "Running lint checks..."
	-$(VENV_BIN)/flake8 $(MAIN) src
	$(VENV_BIN)/mypy $(MAIN) src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

build: venv $(PACKAGE)
