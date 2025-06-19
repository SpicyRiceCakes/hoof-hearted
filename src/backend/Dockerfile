# 🐎 Hoof Hearted - Backend Dockerfile (Python Flask)

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for monitoring and building Python packages
RUN apt-get update && apt-get install -y \
    curl \
    procps \
    psmisc \
    lsof \
    htop \
    gcc \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN groupadd -r hoofhearted && useradd -r -g hoofhearted hoofhearted
RUN chown -R hoofhearted:hoofhearted /app

# Switch to non-root user
USER hoofhearted

# Expose Flask port
EXPOSE 5000

# Add SpicyRiceCakes metadata
LABEL maintainer="SpicyRiceCakes <contact@spicyricecakes.com>"
LABEL description="Hoof Hearted - Home Server Monitoring Dashboard Backend"
LABEL version="1.0.0"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start Flask application
CMD ["python", "app.py"]