# 🐎 Hoof Hearted

**Home Server Monitoring Dashboard** - Answering "Why is my GPU fan running?"

Built with 🌶️🍚🍰 SpicyRiceCakes philosophy: **Emotion → Logic → Joy**

---

## 🎯 What is Hoof Hearted?

A lightweight, real-time home server monitoring dashboard that focuses on answering the most important question: **"Why is my GPU fan running?"**

Perfect for home servers, gaming rigs, and workstations. Get instant insights into system performance, identify resource-intensive processes, and monitor your hardware health from any device on your network.

### ✨ Key Features

- 🔥 **Real-time GPU monitoring** - Usage, temperature, fan speed, memory
- 🧠 **Process identification** - See exactly which processes are using your GPU/CPU
- 📱 **Mobile-friendly dashboard** - Monitor from your phone, tablet, or desktop
- 📊 **Historical data** - Track trends and usage patterns over time
- 🔔 **Smart alerts** - Configurable notifications for high resource usage
- 🏠 **Local-first** - All data stays on your network, no external dependencies
- 🐳 **Easy deployment** - One-line Docker installation

---

## 🚀 Quick Start

### One-Line Installation

```bash
curl -sSL https://raw.githubusercontent.com/spicyricecakes/hoof-hearted/main/install.sh | bash
```

After installation, access your dashboard at: **http://localhost:0909**

*Why port 0909? It sounds like "공구공구" (gong-goo-gong-goo) in Korean - SpicyRiceCakes fart humor! 💨*

### Manual Installation

1. **Clone and configure:**
   ```bash
   git clone https://github.com/spicyricecakes/hoof-hearted.git
   cd hoof-hearted
   cp .env.example .env
   ```

2. **Start with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

3. **Access dashboard:**
   Open http://localhost:0909 in your browser

---

## 🏗️ Architecture

### Technology Stack
- **Frontend:** Vue.js 3 + Composition API + Vite
- **Backend:** Python Flask + Flask-SocketIO for WebSocket support
- **Database:** PostgreSQL (with optional TimescaleDB upgrade path)
- **Deployment:** Docker multi-container setup

### Container Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (Vue.js)      │◄──►│   (Flask)       │◄──►│ (PostgreSQL)    │
│   Port: 0909    │    │   Port: 5000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 📋 System Requirements

### Minimum Requirements
- **RAM:** 512MB available
- **CPU:** Any modern processor
- **Storage:** 1GB for application + database growth
- **Network:** Local network access

### Recommended Requirements
- **RAM:** 1GB+ available for smooth operation
- **CPU:** Multi-core for concurrent monitoring
- **Storage:** 5GB+ for extended historical data
- **Network:** Gigabit for responsive dashboard

---

## ⚙️ Configuration

### Environment Variables

Key configuration options in `.env`:

```bash
# Dashboard access
DASHBOARD_PORT=0909                    # Main dashboard port
EXTERNAL_DOMAIN=                       # For remote access via Cloudflare

# Monitoring settings
METRICS_INTERVAL=5                     # Collection interval (seconds)
GPU_MONITORING=auto                    # nvidia/amd/auto
ENABLE_PROCESS_MONITORING=true         # Process tracking

# Alert thresholds
CPU_ALERT_THRESHOLD=80                 # CPU usage %
GPU_ALERT_THRESHOLD=85                 # GPU usage %
MEMORY_ALERT_THRESHOLD=90              # Memory usage %
TEMPERATURE_ALERT_THRESHOLD=75         # Temperature °C

# Updates
ENABLE_AUTO_UPDATES=false              # Watchtower integration
```

See `.env.example` for complete configuration options.

---

## 🖥️ Platform Support

### Deployment Options

#### 🔧 **Unraid (Recommended for Home Servers)**
- Use Community Applications template
- GUI-based configuration
- Automatic updates via Unraid interface

#### 🐳 **Docker Compose (Universal)**
- Works on any Docker-capable system
- Manual control over updates
- Best for technical users

#### 📦 **Portainer (Container Management)**
- Web-based Docker management
- Stack deployment support
- Good for multiple containers

### Operating System Support
- ✅ **Linux** (Ubuntu, Debian, CentOS, etc.)
- ✅ **macOS** (Intel and Apple Silicon)
- ✅ **Windows** (via Docker Desktop)
- ✅ **Unraid** (Community Applications)

### GPU Support
- ✅ **NVIDIA** (via nvidia-ml-py)
- ✅ **AMD** (via system monitoring)
- ✅ **Intel iGPU** (basic monitoring)
- ✅ **Auto-detection** (fallback to CPU monitoring)

---

## 📱 Dashboard Features

### Main Dashboard
- **System Overview** - CPU, GPU, memory usage at a glance
- **Process List** - Live view of running processes with resource usage
- **Temperature Monitoring** - Real-time temperature tracking
- **Historical Charts** - Usage trends over time

### Mobile Experience
- **Responsive design** - Works perfectly on phones and tablets
- **Touch-friendly controls** - Easy navigation on mobile devices
- **Quick status check** - Essential info accessible on the go
- **Dark mode support** - Easy on the eyes for night monitoring

### Real-time Updates
- **WebSocket communication** - Live data without page refreshes
- **Smooth animations** - Visual feedback for data changes
- **Configurable refresh rates** - Balance between responsiveness and performance

---

## 🔔 Alerts & Notifications

### Alert Types
- **High CPU usage** - When CPU exceeds threshold
- **High GPU usage** - When GPU exceeds threshold
- **High memory usage** - When memory exceeds threshold
- **High temperatures** - When temperatures exceed safe limits
- **Process alerts** - When specific processes consume too many resources

### Notification Methods
- **Dashboard notifications** - In-app alert system
- **Email alerts** (optional) - SMTP configuration
- **Discord webhooks** (optional) - Send alerts to Discord channels

---

## 🛡️ Security & Privacy

### Local-First Approach
- **No external dependencies** - All data stays on your network
- **No telemetry** - No data sent to external services
- **Local network only** - Default configuration restricts access to LAN

### Optional Security Features
- **Basic authentication** - Username/password protection
- **IP restrictions** - Limit access to specific IP ranges
- **HTTPS support** - SSL/TLS encryption (via Cloudflare)

---

## 🔄 Updates & Maintenance

### Update Methods

#### Automatic Updates (Optional)
```bash
# Enable Watchtower in docker-compose.yml
docker-compose --profile watchtower up -d
```

#### Manual Updates
```bash
# Pull latest images and restart
docker-compose pull
docker-compose up -d
```

#### Unraid Updates
- Updates available through Community Applications
- Notification when new versions are released
- One-click update process

### Backup & Restore
```bash
# Backup configuration and data
docker-compose down
tar -czf hoof-hearted-backup.tar.gz .env data/

# Restore from backup
tar -xzf hoof-hearted-backup.tar.gz
docker-compose up -d
```

---

## 🐛 Troubleshooting

### Common Issues

**Dashboard not accessible:**
- Check port 0909 is not blocked by firewall
- Verify Docker containers are running: `docker-compose ps`
- Check logs: `docker-compose logs -f`

**GPU not detected:**
- Ensure GPU drivers are installed
- Check container has access to GPU
- Try `GPU_MONITORING=auto` in .env

**High resource usage:**
- Increase `METRICS_INTERVAL` to reduce frequency
- Disable `ENABLE_PROCESS_MONITORING` if not needed
- Check database disk usage

### Getting Help

- 📚 **Documentation:** [GitHub Wiki](https://github.com/spicyricecakes/hoof-hearted/wiki)
- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/spicyricecakes/hoof-hearted/issues)
- 💬 **Community:** [Discussions](https://github.com/spicyricecakes/hoof-hearted/discussions)
- 📧 **Support:** contact@spicyricecakes.com

---

## 🤝 Contributing

We welcome contributions! Whether it's:

- 🐛 **Bug fixes**
- ✨ **New features**
- 📚 **Documentation improvements**
- 🎨 **UI/UX enhancements**
- 🌍 **Translations**

### Development Setup

1. **Clone repository:**
   ```bash
   git clone https://github.com/spicyricecakes/hoof-hearted.git
   cd hoof-hearted
   ```

2. **Start development environment:**
   ```bash
   # Backend
   cd src/backend
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   python app.py

   # Frontend (new terminal)
   cd src/frontend
   npm install
   npm run dev
   ```

3. **Make changes and submit PR**

---

## 📄 License

**MIT License** - Use, modify, and distribute freely.

See [LICENSE](LICENSE) file for full details.

---

## 🌶️ About SpicyRiceCakes

**SpicyRiceCakes** is dedicated to making dreams reality through AI-human collaboration.

Our philosophy: **🌶️ Emotion → 🍚 Logic → 🍰 Joy**

- **🌶️ Emotion** - User experience and feeling come first
- **🍚 Logic** - Clean architecture and systematic thinking  
- **🍰 Joy** - Delightful details and poetic touches

### Other SpicyRiceCakes Projects
- 🎨 **MirimYoo.com** - Artist portfolio website
- 🏠 **PadTie** - Real estate management platform
- 🧠 **SophiAMindMapper** - AI memory and knowledge management

---

## 💝 Support

If Hoof Hearted helps you monitor your home server, consider:

- ⭐ **Star the repository** on GitHub
- 🐛 **Report bugs** to help improve the project
- 💡 **Suggest features** for future development
- 📢 **Share with friends** who run home servers
- ☕ **Buy us coffee** (coming soon!)

---

**🐎 Happy monitoring!**  
*May your GPU fans run only when needed.* 💨

---

*Built with ❤️ by [SpicyRiceCakes](https://spicyricecakes.com)*# hoof-hearted
