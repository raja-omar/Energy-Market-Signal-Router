# Energy Market Price Signal Router

A production-grade Python microservice that ingests electricity market price signals and routes them to trading algorithm consumers via Redis Pub/Sub.

## Features

- **REST API**: Accept external price signals via `POST /prices`
- **Market Simulator**: Generate realistic day-ahead and real-time electricity prices
- **Message-Passing Architecture**: Route signals to consumers via Redis
- **Battery Arbitrage Algorithm**: Charge when prices are low, discharge when high
- **Docker Compose**: Run Redis, ingestion API, and consumer with one command
- **Tests & CI**: Unit tests, integration tests, GitHub Actions

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (for full stack)
- Redis (or use Docker)

### Local Development

```bash
# Create virtualenv and install
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Copy env template (optional)
cp .env.example .env

# Run with Docker Compose (Redis + ingestion + consumer)
make up

# Or run services individually (Redis must be running):
# Terminal 1: redis-server
# Terminal 2: PYTHONPATH=src uvicorn signal_ingestion.api:app --reload
# Terminal 3: PYTHONPATH=src python -m trading_consumer.main
```

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Publish a price signal
curl -X POST http://localhost:8000/prices \
  -H "Content-Type: application/json" \
  -d '{"timestamp":"2025-06-15T12:00:00Z","market_type":"day-ahead","price_cents":35.5,"region":"CAISO"}'

# Generate and publish simulated signals (demo)
curl -X POST "http://localhost:8000/simulate?count=5"
```

### Run Tests

```bash
make test
# or: PYTHONPATH=src pytest tests/ -v
```

## Project Structure

```
energy-market-signal-router/
├── src/
│   ├── shared/           # Models, config, Redis client
│   ├── signal_ingestion/ # API, simulator, publisher
│   └── trading_consumer/ # Subscriber, arbitrage algorithm
├── tests/
├── terraform/            # IaC (placeholder for cloud Redis)
└── docs/
```

## License

MIT
