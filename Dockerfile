# Multi-stage build for ingestion and consumer services
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY src/ ./src/

# Default: run ingestion API (override in docker-compose)
ENV PYTHONPATH=/app/src
CMD ["python", "-m", "uvicorn", "signal_ingestion.api:app", "--host", "0.0.0.0", "--port", "8000"]
