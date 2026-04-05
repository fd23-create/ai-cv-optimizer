# Multi-stage build for Python Flask ML service
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies only when needed
FROM base AS deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy models
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download fr_core_news_sm
RUN python -m spacy download es_core_news_sm
RUN python -m spacy download de_core_news_sm
RUN python -m spacy download it_core_news_sm
RUN python -m spacy download pt_core_news_sm

# Development stage
FROM base AS development
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm
COPY . .
RUN mkdir -p logs uploads models
EXPOSE 5001
CMD ["python", "src/app.py"]

# Production stage
FROM base AS production
WORKDIR /app

# Create non-root user
RUN groupadd -r flask && useradd -r -g flask flask

# Copy dependencies and models
COPY --from=deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin
COPY --chown=flask:flask . .

# Create necessary directories
RUN mkdir -p logs uploads models && chown -R flask:flask logs uploads models

# Switch to non-root user
USER flask

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5001/health || exit 1

EXPOSE 5001

# Use Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "4", "--timeout", "120", "--keepalive", "2", "--max-requests", "1000", "--max-requests-jitter", "50", "src.app:app"]
