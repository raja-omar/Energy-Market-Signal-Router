.PHONY: up down logs test install lint

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

test:
	PYTHONPATH=src pytest tests/ -v

install:
	pip install -r requirements.txt

lint:
	pip install ruff
	ruff check src/ tests/
