# Makefile for mock_http_origin
# https://www.gnu.org/software/make/manual/make.html

VENV = mock_http_origin_venv
VENV_BIN = ./$(VENV)/bin

# Install the application requirements
install: requirements.txt
	# Use `python3` from the current environment to create a virtual environment
	python3 -m venv $(VENV)
	# Upgrade PIP in the virtual environment
	$(VENV_BIN)/python -m pip install --upgrade pip
	# Install the Python requirements in the virtual environment
	$(VENV_BIN)/python -m pip install -r requirements.txt

# Test the application
test:
	$(VENV_BIN)/python -m pytest -v tests/test_*.py

# (Re)Format the application files
format:
	$(VENV_BIN)/black *.py

# Lint the application files
lint:
	# Use a larger max length since screens are larger these days
	$(VENV_BIN)/flake8 --max-line-length 127 *.py

all: install lint test

# Actions that don't require target files
.PHONY: clean

# Clean up files used locally when needed
clean:
	# Remove the Python cache files
	rm -rf ./__pycache__
	rm -rf ./tests/__pycache__
	# Remove the Python pytest files
	rm -rf ./.pytest_cache
	# Remove the Python the virtual environment
	rm -rf ./$(VENV)
