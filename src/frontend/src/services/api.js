// API service for Hoof Hearted monitoring
import axios from 'axios'
import { io } from 'socket.io-client'

class ApiService {
  constructor() {
    // Use environment variable or detect current location for API calls
    this.baseURL = import.meta.env.VITE_API_URL || (
      typeof window !== 'undefined' ? `${window.location.protocol}//${window.location.host}` : 'http://localhost:5002'
    )
    
    this.api = axios.create({
      baseURL: this.baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      }
    })

    // Initialize WebSocket connection
    this.socket = null
    this.isConnected = false
  }

  // Initialize WebSocket connection
  initWebSocket() {
    if (this.socket) return this.socket

    this.socket = io(this.baseURL, {
      transports: ['websocket', 'polling'],
      autoConnect: true,
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5
    })

    this.socket.on('connect', () => {
      console.log('🔌 Connected to Hoof Hearted WebSocket')
      this.isConnected = true
    })

    this.socket.on('disconnect', () => {
      console.log('🔌 Disconnected from Hoof Hearted WebSocket')
      this.isConnected = false
    })

    return this.socket
  }

  // Health and status endpoints
  async getHealth() {
    try {
      const response = await this.api.get('/api/health')
      return response.data
    } catch (error) {
      console.error('Health check failed:', error)
      return { status: 'unhealthy', error: error.message }
    }
  }

  async getStatus() {
    try {
      const response = await this.api.get('/api/status')
      return response.data
    } catch (error) {
      console.error('Status check failed:', error)
      return { message: 'Backend connecting...', error: error.message }
    }
  }

  // System monitoring endpoints
  async getSystemOverview() {
    try {
      const response = await this.api.get('/api/system/overview')
      return response.data
    } catch (error) {
      console.error('System overview failed:', error)
      return this.getFallbackSystemData()
    }
  }

  async getCPUMetrics() {
    try {
      const response = await this.api.get('/api/system/cpu')
      return response.data
    } catch (error) {
      console.error('CPU metrics failed:', error)
      return { usage: 0, temperature: 0, processes: [] }
    }
  }

  async getMemoryMetrics() {
    try {
      const response = await this.api.get('/api/system/memory')
      return response.data
    } catch (error) {
      console.error('Memory metrics failed:', error)
      return { used: 0, total: 16, processes: [] }
    }
  }

  async getDiskMetrics() {
    try {
      const response = await this.api.get('/api/system/disk')
      return response.data
    } catch (error) {
      console.error('Disk metrics failed:', error)
      return { disks: [{ name: 'C:', used: 0, total: 1000 }] }
    }
  }

  // GPU monitoring endpoints
  async getGPUSummary() {
    try {
      const response = await this.api.get('/api/gpu/summary')
      return response.data
    } catch (error) {
      console.error('GPU summary failed:', error)
      return this.getFallbackGPUData()
    }
  }

  async getGPUMetrics() {
    try {
      const response = await this.api.get('/api/gpu/metrics')
      return response.data
    } catch (error) {
      console.error('GPU metrics failed:', error)
      return this.getFallbackGPUData()
    }
  }

  async getGPUProcesses() {
    try {
      const response = await this.api.get('/api/gpu/processes')
      return response.data
    } catch (error) {
      console.error('GPU processes failed:', error)
      return { processes: [], explanation: 'Unable to fetch GPU processes' }
    }
  }

  // Real-time monitoring
  async getMonitoringStats() {
    try {
      const response = await this.api.get('/api/monitoring/stats')
      return response.data
    } catch (error) {
      console.error('Monitoring stats failed:', error)
      return { updates_sent: 0, clients_connected: 0 }
    }
  }

  // WebSocket event handlers
  onSystemMetricsUpdate(callback) {
    if (!this.socket) this.initWebSocket()
    this.socket.on('system:metrics_update', callback)
  }

  onInitialStatus(callback) {
    if (!this.socket) this.initWebSocket()
    this.socket.on('system:initial_status', callback)
  }

  onSystemAlerts(callback) {
    if (!this.socket) this.initWebSocket()
    this.socket.on('system:alerts', callback)
  }

  // Request immediate updates
  requestGPUUpdate() {
    if (this.socket && this.isConnected) {
      this.socket.emit('request_gpu_update')
    }
  }

  requestMonitoringStats() {
    if (this.socket && this.isConnected) {
      this.socket.emit('request_monitoring_stats')
    }
  }

  // Fallback data for when API is unavailable
  getFallbackSystemData() {
    return {
      cpu: {
        usage: 45,
        temperature: 62,
        processes: []
      },
      memory: {
        used: 12.4,
        total: 32,
        processes: []
      },
      disk: {
        disks: [
          { name: "C:", used: 450, total: 1000 },
          { name: "D:", used: 1200, total: 2000 }
        ]
      },
      network: {
        upload: 12.5,
        download: 45.2
      },
      uptime: "5d 12h 34m"
    }
  }

  getFallbackGPUData() {
    return {
      usage: 78,
      temperature: 72,
      memory: {
        used: 6.2,
        total: 8
      },
      fanSpeed: 2100,
      powerConsumption: 185,
      processes: [
        { id: 1, name: "blender.exe", cpu: 45.8, memory: 4.2, gpu: 65.3 }
      ]
    }
  }

  // Cleanup
  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
      this.isConnected = false
    }
  }
}

export default new ApiService()