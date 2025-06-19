#!/bin/bash

# 🐎 Hoof Hearted - Unraid Test Deployment Script
# Tests the Docker container locally before Unraid deployment

set -e

echo "🐎 Hoof Hearted - Testing Unraid Docker Container"
echo "=================================================="

# Configuration
CONTAINER_NAME="hoof-hearted-unraid-test"
IMAGE_NAME="hoof-hearted-unraid:latest"
TEST_PORT="9095"
DATA_DIR="/tmp/hoof-hearted-test-data"

# Clean up existing test container
echo "🧹 Cleaning up existing test containers..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Create test data directory
echo "📁 Creating test data directory..."
mkdir -p $DATA_DIR

# Build the Docker image
echo "🔨 Building Docker image..."
docker build -f Dockerfile.unraid.new -t $IMAGE_NAME .

# Run the container
echo "🚀 Starting test container..."
docker run -d \
  --name $CONTAINER_NAME \
  -p $TEST_PORT:80 \
  -v $DATA_DIR:/app/data \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -e FLASK_ENV=production \
  -e GPU_MONITORING_ENABLED=true \
  -e SYSTEM_MONITORING_ENABLED=true \
  -e ENABLE_PROCESS_MONITORING=true \
  -e LOG_LEVEL=INFO \
  -e CUSTOM_TITLE="Hoof Hearted - Test Environment" \
  $IMAGE_NAME

# Wait for container to start
echo "⏳ Waiting for container to start..."
sleep 10

# Check container status
echo "🔍 Checking container status..."
docker logs $CONTAINER_NAME --tail 20

# Test frontend
echo "🌐 Testing frontend accessibility..."
if curl -f http://localhost:$TEST_PORT >/dev/null 2>&1; then
    echo "✅ Frontend is accessible at http://localhost:$TEST_PORT"
else
    echo "❌ Frontend test failed"
    exit 1
fi

# Test API
echo "🔧 Testing API accessibility..."
if curl -f http://localhost:$TEST_PORT/api/status >/dev/null 2>&1; then
    echo "✅ API is accessible at http://localhost:$TEST_PORT/api/status"
else
    echo "❌ API test failed"
    exit 1
fi

# Show API response
echo "📊 API Status Response:"
curl -s http://localhost:$TEST_PORT/api/status | python3 -m json.tool || echo "API response received"

echo ""
echo "🎉 Test deployment successful!"
echo "📱 Access your Hoof Hearted dashboard at: http://localhost:$TEST_PORT"
echo "🔧 API endpoint: http://localhost:$TEST_PORT/api/status"
echo "📝 Container logs: docker logs $CONTAINER_NAME"
echo "🛑 Stop test: docker stop $CONTAINER_NAME && docker rm $CONTAINER_NAME"
echo ""
echo "🌶️ Ready for Unraid deployment! Use the template in deploy/unraid/hoof-hearted-template.xml"