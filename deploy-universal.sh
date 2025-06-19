#!/bin/bash

# 🐎 Hoof Hearted - Universal Multi-Platform Deployment
# Supports: Linux (Asus/Intel), macOS (Intel/Apple Silicon)
# Auto-detects: NVIDIA, AMD, Intel GPU, or CPU-only monitoring

set -e

echo "🐎 Hoof Hearted Universal Deployment"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Functions
print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_platform() { echo -e "${PURPLE}[PLATFORM]${NC} $1"; }

# Detect platform
detect_platform() {
    local os=$(uname -s)
    local arch=$(uname -m)
    
    case "$os" in
        Linux*)
            if [ -f /proc/version ]; then
                if grep -qi "asus" /proc/version 2>/dev/null || lscpu | grep -qi "asus" 2>/dev/null; then
                    PLATFORM="linux-asus"
                    print_platform "Detected: Linux on Asus hardware"
                elif lscpu | grep -qi "intel" 2>/dev/null; then
                    PLATFORM="linux-intel"
                    print_platform "Detected: Linux on Intel hardware"
                else
                    PLATFORM="linux-generic"
                    print_platform "Detected: Linux (generic)"
                fi
            else
                PLATFORM="linux-generic"
                print_platform "Detected: Linux (generic)"
            fi
            ;;
        Darwin*)
            if [[ "$arch" == "arm64" ]]; then
                PLATFORM="macos-apple-silicon"
                print_platform "Detected: macOS on Apple Silicon"
            else
                PLATFORM="macos-intel"
                print_platform "Detected: macOS on Intel"
            fi
            ;;
        *)
            PLATFORM="unknown"
            print_warning "Unknown platform: $os"
            ;;
    esac
    
    echo "Architecture: $arch"
}

# Detect GPU
detect_gpu() {
    print_status "Detecting GPU capabilities..."
    
    GPU_TYPE="none"
    GPU_SUPPORT=""
    
    # NVIDIA detection
    if command -v nvidia-smi >/dev/null 2>&1; then
        GPU_TYPE="nvidia"
        GPU_INFO=$(nvidia-smi --query-gpu=name,driver_version --format=csv,noheader,nounits)
        print_success "NVIDIA GPU detected: $GPU_INFO"
        GPU_SUPPORT="--gpus all"
    # AMD detection (Linux)
    elif command -v rocm-smi >/dev/null 2>&1; then
        GPU_TYPE="amd"
        print_success "AMD GPU detected (ROCm support)"
    elif lspci 2>/dev/null | grep -i "amd\|radeon" >/dev/null; then
        GPU_TYPE="amd"
        print_success "AMD GPU detected (basic support)"
    # Intel GPU detection
    elif lspci 2>/dev/null | grep -i "intel.*graphics\|intel.*vga" >/dev/null; then
        GPU_TYPE="intel"
        print_success "Intel GPU detected"
    # macOS Metal detection
    elif [[ "$PLATFORM" == "macos-"* ]] && system_profiler SPDisplaysDataType 2>/dev/null | grep -i "metal" >/dev/null; then
        GPU_TYPE="metal"
        print_success "Metal GPU support detected on macOS"
    else
        print_warning "No dedicated GPU detected - CPU monitoring only"
    fi
    
    export GPU_TYPE
}

# Check dependencies
check_dependencies() {
    print_status "Checking dependencies..."
    
    # Docker
    if ! command -v docker >/dev/null 2>&1; then
        print_error "Docker not found. Please install Docker first."
        exit 1
    fi
    
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker."
        exit 1
    fi
    print_success "Docker is ready"
    
    # Docker Compose
    if ! command -v docker-compose >/dev/null 2>&1; then
        print_warning "docker-compose not found, using 'docker compose'"
        COMPOSE_CMD="docker compose"
    else
        COMPOSE_CMD="docker-compose"
    fi
    print_success "Docker Compose available: $COMPOSE_CMD"
}

# Select deployment configuration
select_config() {
    print_status "Selecting deployment configuration..."
    
    case "$PLATFORM" in
        "linux-asus"|"linux-intel"|"linux-generic")
            if [ "$GPU_TYPE" = "nvidia" ]; then
                CONFIG_FILE="docker-compose.dreams.yml"
                PORT="9090"
                print_success "Using Dreams config (Linux + NVIDIA)"
            else
                CONFIG_FILE="docker-compose.unraid.yml"
                PORT="9091"
                print_success "Using Unraid config (Linux + non-NVIDIA)"
            fi
            ;;
        "macos-"*)
            CONFIG_FILE="docker-compose.unraid.yml"
            PORT="9091"
            print_success "Using Unraid config (macOS compatible)"
            ;;
        *)
            CONFIG_FILE="docker-compose.unraid.yml"
            PORT="9091"
            print_warning "Using default Unraid config"
            ;;
    esac
}

# Create platform-specific env file
create_env_file() {
    print_status "Creating platform-specific environment..."
    
    cat > .env.platform << EOF
# Auto-generated platform configuration
PLATFORM=$PLATFORM
GPU_TYPE=$GPU_TYPE
COMPOSE_PROJECT_NAME=hoof-hearted-$PLATFORM
DASHBOARD_PORT=$PORT

# Platform optimizations
FLASK_ENV=production
NODE_ENV=production
GPU_MONITORING_ENABLED=true
SYSTEM_MONITORING_ENABLED=true
ENABLE_PROCESS_MONITORING=true
LOG_LEVEL=INFO

# Platform-specific settings
$(case "$PLATFORM" in
    "linux-"*)
        echo "ENABLE_DOCKER_MONITORING=true"
        echo "ENABLE_HARDWARE_MONITORING=true"
        ;;
    "macos-"*)
        echo "ENABLE_DOCKER_MONITORING=false"
        echo "ENABLE_HARDWARE_MONITORING=false"
        ;;
esac)

# GPU-specific settings
$(case "$GPU_TYPE" in
    "nvidia")
        echo "NVIDIA_VISIBLE_DEVICES=all"
        echo "GPU_VENDOR=nvidia"
        ;;
    "amd")
        echo "GPU_VENDOR=amd"
        ;;
    "intel")
        echo "GPU_VENDOR=intel"
        ;;
    "metal")
        echo "GPU_VENDOR=apple"
        ;;
    *)
        echo "GPU_VENDOR=none"
        ;;
esac)
EOF

    print_success "Environment configured for $PLATFORM with $GPU_TYPE GPU"
}

# Deploy container
deploy_container() {
    print_status "Deploying Hoof Hearted container..."
    
    # Stop existing containers
    $COMPOSE_CMD -f $CONFIG_FILE --env-file .env.platform down --remove-orphans 2>/dev/null || true
    
    # Build and start
    print_status "Building multi-platform container..."
    if [ "$GPU_TYPE" = "nvidia" ] && [ ! -z "$GPU_SUPPORT" ]; then
        print_status "Enabling NVIDIA GPU support..."
        $COMPOSE_CMD -f $CONFIG_FILE --env-file .env.platform up --build -d
    else
        $COMPOSE_CMD -f $CONFIG_FILE --env-file .env.platform up --build -d
    fi
    
    # Wait for startup
    print_status "Waiting for services to start..."
    sleep 15
}

# Test deployment
test_deployment() {
    print_status "Testing deployment..."
    
    local base_url="http://localhost:$PORT"
    
    # Test frontend
    if curl -f -s "$base_url" >/dev/null 2>&1; then
        print_success "✅ Frontend accessible at $base_url"
    else
        print_error "❌ Frontend not accessible"
        return 1
    fi
    
    # Test API
    if curl -f -s "$base_url/api/health" >/dev/null 2>&1; then
        print_success "✅ Backend API responding"
    else
        print_error "❌ Backend API not responding"
        return 1
    fi
    
    # Test platform-specific endpoints
    if curl -f -s "$base_url/api/status" >/dev/null 2>&1; then
        print_success "✅ Platform status endpoint working"
        
        # Show platform info
        local status=$(curl -s "$base_url/api/status" | grep -o '"platform":"[^"]*"' | cut -d'"' -f4)
        print_platform "Backend reports platform: $status"
    fi
    
    return 0
}

# Show deployment info
show_deployment_info() {
    echo ""
    print_success "🐎 Hoof Hearted deployed successfully!"
    echo ""
    echo "📊 Dashboard: http://localhost:$PORT"
    echo "🔌 Backend API: http://localhost:$PORT/api/"
    echo "🖥️  Platform: $PLATFORM"
    echo "🎮 GPU: $GPU_TYPE"
    echo ""
    echo "✨ Features available:"
    echo "  🎨 Vue.js Magic Dashboard"
    echo "  📊 Real-time system monitoring"
    case "$GPU_TYPE" in
        "nvidia") echo "  🎮 NVIDIA GPU monitoring with CUDA support" ;;
        "amd") echo "  🎮 AMD GPU monitoring" ;;
        "intel") echo "  🎮 Intel GPU monitoring" ;;
        "metal") echo "  🎮 Apple Metal GPU support" ;;
        *) echo "  💻 CPU monitoring (no dedicated GPU)" ;;
    esac
    echo "  🔍 Process identification"
    echo "  📡 WebSocket real-time updates"
    echo "  🌙 Dark/Light theme toggle"
    echo ""
    echo "📋 Management commands:"
    echo "  View logs: $COMPOSE_CMD -f $CONFIG_FILE --env-file .env.platform logs -f"
    echo "  Stop: $COMPOSE_CMD -f $CONFIG_FILE --env-file .env.platform down"
    echo "  Restart: $COMPOSE_CMD -f $CONFIG_FILE --env-file .env.platform restart"
    echo ""
    print_success "Happy monitoring! 🚀"
}

# Main execution
main() {
    detect_platform
    detect_gpu
    check_dependencies
    select_config
    create_env_file
    deploy_container
    
    if test_deployment; then
        show_deployment_info
    else
        print_error "Deployment test failed. Check logs:"
        echo "$COMPOSE_CMD -f $CONFIG_FILE --env-file .env.platform logs"
        exit 1
    fi
}

# Run main function
main "$@"