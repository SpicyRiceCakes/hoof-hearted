#!/bin/bash

# 🐎 Hoof Hearted - Unraid Deployment Script
# Test deployment with Vue.js Magic Dashboard + Real API integration

set -e

echo "🐎 Starting Hoof Hearted deployment for Unraid testing..."

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

# Stop any existing Unraid test containers
print_status "Stopping existing Unraid test containers..."
docker-compose -f docker-compose.unraid.yml down --remove-orphans 2>/dev/null || true

# Check if we should rebuild
read -p "Do you want to rebuild the container from scratch? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Removing old container and images..."
    docker-compose -f docker-compose.unraid.yml down --rmi all --volumes --remove-orphans 2>/dev/null || true
fi

# Build and start the Unraid container
print_status "Building Hoof Hearted Unraid container..."
print_status "This includes:"
print_status "  📦 Vue.js Magic Dashboard with Tailwind v3"
print_status "  🔌 Flask Backend with real API endpoints"
print_status "  🌐 Nginx proxy for SPA routing"
print_status "  📊 Real-time WebSocket monitoring"

docker-compose -f docker-compose.unraid.yml up --build -d

# Wait for container to be ready
print_status "Waiting for container to be ready..."
sleep 15

# Check container health
print_status "Checking container health..."
if docker-compose -f docker-compose.unraid.yml ps | grep -q "healthy"; then
    print_success "Container is healthy!"
else
    print_warning "Container health check may still be running..."
fi

# Test the endpoints
print_status "Testing endpoints..."

# Test frontend
if curl -f -s "http://localhost:9091" > /dev/null 2>&1; then
    print_success "✅ Frontend is accessible at http://localhost:9091"
else
    print_error "❌ Frontend not accessible"
fi

# Test backend health
if curl -f -s "http://localhost:9091/api/health" > /dev/null 2>&1; then
    print_success "✅ Backend API is responding"
else
    print_error "❌ Backend API not responding"
fi

# Test backend status
if curl -f -s "http://localhost:9091/api/status" > /dev/null 2>&1; then
    print_success "✅ Backend status endpoint working"
else
    print_error "❌ Backend status endpoint not working"
fi

# Show container logs snippet
print_status "Recent container logs:"
docker-compose -f docker-compose.unraid.yml logs --tail=10 hoof-hearted

# Show container status
print_status "Container status:"
docker-compose -f docker-compose.unraid.yml ps

# Check if GPU monitoring is available
print_status "Checking GPU monitoring capability..."
if command -v nvidia-smi &> /dev/null; then
    print_success "NVIDIA GPU detected:"
    nvidia-smi --query-gpu=name,temperature.gpu,utilization.gpu --format=csv,noheader,nounits
else
    print_warning "No NVIDIA GPU detected. CPU-only monitoring will be available."
fi

# Final success message
echo ""
print_success "🐎 Hoof Hearted Unraid container deployed successfully!"
echo ""
echo "🌐 Dashboard URL: http://localhost:9091"
echo ""
echo "✨ Features available:"
echo "  🎨 Vue.js Magic Dashboard (converted from React)"
echo "  📊 Real-time system monitoring"
echo "  🎮 GPU monitoring (if available)"
echo "  🔍 Process identification"
echo "  📡 WebSocket live updates"
echo "  🌙 Dark/Light theme toggle"
echo "  📱 Mobile-responsive design"
echo ""
echo "📋 Useful commands:"
echo "  View logs: docker-compose -f docker-compose.unraid.yml logs -f"
echo "  Stop container: docker-compose -f docker-compose.unraid.yml down"
echo "  Restart container: docker-compose -f docker-compose.unraid.yml restart"
echo ""
print_success "Ready for Unraid deployment testing! 🚀"