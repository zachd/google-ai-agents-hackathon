.PHONY: all venv install setup run run-backend run-frontend run-all clean help

# Detect Python command
PYTHON := $(shell command -v python3 2> /dev/null || command -v python 2> /dev/null)
VENV_BIN := venv/bin
PIP := $(VENV_BIN)/pip
ADK := $(VENV_BIN)/adk
NODE := $(shell command -v node 2> /dev/null)
NPM := $(shell command -v npm 2> /dev/null)

all: setup ## Complete setup and show next steps (default target)
	@echo ""
	@echo "✅ All setup steps completed!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Edit .env and add your Google API key"
	@echo "  2. Run 'make run-all' to start both backend and frontend"
	@echo ""

help: ## Show this help message
	@echo "Available targets:"
	@echo "  make all         - Complete setup and show next steps (default)"
	@echo "  make setup       - Create venv and install all dependencies"
	@echo "  make venv        - Create virtual environment only"
	@echo "  make install     - Install dependencies in existing venv"
	@echo "  make run         - Run the ADK server with agents (port 8081)"
	@echo "  make run-backend - Run FastAPI backend server (port 8080)"
	@echo "  make run-frontend- Run React frontend (port 8082)"
	@echo "  make run-all     - Run both backend and frontend together"
	@echo "  make clean       - Remove virtual environment"

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

run-backend: ## Run FastAPI backend server
	@if [ ! -f ".env" ]; then \
		echo "❌ Error: .env file not found. Run 'make setup' first."; \
		exit 1; \
	fi
	@echo "Starting FastAPI backend server on port 8080..."
	@python main.py

run-frontend: ## Run React frontend
	@if [ ! -d "node_modules" ]; then \
		echo "Installing frontend dependencies..."; \
		npm install; \
	fi
	@echo "Starting React frontend on port 8082..."
	@npm run dev

run-all: ## Run both backend and frontend together
	@echo "🚀 Starting Mystery Trip Planner (Backend + Frontend)"
	@echo ""
	@echo "Backend will run on: http://localhost:8080"
	@echo "Frontend will run on: http://localhost:8082"
	@echo ""
	@echo "Press Ctrl+C to stop both services"
	@echo ""
	@if [ ! -f ".env" ]; then \
		echo "❌ Error: .env file not found. Run 'make setup' first."; \
		exit 1; \
	fi
	@if [ ! -d "node_modules" ]; then \
		echo "Installing frontend dependencies..."; \
		npm install; \
	fi
	@echo "Starting services..."
	@trap 'kill %1; kill %2' INT; \
	python main.py & \
	npm run dev & \
	wait

clean: ## Remove virtual environment
	@echo "Removing virtual environment..."
	@rm -rf venv
	@echo "Clean complete."
