#!/bin/bash

# 🐎 Test Hoof Hearted API Connection for Dreams
# Quick test script to verify backend APIs are working

echo "🐎 Testing Hoof Hearted API connections..."

BASE_URL="http://localhost:5001"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

test_endpoint() {
    local endpoint=$1
    local description=$2
    
    echo -n "Testing $description... "
    
    if response=$(curl -s -w "%{http_code}" "$BASE_URL$endpoint" 2>/dev/null); then
        http_code="${response: -3}"
        body="${response%???}"
        
        if [ "$http_code" -eq 200 ]; then
            echo -e "${GREEN}✅ SUCCESS${NC}"
            if [ "$3" = "verbose" ]; then
                echo "Response: $body" | jq . 2>/dev/null || echo "Response: $body"
            fi
        else
            echo -e "${RED}❌ FAILED (HTTP $http_code)${NC}"
        fi
    else
        echo -e "${RED}❌ CONNECTION FAILED${NC}"
    fi
}

echo ""
echo "🔍 API Health Checks:"
test_endpoint "/health" "Basic Health Check" verbose
test_endpoint "/api/health" "API Health Check" verbose
test_endpoint "/api/status" "System Status" verbose

echo ""
echo "🖥️ System Monitoring Endpoints:"
test_endpoint "/api/system/overview" "System Overview"
test_endpoint "/api/system/cpu" "CPU Metrics"
test_endpoint "/api/system/memory" "Memory Metrics"
test_endpoint "/api/system/disk" "Disk Metrics"

echo ""
echo "🎮 GPU Monitoring Endpoints:"
test_endpoint "/api/gpu/summary" "GPU Summary"
test_endpoint "/api/gpu/metrics" "GPU Metrics"
test_endpoint "/api/gpu/processes" "GPU Processes" verbose

echo ""
echo "⚡ Real-time Monitoring:"
test_endpoint "/api/monitoring/stats" "Monitoring Stats"

echo ""
echo "🌐 Testing Frontend Connection:"
if curl -s "http://localhost:9090" > /dev/null 2>&1; then
    echo -e "Frontend (http://localhost:9090): ${GREEN}✅ ACCESSIBLE${NC}"
else
    echo -e "Frontend (http://localhost:9090): ${RED}❌ NOT ACCESSIBLE${NC}"
fi

echo ""
echo "🐎 API test completed!"