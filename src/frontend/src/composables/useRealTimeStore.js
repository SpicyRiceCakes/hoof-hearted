// 🐎 Hoof Hearted - Real-Time Data Store
// Vue 3 Composition API + Socket.IO for Real-Time Monitoring
// Implements Sophie's approved reactive store architecture

import { reactive, computed, onMounted, onUnmounted } from 'vue'
import { io } from 'socket.io-client'

// Global reactive state for real-time monitoring data
const state = reactive({
  // Connection management
  connected: false,
  connecting: false,
  reconnecting: false,
  connectionError: null,
  lastConnectionTime: null,
  
  // Metrics data
  gpuMetrics: {
    available: false,
    summary: {},
    gpus: [],
    lastUpdate: null
  },
  
  systemMetrics: {
    available: false,
    summary: {},
    cpu: {},
    memory: {},
    topProcesses: [],
    lastUpdate: null
  },
  
  // Real-time alerts
  alerts: [],
  lastAlert: null,
  
  // Monitoring statistics
  monitoringStats: {
    active: false,
    connectedClients: 0,
    updateCount: 0,
    errorCount: 0,
    uptimeSeconds: 0,
    updatesPerMinute: 0,
    errorRate: 0
  },
  
  // Update tracking
  totalUpdates: 0,
  lastUpdateTime: null,
  updateFrequency: 'standard'
})

// Socket.IO instance (will be initialized per component)
let socket = null
let reconnectAttempts = 0
const maxReconnectAttempts = 5

/**
 * Main composable for real-time monitoring data
 * Implements Sophie's approved architecture with namespace isolation
 */
export function useRealTimeStore() {
  
  // Initialize Socket.IO connection
  const connect = () => {
    if (socket?.connected) {
      console.log('🔗 Socket already connected')
      return
    }
    
    state.connecting = true
    state.connectionError = null
    
    // Socket.IO client configuration (Sophie's recommendation for manual setup)
    socket = io(import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000', {
      transports: ['websocket', 'polling'],
      timeout: 10000,
      reconnection: true,
      reconnectionAttempts: maxReconnectAttempts,
      reconnectionDelay: 2000,
      reconnectionDelayMax: 10000
    })
    
    // Connection event handlers
    socket.on('connect', handleConnect)
    socket.on('disconnect', handleDisconnect)
    socket.on('connect_error', handleConnectionError)
    socket.on('reconnect', handleReconnect)
    socket.on('reconnect_error', handleReconnectError)
    
    // Data event handlers (using Sophie's namespaced events)
    socket.on('system:initial_status', handleInitialStatus)
    socket.on('system:metrics_update', handleMetricsUpdate)
    socket.on('system:alerts', handleAlerts)
    socket.on('system:monitoring_stats', handleMonitoringStats)
    
    // Legacy event handlers for backward compatibility
    socket.on('gpu_status_update', handleLegacyGpuUpdate)
    socket.on('high_gpu_usage_alert', handleLegacyAlert)
    
    console.log('🚀 Socket.IO client initialized')
  }
  
  // Disconnect Socket.IO
  const disconnect = () => {
    if (socket) {
      socket.disconnect()
      socket = null
      state.connected = false
      state.connecting = false
      console.log('🔌 Socket.IO disconnected')
    }
  }
  
  // Connection event handlers
  const handleConnect = () => {
    state.connected = true
    state.connecting = false
    state.reconnecting = false
    state.connectionError = null
    state.lastConnectionTime = new Date().toISOString()
    reconnectAttempts = 0
    
    console.log('✅ Socket.IO connected successfully')
  }
  
  const handleDisconnect = (reason) => {
    state.connected = false
    state.connecting = false
    
    console.log(`🔌 Socket.IO disconnected: ${reason}`)
    
    // Auto-reconnect for certain disconnect reasons
    if (reason === 'io server disconnect') {
      // Server initiated disconnect - will auto-reconnect
      state.reconnecting = true
    }
  }
  
  const handleConnectionError = (error) => {
    state.connectionError = error.message || 'Connection failed'
    state.connecting = false
    
    console.error('❌ Socket.IO connection error:', error)
  }
  
  const handleReconnect = (attemptNumber) => {
    state.reconnecting = false
    reconnectAttempts = 0
    
    console.log(`🔄 Socket.IO reconnected after ${attemptNumber} attempts`)
  }
  
  const handleReconnectError = (error) => {
    reconnectAttempts++
    
    if (reconnectAttempts >= maxReconnectAttempts) {
      state.reconnecting = false
      state.connectionError = 'Failed to reconnect after multiple attempts'
      console.error('❌ Socket.IO reconnection failed:', error)
    }
  }
  
  // Data event handlers
  const handleInitialStatus = (data) => {
    console.log('📊 Received initial status', data)
    
    if (data.gpu) {
      state.gpuMetrics.available = data.gpu.monitoring_available || false
      state.gpuMetrics.summary = data.gpu
      state.gpuMetrics.lastUpdate = data.timestamp
    }
    
    if (data.system) {
      state.systemMetrics.available = data.system.monitoring_available || false
      state.systemMetrics.summary = data.system
      state.systemMetrics.lastUpdate = data.timestamp
    }
  }
  
  const handleMetricsUpdate = (data) => {
    state.totalUpdates++
    state.lastUpdateTime = data.timestamp
    state.updateFrequency = data.urgency || 'standard'
    
    // Update GPU metrics
    if (data.gpu?.available) {
      state.gpuMetrics.available = true
      state.gpuMetrics.summary = data.gpu.summary || {}
      state.gpuMetrics.gpus = data.gpu.gpus || []
      state.gpuMetrics.lastUpdate = data.timestamp
    }
    
    // Update system metrics
    if (data.system?.available) {
      state.systemMetrics.available = true
      state.systemMetrics.summary = data.system.summary || {}
      state.systemMetrics.cpu = data.system.cpu || {}
      state.systemMetrics.memory = data.system.memory || {}
      state.systemMetrics.topProcesses = data.system.top_processes || []
      state.systemMetrics.lastUpdate = data.timestamp
    }
    
    console.log(`📊 Metrics update #${state.totalUpdates} (${data.urgency})`)
  }
  
  const handleAlerts = (data) => {
    const newAlerts = data.alerts || []
    
    // Add alerts to the front of the array (newest first)
    state.alerts.unshift(...newAlerts.map(alert => ({
      ...alert,
      id: Math.random().toString(36).substr(2, 9),
      timestamp: data.timestamp,
      seen: false
    })))
    
    // Limit alerts array size (keep last 50 alerts)
    if (state.alerts.length > 50) {
      state.alerts = state.alerts.slice(0, 50)
    }
    
    state.lastAlert = data.timestamp
    
    console.log(`🚨 Received ${newAlerts.length} alert(s)`, newAlerts)
  }
  
  const handleMonitoringStats = (data) => {
    state.monitoringStats = { ...data }
    console.log('📈 Monitoring stats updated', data)
  }
  
  // Legacy event handlers for backward compatibility
  const handleLegacyGpuUpdate = (data) => {
    state.gpuMetrics.summary = data
    state.gpuMetrics.lastUpdate = Date.now()
    console.log('📊 Legacy GPU update received')
  }
  
  const handleLegacyAlert = (data) => {
    // Convert legacy alert format to new format
    const alerts = [{
      type: 'warning',
      category: 'gpu_usage',
      message: `High GPU usage detected`,
      timestamp: data.timestamp
    }]
    
    handleAlerts({ alerts, timestamp: data.timestamp })
  }
  
  // Manual actions
  const requestUpdate = () => {
    if (socket?.connected) {
      socket.emit('request_gpu_update')
      console.log('🔄 Manual update requested')
    }
  }
  
  const requestMonitoringStats = () => {
    if (socket?.connected) {
      socket.emit('request_monitoring_stats')
      console.log('📈 Monitoring stats requested')
    }
  }
  
  const markAlertAsSeen = (alertId) => {
    const alert = state.alerts.find(a => a.id === alertId)
    if (alert) {
      alert.seen = true
    }
  }
  
  const clearAllAlerts = () => {
    state.alerts = []
  }
  
  // Computed properties for easy access to data
  const connectionStatus = computed(() => {
    if (state.connected) return 'connected'
    if (state.connecting) return 'connecting'
    if (state.reconnecting) return 'reconnecting'
    if (state.connectionError) return 'error'
    return 'disconnected'
  })
  
  const hasGpuData = computed(() => {
    return state.gpuMetrics.available && state.gpuMetrics.gpus.length > 0
  })
  
  const hasSystemData = computed(() => {
    return state.systemMetrics.available && Object.keys(state.systemMetrics.cpu).length > 0
  })
  
  const unreadAlerts = computed(() => {
    return state.alerts.filter(alert => !alert.seen)
  })
  
  const criticalAlerts = computed(() => {
    return state.alerts.filter(alert => alert.type === 'critical')
  })
  
  const isMonitoringActive = computed(() => {
    return state.monitoringStats.active && state.connected
  })
  
  const dataFreshness = computed(() => {
    const now = Date.now()
    const lastUpdate = Math.max(
      state.gpuMetrics.lastUpdate || 0,
      state.systemMetrics.lastUpdate || 0
    )
    
    if (!lastUpdate) return 'no-data'
    
    const ageSeconds = (now - lastUpdate) / 1000
    
    if (ageSeconds < 10) return 'fresh'
    if (ageSeconds < 30) return 'recent'
    if (ageSeconds < 60) return 'stale'
    return 'very-stale'
  })
  
  // Component lifecycle management
  const setupRealTimeStore = () => {
    onMounted(() => {
      connect()
    })
    
    onUnmounted(() => {
      disconnect()
    })
  }
  
  // Return reactive state and methods
  return {
    // State
    state,
    
    // Connection management
    connect,
    disconnect,
    connectionStatus,
    
    // Data access
    hasGpuData,
    hasSystemData,
    dataFreshness,
    
    // Alerts
    unreadAlerts,
    criticalAlerts,
    markAlertAsSeen,
    clearAllAlerts,
    
    // Monitoring
    isMonitoringActive,
    requestUpdate,
    requestMonitoringStats,
    
    // Lifecycle
    setupRealTimeStore
  }
}

/**
 * Simplified composable for components that only need specific data
 * Implements Sophie's namespace isolation recommendation
 */
export function useGpuData() {
  const { state, hasGpuData } = useRealTimeStore()
  
  return {
    gpuMetrics: computed(() => state.gpuMetrics),
    hasGpuData,
    gpus: computed(() => state.gpuMetrics.gpus || []),
    gpuSummary: computed(() => state.gpuMetrics.summary || {})
  }
}

export function useSystemData() {
  const { state, hasSystemData } = useRealTimeStore()
  
  return {
    systemMetrics: computed(() => state.systemMetrics),
    hasSystemData,
    cpu: computed(() => state.systemMetrics.cpu || {}),
    memory: computed(() => state.systemMetrics.memory || {}),
    topProcesses: computed(() => state.systemMetrics.topProcesses || [])
  }
}

export function useAlerts() {
  const { state, unreadAlerts, criticalAlerts, markAlertAsSeen, clearAllAlerts } = useRealTimeStore()
  
  return {
    alerts: computed(() => state.alerts),
    unreadAlerts,
    criticalAlerts,
    lastAlert: computed(() => state.lastAlert),
    markAlertAsSeen,
    clearAllAlerts
  }
}