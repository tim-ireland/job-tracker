.PHONY: help build up down restart logs shell sync clean test

help:
	@echo "Job Search Toolkit - Make commands"
	@echo ""
	@echo "  make build      - Build Docker image"
	@echo "  make up         - Start application"
	@echo "  make down       - Stop application"
	@echo "  make restart    - Restart application"
	@echo "  make logs       - View logs"
	@echo "  make shell      - Open shell in container"
	@echo "  make sync       - Sync filesystem applications to database"
	@echo "  make clean      - Remove containers and images"
	@echo "  make test       - Run tests"
	@echo ""

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "✅ Application started at http://localhost:8000"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

shell:
	docker-compose exec job-tracker bash

sync:
	docker-compose exec job-tracker python scripts/sync_applications.py

clean:
	docker-compose down -v
	docker rmi job-search-toolkit:latest || true

test:
	pytest
