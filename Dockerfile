# Multi-stage build for Hoof Hearted monitoring application
FROM node:18-alpine AS frontend-builder

# Build Vue.js frontend
WORKDIR /app/frontend
COPY src/frontend/package*.json ./
RUN npm ci
COPY src/frontend/ ./
RUN npm run build

# Python backend stage
FROM python:3.11-slim AS backend

# Install system dependencies for monitoring
RUN apt-get update && apt-get install -y \
    curl \
    procps \
    htop \
    gcc \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy backend requirements and install Python dependencies
COPY src/backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY src/backend/ ./backend/

# Copy built frontend assets
COPY --from=frontend-builder /app/frontend/dist ./static/

# Create directories for data persistence
RUN mkdir -p /app/data /app/database /app/config /app/logs

# Set environment variables
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV PORT=3000

# Expose ports
EXPOSE 3000 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Starting Hoof Hearted monitoring application..."\n\
echo "Backend starting on port 5000..."\n\
python backend/app.py &\n\
echo "Frontend serving on port 3000..."\n\
python -m http.server 3000 --directory static &\n\
wait\n\
' > /app/start.sh && chmod +x /app/start.sh

# Start both services
CMD ["/app/start.sh"]