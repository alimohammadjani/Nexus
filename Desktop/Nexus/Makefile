.PHONY: help up down logs dev api web test build stress stress-headless stress-down

help:
	@echo "DevHub commands:"
	@echo "  make up               Start production Docker stack"
	@echo "  make down             Stop Docker stack"
	@echo "  make logs             Tail Docker logs"
	@echo "  make dev              Start dev stack (api + web + postgres)"
	@echo "  make api              Run backend locally with uvicorn"
	@echo "  make web              Run frontend locally with Vite"
	@echo "  make test             Run backend tests"
	@echo "  make build            Build frontend"
	@echo "  make stress           Start load-test stack (API + Locust UI on :8089)"
	@echo "  make stress-headless  Run Locust headless: 100 users, 20/s ramp, 2m"
	@echo "  make stress-down      Stop load-test stack"

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

stress:
	docker compose -f docker-compose.stress.yml up --build

stress-headless:
	docker compose -f docker-compose.stress.yml run --rm locust -f /mnt/locust/locustfile.py --host http://api:8000 --headless -u 100 -r 20 -t 2m

stress-down:
	docker compose -f docker-compose.stress.yml down
