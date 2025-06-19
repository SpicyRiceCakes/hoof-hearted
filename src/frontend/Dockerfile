# 🐎 Hoof Hearted - Frontend Dockerfile (Magic Dashboard)
# Serves the integrated Magic dashboard with real API connections

FROM nginx:alpine

# Copy Magic dashboard directly
COPY public/index.html /usr/share/nginx/html/index.html

# Copy nginx configuration (will be mounted from host)
# Note: nginx.conf is mounted as volume in docker-compose.yml

# Create health check endpoint
RUN echo 'server { listen 8080; location /health { return 200 "healthy\n"; add_header Content-Type text/plain; } }' > /etc/nginx/conf.d/health.conf

# Expose port 80
EXPOSE 80

# Add SpicyRiceCakes metadata
LABEL maintainer="SpicyRiceCakes <contact@spicyricecakes.com>"
LABEL description="Hoof Hearted - Home Server Monitoring Dashboard Frontend"
LABEL version="1.0.0"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]