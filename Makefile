.PHONY: all venv install setup run run-backend run-frontend run-all docker docker-debug docker-build docker-up docker-down docker-logs clean help

# Detect Python command
PYTHON := $(shell command -v python3 2> /dev/null || command -v python 2> /dev/null)
VENV_BIN := venv/bin
PIP := $(VENV_BIN)/pip
ADK := $(VENV_BIN)/adk
NODE := $(shell command -v node 2> /dev/null)
NPM := $(shell command -v npm 2> /dev/null)

# Detect docker-compose command (try new 'docker compose' first, then old 'docker-compose')
DOCKER_COMPOSE := $(shell docker compose version > /dev/null 2>&1 && echo "docker compose" || echo "docker-compose")

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
	@echo "  make all          - Complete setup and show next steps (default)"
	@echo "  make setup        - Create venv and install all dependencies"
	@echo "  make venv         - Create virtual environment only"
	@echo "  make install      - Install dependencies in existing venv"
	@echo "  make run          - Run the ADK server with agents (port 8081)"
	@echo "  make run-backend  - Run FastAPI backend server (port 8080)"
	@echo "  make run-frontend - Run React frontend (port 8082)"
	@echo "  make run-all      - Run both backend and frontend together"
	@echo ""
	@echo "Docker commands:"
	@echo "  make docker       - Build and start (backend + frontend)"
	@echo "  make docker-debug - Start with ADK web (all 3 services)"
	@echo "  make docker-up    - Start containers"
	@echo "  make docker-down  - Stop containers"
	@echo "  make docker-logs  - View logs"
	@echo ""
	@echo "  make clean        - Remove virtual environment"

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
	@$(VENV_BIN)/python main.py

run-frontend: ## Run React frontend
	@if [ ! -d "frontend/node_modules" ]; then \
		echo "Installing frontend dependencies..."; \
		cd frontend && npm install; \
	fi
	@echo "Starting React frontend on port 8082..."
	@cd frontend && npm run dev

run-all: ## Run both backend and frontend together
	@echo "🚀 Starting Mystery Trip Planner (Backend + Frontend)"
	@echo ""
	@echo "Backend will run on: http://localhost:8080"
	@echo "Frontend will run on: http://localhost:8082 (or next available port)"
	@echo ""
	@echo "Press Ctrl+C to stop both services"
	@echo ""
	@if [ ! -f ".env" ]; then \
		echo "❌ Error: .env file not found. Run 'make setup' first."; \
		exit 1; \
	fi
	@if [ ! -d "frontend/node_modules" ]; then \
		echo "Installing frontend dependencies..."; \
		cd frontend && npm install; \
	fi
	@echo "Starting services..."
	@trap 'kill %1; kill %2' INT; \
	$(VENV_BIN)/python main.py & \
	cd frontend && npm run dev & \
	wait

docker-build: ## Build Docker images
	@$(DOCKER_COMPOSE) build

docker-up: ## Start containers
	@echo "🐳 Starting containers..."
	@echo "Backend: http://localhost:8080"
	@echo "Frontend: http://localhost:8082"
	@$(DOCKER_COMPOSE) up

docker-down: ## Stop containers
	@$(DOCKER_COMPOSE) down

docker-logs: ## View logs
	@$(DOCKER_COMPOSE) logs -f

docker: ## Build and start (one command)
	@echo "🐳 Building and starting..."
	@$(DOCKER_COMPOSE) up --build

docker-debug: ## Start with ADK web interface (port 8081)
	@echo "🐳 Starting with ADK web interface..."
	@echo "Backend: http://localhost:8080"
	@echo "Frontend: http://localhost:8082"
	@echo "ADK Web: http://localhost:8081"
	@$(DOCKER_COMPOSE) --profile debug up --build

clean: ## Remove virtual environment
	@echo "Removing virtual environment..."
	@rm -rf venv
	@echo "Clean complete."