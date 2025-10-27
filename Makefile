.PHONY: all venv install setup run clean help

# Detect Python command
PYTHON := $(shell command -v python3 2> /dev/null || command -v python 2> /dev/null)
VENV_BIN := venv/bin
PIP := $(VENV_BIN)/pip
ADK := $(VENV_BIN)/adk

all: setup ## Complete setup and show next steps (default target)
	@echo ""
	@echo "✅ All setup steps completed!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Edit .env and add your Google API key"
	@echo "  2. Run 'make run' to start the ADK server"
	@echo ""

help: ## Show this help message
	@echo "Available targets:"
	@echo ""
	@echo "Setup & Run:"
	@echo "  make all     - Complete setup and show next steps (default)"
	@echo "  make setup   - Create venv and install all dependencies"
	@echo "  make venv    - Create virtual environment only"
	@echo "  make install - Install dependencies in existing venv"
	@echo "  make run     - Run the ADK server with agents on port 8081"
	@echo "  make clean   - Remove virtual environment"
	@echo ""
	@echo "Note: See evals/README.md for evaluation test scenarios (documentation format)"

venv: ## Create virtual environment
	@if [ ! -d "venv" ]; then \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv venv; \
		echo "Virtual environment created."; \
	else \
		echo "Virtual environment already exists."; \
	fi

install: venv ## Install dependencies
	@echo "Installing dependencies..."
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@echo "Dependencies installed."

setup: install ## Complete setup (venv + install)
	@if [ ! -f ".env" ]; then \
		echo "Creating .env file from .env.example..."; \
		cp .env.example .env; \
		echo ""; \
		echo "⚠️  IMPORTANT: Please edit .env and add your Google API Key"; \
		echo "   Get your key from: https://aistudio.google.com/app/apikey"; \
	else \
		echo ".env file already exists."; \
	fi
	@echo "Setup complete!"

run: ## Run ADK server
	@if [ ! -f ".env" ]; then \
		echo "❌ Error: .env file not found. Run 'make setup' first."; \
		exit 1; \
	fi
	@echo "Starting ADK server on port 8081..."
	@$(ADK) web --port 8081 .

clean: ## Remove virtual environment
	@echo "Removing virtual environment..."
	@rm -rf venv
	@echo "Clean complete."
