#!/bin/bash

# 🐎 Hoof Hearted - One-Line Installation Script
# SpicyRiceCakes Home Server Monitoring Dashboard
#
# Usage: curl -sSL https://raw.githubusercontent.com/spicyricecakes/hoof-hearted/main/install.sh | bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# SpicyRiceCakes banner
echo -e "${PURPLE}"
echo "  🌶️🍚🍰 SpicyRiceCakes"
echo "  🐎 Hoof Hearted Server Monitor"
echo "  Answering 'Why is my GPU fan running?'"
echo -e "${NC}"

# Configuration
REPO_URL="https://github.com/spicyricecakes/hoof-hearted"
INSTALL_DIR="$HOME/hoof-hearted"
DEFAULT_PORT="0909"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    echo -e "${BLUE}💡 Visit: https://docs.docker.com/get-docker/${NC}"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not available. Please install Docker Compose.${NC}"
    exit 1
fi

# Use docker compose if available, fallback to docker-compose
DOCKER_COMPOSE_CMD="docker compose"
if ! docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
fi

echo -e "${BLUE}🔍 Checking system requirements...${NC}"

# Check available memory
AVAILABLE_MEMORY=$(free -m | awk 'NR==2{printf "%.0f", $7}')
if [ "$AVAILABLE_MEMORY" -lt 512 ]; then
    echo -e "${YELLOW}⚠️  Warning: Low available memory (${AVAILABLE_MEMORY}MB). Recommended: 512MB+${NC}"
fi

# Check available disk space
AVAILABLE_DISK=$(df -BM . | awk 'NR==2{sub(/M/,"",$4); print $4}')
if [ "$AVAILABLE_DISK" -lt 1024 ]; then
    echo -e "${YELLOW}⚠️  Warning: Low disk space (${AVAILABLE_DISK}MB). Recommended: 1GB+${NC}"
fi

echo -e "${GREEN}✅ System requirements check completed${NC}"

# Create installation directory
echo -e "${BLUE}📁 Creating installation directory...${NC}"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Download configuration files
echo -e "${BLUE}⬇️  Downloading configuration files...${NC}"

# Download docker-compose.yml
curl -sSL "$REPO_URL/raw/main/docker-compose.yml" -o docker-compose.yml

# Download .env.example
curl -sSL "$REPO_URL/raw/main/.env.example" -o .env.example

# Create .env from template if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${BLUE}⚙️  Creating environment configuration...${NC}"
    cp .env.example .env
    
    # Generate a random secret key
    SECRET_KEY=$(openssl rand -base64 32 2>/dev/null || dd if=/dev/urandom bs=32 count=1 2>/dev/null | base64)
    sed -i.bak "s/your-super-secret-key-change-this-in-production/$SECRET_KEY/" .env
    
    # Generate a random database password
    DB_PASSWORD=$(openssl rand -base64 16 2>/dev/null || dd if=/dev/urandom bs=16 count=1 2>/dev/null | base64 | tr -d '=+/')
    sed -i.bak "s/hoof_hearted_dev_change_me/$DB_PASSWORD/" .env
    
    rm -f .env.bak
    
    echo -e "${GREEN}✅ Configuration file created with secure random passwords${NC}"
else
    echo -e "${YELLOW}📝 Using existing .env configuration${NC}"
fi

# Check if port 0909 is available
if netstat -tuln 2>/dev/null | grep -q ":0909 "; then
    echo -e "${YELLOW}⚠️  Port 0909 is already in use. You may need to change DASHBOARD_PORT in .env${NC}"
fi

# Download deployment assets
echo -e "${BLUE}📦 Setting up deployment assets...${NC}"
mkdir -p deploy/{nginx,postgres}

# Download nginx configuration
curl -sSL "$REPO_URL/raw/main/deploy/nginx/nginx.conf" -o deploy/nginx/nginx.conf

# Download postgres initialization script
curl -sSL "$REPO_URL/raw/main/deploy/postgres/init.sql" -o deploy/postgres/init.sql

# Pull Docker images
echo -e "${BLUE}🐳 Pulling Docker images...${NC}"
$DOCKER_COMPOSE_CMD pull

# Start services
echo -e "${BLUE}🚀 Starting Hoof Hearted services...${NC}"
$DOCKER_COMPOSE_CMD up -d

# Wait for services to be healthy
echo -e "${BLUE}⏳ Waiting for services to start...${NC}"
sleep 10

# Check service health
if $DOCKER_COMPOSE_CMD ps | grep -q "healthy\|Up"; then
    DASHBOARD_PORT=$(grep DASHBOARD_PORT .env | cut -d'=' -f2 | tr -d '"' || echo "0909")
    
    echo -e "${GREEN}"
    echo "🎉 Hoof Hearted is now running!"
    echo ""
    echo "📊 Dashboard: http://localhost:${DASHBOARD_PORT}"
    echo "🔧 Configuration: $INSTALL_DIR/.env"
    echo "📁 Installation: $INSTALL_DIR"
    echo ""
    echo "🌶️ Powered by SpicyRiceCakes"
    echo -e "${NC}"
    
    echo -e "${BLUE}💡 Useful commands:${NC}"
    echo "  View logs:    cd $INSTALL_DIR && $DOCKER_COMPOSE_CMD logs -f"
    echo "  Stop:         cd $INSTALL_DIR && $DOCKER_COMPOSE_CMD down"
    echo "  Restart:      cd $INSTALL_DIR && $DOCKER_COMPOSE_CMD restart"
    echo "  Update:       cd $INSTALL_DIR && $DOCKER_COMPOSE_CMD pull && $DOCKER_COMPOSE_CMD up -d"
    
    # Optional: Open browser (macOS)
    if command -v open &> /dev/null; then
        echo -e "${BLUE}🌐 Opening dashboard in browser...${NC}"
        open "http://localhost:${DASHBOARD_PORT}"
    fi
    
else
    echo -e "${RED}❌ Some services failed to start. Check logs:${NC}"
    echo "  $DOCKER_COMPOSE_CMD logs"
    exit 1
fi