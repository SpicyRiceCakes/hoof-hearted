# 🐎 Hoof Hearted - Docker Architecture

**Docker-first development approach based on src-brain best practices.**

## 🚀 Quick Start

```bash
# Start the complete application stack
npm run dev

# View logs from all services
npm run logs

# Stop all services
npm run down
```

Access the dashboard at **http://localhost:0909** (Korean fart humor port! 공구공구)

## 🏗️ Architecture Overview

### Multi-Stage Docker Setup

Our Docker configuration follows **src-brain advanced testing methodology** with:

1. **Production Stack** (`docker-compose.yml`) - Optimized for deployment
2. **Testing Stack** (`docker-compose.test.yml`) - External testing architecture
3. **Multi-Stage Builds** (`Dockerfile.test`) - Development and production targets

### Service Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Frontend      │────▶│   Backend API   │────▶│   PostgreSQL    │
│   Vue.js/Nginx  │     │   Flask/Python  │     │   Database      │
│   Port: 0909    │     │   Port: 5001    │     │   Port: 5432    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## 🛠️ Development Workflow

### Docker-First Development (Recommended)

**Instead of `npm run dev`, use Docker:**

```bash
# Start development environment
npm run dev

# Monitor all services
npm run logs

# Check service status
npm run status

# Health check all services
npm run health
```

### Why Docker-First?

Based on **src-brain methodology**:
- ✅ **Unified logging** across all services
- ✅ **Production parity** from day one
- ✅ **Easy debugging** with MCP Docker tools
- ✅ **Multi-container orchestration** for complex monitoring

## 🧪 Testing Architecture

### External Testing Approach

**Philosophy**: App runs in Docker, tests run on host machine.

```
┌─────────────────┐    HTTP Requests    ┌─────────────────┐
│   Host Machine  │ ─────────────────► │ Docker Container│
│                 │                     │                 │
│ ↳ Playwright    │                     │ ↳ Hoof Hearted │
│ ↳ Test Runner   │                     │ ↳ Port Mapped   │
│ ↳ Local Browsers│                     │                 │
└─────────────────┘                     └─────────────────┘
      localhost                              localhost:5174
```

### Testing Commands

```bash
# Development testing
npm run test:dev         # Start dev containers
npm run test             # Run Playwright tests
npm run test:down        # Stop test containers

# Production testing
npm run test:prod        # Start prod containers
npm run test:quick       # Quick test run
npm run test:down        # Stop test containers

# Full pipeline test
npm run test:full-pipeline

# Interactive testing
npm run test:ui          # Playwright UI mode
npm run test:debug       # Debug failing tests
```

### Test Configuration

- **Frontend Tests**: `src/frontend/tests/` (Playwright)
- **Configuration**: `src/frontend/playwright.config.ts`
- **Test Ports**: Dev (5174), Prod (8081)

## 📁 File Structure

```
/
├── docker-compose.yml              # Production stack
├── docker-compose.test.yml         # Testing stack
├── Dockerfile.test                 # Multi-stage builds
├── package.json                    # Root-level Docker commands
│
├── src/
│   ├── frontend/
│   │   ├── Dockerfile              # Frontend production build
│   │   ├── package.json            # Enhanced with Docker scripts
│   │   ├── playwright.config.ts    # External testing config
│   │   └── tests/                  # Playwright test suite
│   │
│   └── backend/
│       ├── Dockerfile              # Backend production build
│       └── requirements.txt        # Python dependencies
│
└── deploy/
    ├── nginx/                      # Nginx configuration
    └── postgres/                   # Database initialization
```

## 🌐 Port Configuration

### Production Ports
- **Frontend**: `0909` (Korean humor: 공구공구)
- **Backend**: `5001` (Avoids macOS AirPlay port 5000)
- **Database**: `5432` (Standard PostgreSQL)

### Testing Ports
- **Frontend Dev**: `5174`
- **Frontend Prod**: `8081`
- **Backend Dev**: `5002`
- **Backend Prod**: `5003`
- **Test Database**: `5433`

## 🔧 Docker Commands Reference

### Development Commands
```bash
npm run dev              # Start all services
npm run down             # Stop all services
npm run logs             # View all logs
npm run clean            # Complete cleanup
```

### Testing Commands
```bash
npm run test:dev         # Start test environment
npm run test             # Run tests
npm run test:quick       # Quick test (Chrome only)
npm run test:mobile      # Mobile testing
npm run test:report      # View test results
```

### Maintenance Commands
```bash
npm run status           # Check container status
npm run health           # Health check all services
npm run frontend:install # Install frontend deps
npm run backend:install  # Install backend deps
npm run install:all      # Install all dependencies
```

## 🚨 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Check what's using port 0909
lsof -i :0909
# Kill process if needed
kill -9 <PID>
```

**2. Docker Build Issues**
```bash
# Clean Docker cache
npm run clean
# Force rebuild
npm run dev
```

**3. Container Health Issues**
```bash
# Check container logs
npm run logs
# Or specific service
docker logs hoof-hearted-backend
```

**4. GPU Access Issues**
```bash
# Uncomment GPU device mappings in docker-compose.yml
# Only on systems with NVIDIA GPUs
```

### Using MCP Docker Tools (Claude Code)

**Preferred debugging approach:**

```bash
# List containers
mcp__docker-mcp__list-containers

# View logs
mcp__docker-mcp__get-logs --container_name hoof-hearted-backend

# This gives Claude direct access to container status and logs
```

## 🎯 Performance Optimization

### Multi-Stage Build Benefits
- **Smaller production images** (removes dev dependencies)
- **Faster deployments** (optimized layers)
- **Security improvements** (minimal attack surface)

### External Testing Benefits
- **Faster test iterations** (local tooling performance)
- **Better debugging** (browser dev tools available)
- **Real environment testing** (against actual containers)

## 📚 Related Documentation

- **GPU Monitoring**: See `src/backend/monitoring/gpu_monitor.py`
- **API Endpoints**: See `src/backend/app.py`
- **Frontend Components**: See `src/frontend/src/components/`
- **src-brain Reference**: `/Users/davidkim/SpicyRiceCakes/src-brain/coding/guides/docker-advanced-testing-guide.md`

## 🌶️🍚🍰 SpicyRiceCakes Philosophy

This Docker architecture embodies our core methodology:
- **🌶️ Emotion**: User experience comes first (Korean humor ports, easy commands)
- **🍚 Logic**: Clean, systematic architecture (multi-stage builds, external testing)
- **🍰 Joy**: Delightful details (meaningful port numbers, comprehensive documentation)

---

**Remember**: Docker-first development is now the preferred approach. Use `npm run dev` instead of traditional development servers for the full monitoring stack experience!