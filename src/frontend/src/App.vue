<template>
  <div id="app" :class="{ 'dark-theme': isDarkMode }">
    <header class="header">
      <div class="header-content">
        <div class="title-section">
          <h1>🐎 Hoof Hearted</h1>
          <p>Home Server Monitoring Dashboard</p>
          <p class="port-info">Running on port 0909 (공구공구!)</p>
        </div>
        <button @click="toggleTheme" class="theme-toggle" :title="isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'">
          {{ isDarkMode ? '☀️' : '🌙' }}
        </button>
      </div>
    </header>
    
    <main class="main">
      <!-- Legacy Status Card for Connection Testing -->
      <div class="status-card">
        <h2>🚀 System Status</h2>
        <p>{{ statusMessage }}</p>
        <div class="metrics">
          <div class="metric">
            <span class="label">Backend API:</span>
            <span class="value" :class="backendStatus">{{ backendStatus }}</span>
          </div>
          <div class="metric">
            <span class="label">Database:</span>
            <span class="value" :class="databaseStatus">{{ databaseStatus }}</span>
          </div>
        </div>
      </div>
      
      <!-- Real-time Monitoring Dashboard -->
      <div class="dashboard-container">
        <RealTimeMonitoringDashboard />
      </div>
    </main>
    
    <footer class="footer">
      <p>🌶️🍚🍰 Built with SpicyRiceCakes philosophy: Emotion → Logic → Joy</p>
    </footer>
  </div>
</template>

<script>
import RealTimeMonitoringDashboard from '@/components/dashboard/RealTimeMonitoringDashboard.vue'

export default {
  name: 'App',
  components: {
    RealTimeMonitoringDashboard
  },
  data() {
    return {
      statusMessage: 'Docker deployment successful! 🎉',
      backendStatus: 'Connected',
      databaseStatus: 'Connecting...',
      isDarkMode: false
    }
  },
  mounted() {
    // Load theme preference
    const savedTheme = localStorage.getItem('hoof-hearted-theme')
    this.isDarkMode = savedTheme === 'dark'
    
    // Test backend connection
    this.checkBackendStatus()
    this.checkDatabaseStatus()
  },
  methods: {
    async checkBackendStatus() {
      try {
        const response = await fetch('/api/status')
        if (response.ok) {
          const data = await response.json()
          this.statusMessage = data.message || 'Backend connected successfully!'
          this.backendStatus = 'Connected'
        }
      } catch (error) {
        this.backendStatus = 'Disconnected'
        this.statusMessage = 'Backend connecting...'
      }
    },
    async checkDatabaseStatus() {
      try {
        const response = await fetch('/api/health')
        if (response.ok) {
          const data = await response.json()
          if (data.status === 'healthy') {
            this.databaseStatus = 'Connected'
          } else {
            this.databaseStatus = 'Disconnected'
          }
        }
      } catch (error) {
        this.databaseStatus = 'Disconnected'
      }
    },
    toggleTheme() {
      this.isDarkMode = !this.isDarkMode
      localStorage.setItem('hoof-hearted-theme', this.isDarkMode ? 'dark' : 'light')
    }
  }
}
</script>

<style>
/* CSS Custom Properties for Theme System */
:root {
  /* Light Theme (Default) */
  --bg-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --bg-secondary: rgba(255, 255, 255, 0.95);
  --bg-footer: rgba(0, 0, 0, 0.8);
  
  --text-primary: #333;
  --text-secondary: #666;
  --text-tertiary: #555;
  --text-footer: white;
  --text-accent: #764ba2;
  
  --border-light: rgba(255, 255, 255, 0.2);
  --border-divider: rgba(0, 0, 0, 0.1);
  
  --status-connected: #4CAF50;
  --status-disconnected: #f44336;
  
  --shadow-card: 0 8px 32px rgba(0, 0, 0, 0.1);
  --shadow-header: 0 2px 20px rgba(0, 0, 0, 0.1);
}

/* Dark Theme */
.dark-theme {
  --bg-primary: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  --bg-secondary: rgba(30, 30, 46, 0.95);
  --bg-footer: rgba(15, 15, 25, 0.9);
  
  --text-primary: #e0e0e0;
  --text-secondary: #a0a0a0;
  --text-tertiary: #c0c0c0;
  --text-footer: #e0e0e0;
  --text-accent: #8b7bd8;
  
  --border-light: rgba(100, 100, 120, 0.3);
  --border-divider: rgba(255, 255, 255, 0.1);
  
  --status-connected: #66bb6a;
  --status-disconnected: #ef5350;
  
  --shadow-card: 0 8px 32px rgba(0, 0, 0, 0.3);
  --shadow-header: 0 2px 20px rgba(0, 0, 0, 0.3);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: var(--text-primary);
  background: var(--bg-primary);
  min-height: 100vh;
  transition: all 0.3s ease;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: var(--bg-secondary);
  backdrop-filter: blur(10px);
  padding: 2rem;
  box-shadow: var(--shadow-header);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.title-section {
  text-align: left;
}

.header h1 {
  font-size: 2.5rem;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.header p {
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.port-info {
  font-weight: bold;
  color: var(--text-accent) !important;
  margin-top: 0.5rem;
}

.theme-toggle {
  background: none;
  border: 2px solid var(--border-light);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  color: var(--text-primary);
}

.theme-toggle:hover {
  transform: scale(1.1);
  border-color: var(--text-accent);
  background: var(--border-light);
}

.theme-toggle:active {
  transform: scale(0.95);
}

.main {
  flex: 1;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.status-card {
  width: 100%;
  max-width: 600px;
  align-self: center;
}

.dashboard-container {
  width: 100%;
}

.status-card, .placeholder-card {
  background: var(--bg-secondary);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 2rem;
  box-shadow: var(--shadow-card);
  border: 1px solid var(--border-light);
  transition: all 0.3s ease;
}

.status-card:hover, .placeholder-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.status-card h2, .placeholder-card h2 {
  color: var(--text-primary);
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.status-card p, .placeholder-card p {
  color: var(--text-secondary);
}

.metrics {
  margin-top: 1.5rem;
}

.metric {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border-divider);
}

.metric:last-child {
  border-bottom: none;
}

.label {
  font-weight: 600;
  color: var(--text-tertiary);
}

.value {
  font-weight: bold;
}

.value.Connected {
  color: var(--status-connected);
}

.value.Disconnected {
  color: var(--status-disconnected);
}

.placeholder-card ul {
  margin-top: 1rem;
  padding-left: 1.5rem;
}

.placeholder-card li {
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
}

.footer {
  background: var(--bg-footer);
  color: var(--text-footer);
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .main {
    grid-template-columns: 1fr;
    padding: 1rem;
  }
  
  .header {
    padding: 1.5rem;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }
  
  .title-section {
    text-align: center;
  }
  
  .header h1 {
    font-size: 2rem;
  }
  
  .status-card, .placeholder-card {
    padding: 1.5rem;
  }
}

@media (max-width: 480px) {
  .header h1 {
    font-size: 1.8rem;
  }
  
  .main {
    padding: 0.5rem;
  }
  
  .theme-toggle {
    width: 45px;
    height: 45px;
    font-size: 1.3rem;
  }
}

/* Smooth transitions for theme switching */
* {
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}
</style>