# 🐎 Hoof Hearted - Frontend Dockerfile (Vue.js)
# Multi-stage build for production optimization

# Stage 1: Build Vue.js application
FROM node:18-alpine AS build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build for production
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy built application
COPY --from=build /app/dist /usr/share/nginx/html

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