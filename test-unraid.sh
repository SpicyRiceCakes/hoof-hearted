#!/bin/bash

# 🐎 Quick Test Script for Hoof Hearted Unraid Container

echo "🐎 Testing Hoof Hearted Unraid container..."

BASE_URL="http://localhost:9091"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

test_endpoint() {
    local endpoint=$1
    local description=$2
    
    echo -n "Testing $description... "
    
    if curl -f -s "$BASE_URL$endpoint" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ OK${NC}"
    else
        echo -e "${RED}❌ FAILED${NC}"
    fi
}

echo ""
echo "🌐 Frontend Tests:"
test_endpoint "/" "Vue.js Magic Dashboard"
test_endpoint "/health" "Health endpoint"

echo ""
echo "🔌 Backend API Tests:"
test_endpoint "/api/health" "API Health"
test_endpoint "/api/status" "System Status"
test_endpoint "/api/system/overview" "System Overview"
test_endpoint "/api/gpu/summary" "GPU Summary"

echo ""
echo "📊 Container Status:"
docker-compose -f docker-compose.unraid.yml ps

echo ""
echo "🐎 Test completed!"
echo "Dashboard: $BASE_URL"