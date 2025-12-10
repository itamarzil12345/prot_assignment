FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY services/scraper/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared code
COPY shared /app/shared

# Copy service code (maintain structure for imports)
COPY services /app/services

# Set Python path
ENV PYTHONPATH=/app

# Run scraper service
CMD ["python", "-m", "services.scraper.src.main"]

