# Aesstore Makefile
# Simplifies common development and deployment tasks

.PHONY: help install dev up down restart logs test lint build clean docker-prune migrate seed db-shell db-reset db-backup db-restore

# Colors
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m

# Help
help:
	@echo "Aesstore Makefile - Available Commands"
	@echo ""
	@echo "$(GREEN)Development$(NC):"
	@echo "  make install      - Install all dependencies (backend + frontend)"
	@echo "  make dev          - Start development servers (backend + frontend)"
	@echo "  make up           - Start all services with Docker Compose"
	@echo "  make down         - Stop all services"
	@echo "  make restart      - Restart all services"
	@echo "  make logs         - Show logs for all services"
	@echo "  make logs-backend - Show backend logs"
	@echo "  make logs-frontend- Show frontend logs"
	@echo "  make logs-db      - Show database logs"
	@echo ""
	@echo "$(GREEN)Testing & Quality$(NC):"
	@echo "  make test         - Run all tests (backend + frontend)"
	@echo "  make test-backend - Run backend tests"
	@echo "  make test-frontend- Run frontend tests"
	@echo "  make lint         - Run all linters"
	@echo "  make lint-backend - Run backend linters"
	@echo "  make lint-frontend- Run frontend linters"
	@echo ""
	@echo "$(GREEN)Build & Deploy$(NC):"
	@echo "  make build        - Build Docker images"
	@echo "  make build-backend- Build backend Docker image"
	@echo "  make build-frontend- Build frontend Docker image"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make docker-prune - Remove unused Docker objects"
	@echo ""
	@echo "$(GREEN)Database$(NC):"
	@echo "  make migrate      - Run database migrations"
	@echo "  make seed        - Seed database with initial data"
	@echo "  make db-shell    - Open PostgreSQL shell"
	@echo "  make db-reset    - Reset database (WARNING: deletes all data!)"
	@echo "  make db-backup   - Create database backup"
	@echo "  make db-restore  - Restore database from backup"
	@echo ""
	@echo "$(GREEN)Production$(NC):"
	@echo "  make prod-up      - Start production services"
	@echo "  make prod-down    - Stop production services"
	@echo "  make prod-build  - Build production Docker images"

# Install dependencies
install:
	@echo "$(YELLOW)Installing backend dependencies...$(NC)"
	cd backend && pip install -r requirements.txt
	@echo "$(YELLOW)Installing frontend dependencies...$(NC)"
	cd frontend && npm install
	@echo "$(GREEN)Dependencies installed successfully!$(NC)"

# Development servers
dev:
	@echo "$(YELLOW)Starting development servers...$(NC)"
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "Press Ctrl+C to stop"
	@echo ""
	# Start backend in background
	cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
	BACKEND_PID=$$!
	# Start frontend
	cd frontend && npm run dev
	# Kill backend on exit
	kill $$BACKEND_PID

# Docker Compose commands
up:
	@echo "$(YELLOW)Starting services with Docker Compose...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)Services started!$(NC)"
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "PGAdmin: http://localhost:5050 (admin@aesstore.com / admin123)"
	@echo "MailHog: http://localhost:8025"
	down:
	@echo "$(YELLOW)Stopping services...$(NC)"
	docker-compose down

restart:
	@echo "$(YELLOW)Restarting services...$(NC)"
	docker-compose restart

logs:
	@echo "$(YELLOW)Showing logs for all services...$(NC)"
	docker-compose logs -f

logs-backend:
	@echo "$(YELLOW)Showing backend logs...$(NC)"
	docker-compose logs -f backend

logs-frontend:
	@echo "$(YELLOW)Showing frontend logs...$(NC)"
	docker-compose logs -f frontend

logs-db:
	@echo "$(YELLOW)Showing database logs...$(NC)"
	docker-compose logs -f db

# Testing
test:
	@echo "$(YELLOW)Running all tests...$(NC)"
	make test-backend
	make test-frontend

test-backend:
	@echo "$(YELLOW)Running backend tests...$(NC)"
	cd backend && python -m pytest tests/ --asyncio-mode=auto -v

test-frontend:
	@echo "$(YELLOW)Running frontend tests...$(NC)"
	cd frontend && npm test

# Linting
lint:
	@echo "$(YELLOW)Running all linters...$(NC)"
	make lint-backend
	make lint-frontend

lint-backend:
	@echo "$(YELLOW)Running backend linters...$(NC)"
	cd backend && black --check app/ tests/ && isort --check-only app/ tests/ && flake8 app/ tests/

lint-frontend:
	@echo "$(YELLOW)Running frontend linters...$(NC)"
	cd frontend && npm run lint && npm run type-check && npm run format:check

# Build
build:
	@echo "$(YELLOW)Building Docker images...$(NC)"
	make build-backend
	make build-frontend

build-backend:
	@echo "$(YELLOW)Building backend Docker image...$(NC)"
	docker build -t aesstore-backend -f Dockerfile .

build-frontend:
	@echo "$(YELLOW)Building frontend Docker image...$(NC)"
	docker build -t aesstore-frontend -f Dockerfile .

clean:
	@echo "$(YELLOW)Cleaning build artifacts...$(NC)"
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name "*.pyo" -delete 2>/dev/null || true
	find . -name "*.pyd" -delete 2>/dev/null || true
	cd frontend && rm -rf .next node_modules
	cd backend && rm -rf __pycache__ *.pyc
	docker-prune:
	@echo "$(YELLOW)Removing unused Docker objects...$(NC)"
	docker system prune -a -f --volumes

# Database operations
migrate:
	@echo "$(YELLOW)Running database migrations...$(NC)"
	cd backend && alembic upgrade head

seed:
	@echo "$(YELLOW)Seeding database...$(NC)"
	cd backend && python -m app.database.seed

db-shell:
	@echo "$(YELLOW)Opening PostgreSQL shell...$(NC)"
	docker-compose exec db psql -U user -d aesstore

db-reset:
	@echo "$(RED)WARNING: This will delete all data!$(NC)"
	@read -p "Are you sure? (y/N) " -n 1 -r; echo ""; if [ $$REPLY != "y" ]; then exit 1; fi
	@echo "$(YELLOW)Resetting database...$(NC)"
	docker-compose down -v
	docker-compose up -d db
	sleep 5
	cd backend && alembic upgrade head
	@echo "$(GREEN)Database reset complete!$(NC)"

db-backup:
	@echo "$(YELLOW)Creating database backup...$(NC)"
	@mkdir -p backups
	docker-compose exec db pg_dump -U user -d aesstore > backups/aesstore-$$(date +%Y%m%d-%H%M%S).sql
	@echo "$(GREEN)Backup created: backups/aesstore-$(date +%Y%m%d-%H%M%S).sql$(NC)"

db-restore:
	@echo "$(YELLOW)Restoring database from backup...$(NC)"
	@ls backups/*.sql | tail -1 | xargs -I {} sh -c 'echo "Restoring from: {}"; docker-compose exec db psql -U user -d aesstore < {}'
	@echo "$(GREEN)Database restored!$(NC)"

# Production
prod-up:
	@echo "$(YELLOW)Starting production services...$(NC)"
	docker-compose -f docker-compose.prod.yml up -d
	@echo "$(GREEN)Production services started!$(NC)"

prod-down:
	@echo "$(YELLOW)Stopping production services...$(NC)"
	docker-compose -f docker-compose.prod.yml down

prod-build:
	@echo "$(YELLOW)Building production Docker images...$(NC)"
	docker-compose -f docker-compose.prod.yml build
