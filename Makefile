.PHONY: help install dev run test clean backup restore docker-build docker-up docker-down deploy health

# Variables
PYTHON := python3
PIP := pip3
VENV := venv
DOCKER_COMPOSE := docker-compose -f docker-compose.prod.yml

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)AI Building Materials Leasing Platform - Makefile Commands$(NC)"
	@echo "=========================================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	$(PYTHON) -m venv $(VENV)
	./$(VENV)/bin/$(PIP) install --upgrade pip
	./$(VENV)/bin/$(PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

dev: ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	./$(VENV)/bin/$(PIP) install -r requirements.txt
	./$(VENV)/bin/$(PIP) install pytest pytest-cov black flake8 mypy
	@echo "$(GREEN)✓ Development dependencies installed$(NC)"

run: ## Run the application in development mode
	@echo "$(BLUE)Starting application...$(NC)"
	./$(VENV)/bin/$(PYTHON) main.py

run-prod: ## Run the application with gunicorn
	@echo "$(BLUE)Starting application with gunicorn...$(NC)"
	./$(VENV)/bin/gunicorn -c gunicorn_config.py main:app

test: ## Run tests
	@echo "$(BLUE)Running tests...$(NC)"
	./$(VENV)/bin/$(PYTHON) test_api.py

examples: ## Run example scripts
	@echo "$(BLUE)Running examples...$(NC)"
	./$(VENV)/bin/$(PYTHON) examples.py

clean: ## Clean up generated files
	@echo "$(BLUE)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf htmlcov/ .pytest_cache/ .coverage
	rm -f *.log
	@echo "$(GREEN)✓ Cleaned up$(NC)"

format: ## Format code with black
	@echo "$(BLUE)Formatting code...$(NC)"
	./$(VENV)/bin/black .
	@echo "$(GREEN)✓ Code formatted$(NC)"

lint: ## Lint code with flake8
	@echo "$(BLUE)Linting code...$(NC)"
	./$(VENV)/bin/flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	@echo "$(GREEN)✓ Linting complete$(NC)"

backup: ## Backup database and configuration
	@echo "$(BLUE)Running backup...$(NC)"
	chmod +x backup.sh
	./backup.sh
	@echo "$(GREEN)✓ Backup complete$(NC)"

restore: ## Restore from backup
	@echo "$(YELLOW)Starting restore process...$(NC)"
	chmod +x restore.sh
	./restore.sh

docker-build: ## Build Docker image
	@echo "$(BLUE)Building Docker image...$(NC)"
	docker build -t ai-leasing-platform:latest .
	@echo "$(GREEN)✓ Docker image built$(NC)"

docker-up: ## Start Docker containers
	@echo "$(BLUE)Starting Docker containers...$(NC)"
	$(DOCKER_COMPOSE) up -d --build
	@echo "$(GREEN)✓ Containers started$(NC)"
	@echo "$(YELLOW)Application: http://localhost$(NC)"
	@echo "$(YELLOW)Prometheus: http://localhost:9090$(NC)"
	@echo "$(YELLOW)Grafana: http://localhost:3000$(NC)"

docker-down: ## Stop Docker containers
	@echo "$(BLUE)Stopping Docker containers...$(NC)"
	$(DOCKER_COMPOSE) down
	@echo "$(GREEN)✓ Containers stopped$(NC)"

docker-logs: ## View Docker logs
	$(DOCKER_COMPOSE) logs -f

docker-ps: ## List Docker containers
	$(DOCKER_COMPOSE) ps

docker-restart: ## Restart Docker containers
	@echo "$(BLUE)Restarting Docker containers...$(NC)"
	$(DOCKER_COMPOSE) restart
	@echo "$(GREEN)✓ Containers restarted$(NC)"

pre-deploy: ## Run pre-deployment checks
	@echo "$(BLUE)Running pre-deployment checks...$(NC)"
	chmod +x pre-deploy-check.sh
	./pre-deploy-check.sh

deploy: pre-deploy docker-up ## Deploy to production
	@echo "$(GREEN)✓ Deployment complete$(NC)"

health: ## Check application health
	@echo "$(BLUE)Checking application health...$(NC)"
	@curl -s http://localhost:8000/api/health | python3 -m json.tool || echo "$(YELLOW)Application not responding$(NC)"

metrics: ## View application metrics
	@echo "$(BLUE)Fetching application metrics...$(NC)"
	@curl -s http://localhost:8000/api/metrics | python3 -m json.tool || echo "$(YELLOW)Metrics not available$(NC)"

k8s-deploy: ## Deploy to Kubernetes
	@echo "$(BLUE)Deploying to Kubernetes...$(NC)"
	kubectl apply -f k8s-deployment.yaml
	@echo "$(GREEN)✓ Kubernetes deployment complete$(NC)"

k8s-status: ## Check Kubernetes deployment status
	@echo "$(BLUE)Kubernetes status:$(NC)"
	kubectl get pods -n ai-leasing-platform
	kubectl get services -n ai-leasing-platform

k8s-logs: ## View Kubernetes logs
	kubectl logs -f -n ai-leasing-platform -l app=ai-leasing-platform

k8s-delete: ## Delete Kubernetes deployment
	@echo "$(YELLOW)Deleting Kubernetes deployment...$(NC)"
	kubectl delete -f k8s-deployment.yaml

init-db: ## Initialize database with sample data
	@echo "$(BLUE)Initializing database...$(NC)"
	./$(VENV)/bin/$(PYTHON) -c "from main import create_app; app = create_app(); app.app_context().push(); from app.models import db; db.create_all(); print('Database initialized')"
	@echo "$(GREEN)✓ Database initialized$(NC)"

reset-db: ## Reset database (WARNING: deletes all data)
	@echo "$(YELLOW)WARNING: This will delete all data!$(NC)"
	@read -p "Type 'yes' to continue: " confirm && [ "$$confirm" = "yes" ] || exit 1
	rm -f materials_leasing.db data/leasing_platform.db
	$(MAKE) init-db
	@echo "$(GREEN)✓ Database reset$(NC)"

version: ## Show version information
	@echo "$(BLUE)AI Building Materials Leasing Platform$(NC)"
	@echo "Version: 1.0.0"
	@echo "Python: $$($(PYTHON) --version)"
	@echo "Docker: $$(docker --version 2>/dev/null || echo 'Not installed')"

setup: install init-db ## Complete setup (install + init database)
	@echo "$(GREEN)✓ Setup complete!$(NC)"
	@echo "$(YELLOW)Run 'make run' to start the application$(NC)"

all: clean install test ## Run all tasks

.DEFAULT_GOAL := help
