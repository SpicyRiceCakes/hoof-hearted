<template>
  <div class="monitoring-dashboard">
    <!-- Connection Status -->
    <div class="connection-status" :class="{ 'connected': isConnected, 'disconnected': !isConnected }">
      <div class="status-indicator"></div>
      <span>{{ isConnected ? 'Connected' : 'Disconnected' }}</span>
    </div>

    <!-- Real-time Metrics Grid -->
    <div class="metrics-grid">
      <!-- GPU Metrics Card -->
      <div class="metric-card gpu-card">
        <h3>🎮 GPU Status</h3>
        <div v-if="gpuMetrics.available && gpuMetrics.gpus.length > 0" class="gpu-metrics">
          <div v-for="(gpu, index) in gpuMetrics.gpus" :key="index" class="gpu-item">
            <div class="gpu-header">
              <strong>{{ gpu.name }}</strong>
            </div>
            <div class="metric-row">
              <span>Usage:</span>
              <span class="metric-value" :class="getUsageClass(gpu.utilization)">
                {{ gpu.utilization }}%
              </span>
            </div>
            <div class="metric-row">
              <span>Temperature:</span>
              <span class="metric-value" :class="getTempClass(gpu.temperature)">
                {{ gpu.temperature }}°C
              </span>
            </div>
            <div class="metric-row">
              <span>Memory:</span>
              <span class="metric-value">
                {{ formatMemory(gpu.memory_used) }} / {{ formatMemory(gpu.memory_total) }}
              </span>
            </div>
            <div class="metric-row">
              <span>Fan Speed:</span>
              <span class="metric-value">{{ gpu.fan_speed || 'N/A' }}%</span>
            </div>
          </div>
        </div>
        <div v-else class="no-data">
          <span>No GPU detected or monitoring unavailable</span>
        </div>
      </div>

      <!-- System Metrics Card -->
      <div class="metric-card system-card">
        <h3>💻 System Status</h3>
        <div v-if="systemMetrics.available" class="system-metrics">
          <div class="metric-row">
            <span>CPU Usage:</span>
            <span class="metric-value" :class="getUsageClass(systemMetrics.cpu.usage)">
              {{ systemMetrics.cpu.usage }}%
            </span>
          </div>
          <div class="metric-row">
            <span>Memory:</span>
            <span class="metric-value" :class="getUsageClass(systemMetrics.memory.percent)">
              {{ formatMemory(systemMetrics.memory.used) }} / {{ formatMemory(systemMetrics.memory.total) }}
              ({{ systemMetrics.memory.percent }}%)
            </span>
          </div>
          <div class="metric-row">
            <span>CPU Temp:</span>
            <span class="metric-value" :class="getTempClass(systemMetrics.cpu.temperature)">
              {{ systemMetrics.cpu.temperature || 'N/A' }}°C
            </span>
          </div>
        </div>
        <div v-else class="no-data">
          <span>System metrics unavailable</span>
        </div>
      </div>

      <!-- Active Processes Card -->
      <div class="metric-card processes-card">
        <h3>⚡ Active Processes</h3>
        <div v-if="processes && processes.length > 0" class="processes-list">
          <div v-for="process in processes.slice(0, 5)" :key="process.pid" class="process-item">
            <div class="process-name">{{ process.name }}</div>
            <div class="process-metrics">
              <span class="cpu">CPU: {{ process.cpu_percent }}%</span>
              <span class="memory">RAM: {{ formatMemory(process.memory_info.rss) }}</span>
            </div>
          </div>
        </div>
        <div v-else class="no-data">
          <span>No active processes detected</span>
        </div>
      </div>

      <!-- Alerts Card -->
      <div class="metric-card alerts-card" v-if="alerts.length > 0">
        <h3>🚨 Active Alerts</h3>
        <div class="alerts-list">
          <div v-for="alert in alerts" :key="alert.id" 
               class="alert-item" 
               :class="alert.level">
            <div class="alert-message">{{ alert.message }}</div>
            <div class="alert-time">{{ formatTime(alert.timestamp) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Last Update Time -->
    <div class="last-update">
      Last updated: {{ lastUpdateTime }}
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRealTimeStore } from '@/composables/useRealTimeStore'

export default {
  name: 'RealTimeMonitoringDashboard',
  setup() {
    const { state, connect, disconnect } = useRealTimeStore()
    const lastUpdateTime = ref(new Date().toLocaleTimeString())

    // Computed properties for reactive data
    const isConnected = computed(() => state.connected)
    const gpuMetrics = computed(() => state.gpuMetrics)
    const systemMetrics = computed(() => state.systemMetrics)
    const processes = computed(() => state.processes)
    const alerts = computed(() => state.alerts)

    // Update timestamp when data changes
    const updateTimestamp = () => {
      lastUpdateTime.value = new Date().toLocaleTimeString()
    }

    // Utility functions
    const getUsageClass = (usage) => {
      if (usage >= 90) return 'critical'
      if (usage >= 70) return 'warning'
      return 'normal'
    }

    const getTempClass = (temp) => {
      if (!temp) return 'normal'
      if (temp >= 80) return 'critical'
      if (temp >= 70) return 'warning'
      return 'normal'
    }

    const formatMemory = (bytes) => {
      if (!bytes) return 'N/A'
      const gb = bytes / (1024 * 1024 * 1024)
      return gb >= 1 ? `${gb.toFixed(1)}GB` : `${(bytes / (1024 * 1024)).toFixed(0)}MB`
    }

    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString()
    }

    // Lifecycle
    onMounted(() => {
      connect()
      // Update timestamp periodically
      const interval = setInterval(updateTimestamp, 1000)
      onUnmounted(() => {
        clearInterval(interval)
        disconnect()
      })
    })

    return {
      isConnected,
      gpuMetrics,
      systemMetrics,
      processes,
      alerts,
      lastUpdateTime,
      getUsageClass,
      getTempClass,
      formatMemory,
      formatTime
    }
  }
}
</script>

<style scoped>
.monitoring-dashboard {
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.connection-status.connected {
  background: rgba(34, 197, 94, 0.1);
  color: rgb(34, 197, 94);
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.connection-status.disconnected {
  background: rgba(239, 68, 68, 0.1);
  color: rgb(239, 68, 68);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.metric-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.metric-card h3 {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--foreground);
}

.metric-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.metric-row:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.metric-value {
  font-weight: 600;
  font-family: 'Monaco', 'Menlo', monospace;
}

.metric-value.normal {
  color: rgb(34, 197, 94);
}

.metric-value.warning {
  color: rgb(251, 191, 36);
}

.metric-value.critical {
  color: rgb(239, 68, 68);
}

.gpu-item {
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.gpu-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.gpu-header {
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
  color: rgb(168, 85, 247);
}

.processes-list {
  max-height: 200px;
  overflow-y: auto;
}

.process-item {
  margin-bottom: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.process-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.process-name {
  font-weight: 500;
  margin-bottom: 0.25rem;
  color: var(--foreground);
}

.process-metrics {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: var(--muted-foreground);
  font-family: 'Monaco', 'Menlo', monospace;
}

.alerts-list {
  max-height: 150px;
  overflow-y: auto;
}

.alert-item {
  padding: 0.75rem;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  border-left: 4px solid;
}

.alert-item.critical {
  background: rgba(239, 68, 68, 0.1);
  border-left-color: rgb(239, 68, 68);
}

.alert-item.warning {
  background: rgba(251, 191, 36, 0.1);
  border-left-color: rgb(251, 191, 36);
}

.alert-item.info {
  background: rgba(59, 130, 246, 0.1);
  border-left-color: rgb(59, 130, 246);
}

.alert-message {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.alert-time {
  font-size: 0.75rem;
  opacity: 0.7;
  font-family: 'Monaco', 'Menlo', monospace;
}

.no-data {
  text-align: center;
  color: var(--muted-foreground);
  font-style: italic;
  padding: 2rem 0;
}

.last-update {
  text-align: center;
  font-size: 0.875rem;
  color: var(--muted-foreground);
  font-family: 'Monaco', 'Menlo', monospace;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .monitoring-dashboard {
    padding: 0.75rem;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .metric-card {
    padding: 1rem;
  }

  .process-metrics {
    flex-direction: column;
    gap: 0.25rem;
  }
}
</style>