.PHONY: help up down logs dev api web test build

help:
	@echo "DevHub commands:"
	@echo "  make up       Start production Docker stack"
	@echo "  make down     Stop Docker stack"
	@echo "  make logs     Tail Docker logs"
	@echo "  make dev      Start dev stack (api + web + postgres)"
	@echo "  make api      Run backend locally with uvicorn"
	@echo "  make web      Run frontend locally with Vite"
	@echo "  make test     Run backend tests"

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

dev:
	docker compose -f docker-compose.dev.yml up --build

api:
	cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

web:
	cd frontend && npm run dev

test:
	cd backend && python -m pytest -q

build:
	cd frontend && npm run build
