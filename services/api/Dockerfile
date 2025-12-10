FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY services/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared code
COPY shared /app/shared

# Copy service code
COPY services/api/src /app/src

# Set Python path
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run API service
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

