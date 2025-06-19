#!/bin/bash

# 🐎 Hoof Hearted - Dreams Deployment Script
# Deploy to David's RTX 4090 GPU workstation

set -e

echo "🐎 Starting Hoof Hearted deployment for Dreams..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if nvidia-docker is available
if ! docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi > /dev/null 2>&1; then
    print_warning "NVIDIA Docker runtime may not be available. GPU monitoring might be limited."
fi

# Copy Dreams environment file
if [ -f ".env.dreams" ]; then
    cp .env.dreams .env
    print_status "Using Dreams environment configuration"
else
    print_warning "No Dreams environment file found. Using defaults."
fi

# Stop any existing containers
print_status "Stopping existing containers..."
docker-compose -f docker-compose.dreams.yml down --remove-orphans 2>/dev/null || true

# Clean up old images (optional)
read -p "Do you want to rebuild images from scratch? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Removing old images..."
    docker-compose -f docker-compose.dreams.yml down --rmi all --volumes --remove-orphans 2>/dev/null || true
fi

# Build and start services
print_status "Building and starting Hoof Hearted services..."
docker-compose -f docker-compose.dreams.yml up --build -d

# Wait for services to be healthy
print_status "Waiting for services to be ready..."
sleep 10

# Check service health
check_service() {
    local service=$1
    local url=$2
    local timeout=60
    local count=0
    
    print_status "Checking $service health..."
    while [ $count -lt $timeout ]; do
        if curl -f -s "$url" > /dev/null 2>&1; then
            print_success "$service is healthy!"
            return 0
        fi
        sleep 2
        count=$((count + 2))
        printf "."
    done
    print_error "$service failed to become healthy within $timeout seconds"
    return 1
}

# Check backend health
if check_service "Backend API" "http://localhost:5001/health"; then
    print_success "Backend API is running on port 5001"
else
    print_error "Backend API health check failed"
    docker-compose -f docker-compose.dreams.yml logs backend
fi

# Check frontend health
if check_service "Frontend" "http://localhost:9090"; then
    print_success "Frontend is running on port 9090"
else
    print_error "Frontend health check failed"
    docker-compose -f docker-compose.dreams.yml logs frontend
fi

# Show running containers
print_status "Running containers:"
docker-compose -f docker-compose.dreams.yml ps

# Show GPU information if available
print_status "Checking GPU availability..."
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=name,temperature.gpu,utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits
else
    print_warning "nvidia-smi not available. GPU monitoring may be limited."
fi

# Final success message
echo ""
print_success "🐎 Hoof Hearted deployment completed!"
echo ""
echo "Access your monitoring dashboard at:"
echo "  🌐 Frontend: http://localhost:9090"
echo "  🔌 Backend API: http://localhost:5001"
echo "  🗄️  Database: localhost:5432"
echo ""
echo "Real-time monitoring features:"
echo "  ✅ GPU temperature and usage tracking"
echo "  ✅ Process identification ('Why is my GPU fan running?')"
echo "  ✅ WebSocket real-time updates"
echo "  ✅ System resource monitoring"
echo ""
echo "To view logs: docker-compose -f docker-compose.dreams.yml logs -f"
echo "To stop: docker-compose -f docker-compose.dreams.yml down"
echo ""
print_success "Happy monitoring! 🎮🔥"