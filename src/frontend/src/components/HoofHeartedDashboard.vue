<template>
  <div :class="{ 'dark': isDarkMode }">
    <div class="min-h-screen bg-gradient-to-br from-background via-background to-muted/20 transition-colors duration-300">
      <!-- Header -->
      <header class="border-b border-border/50 backdrop-blur-sm bg-background/80 sticky top-0 z-50">
        <div class="container mx-auto px-4 py-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="text-2xl">🐎</div>
              <div>
                <h1 class="text-xl font-bold text-foreground">Hoof Hearted</h1>
                <p class="text-sm text-muted-foreground">Home Server Monitoring</p>
              </div>
            </div>
            
            <div class="flex items-center gap-4">
              <!-- Connection Status -->
              <div class="flex items-center gap-2">
                <div class="flex items-center gap-1">
                  <Server class="h-4 w-4" />
                  <CheckCircle v-if="connectionStatus.api" class="h-3 w-3 text-green-500" />
                  <XCircle v-else class="h-3 w-3 text-red-500" />
                </div>
                <div class="flex items-center gap-1">
                  <Database class="h-4 w-4" />
                  <CheckCircle v-if="connectionStatus.database" class="h-3 w-3 text-green-500" />
                  <XCircle v-else class="h-3 w-3 text-red-500" />
                </div>
                <div class="flex items-center gap-1">
                  <Globe class="h-4 w-4" />
                  <CheckCircle v-if="connectionStatus.websocket" class="h-3 w-3 text-green-500" />
                  <XCircle v-else class="h-3 w-3 text-red-500" />
                </div>
              </div>

              <!-- Theme Toggle -->
              <Button
                variant="ghost"
                size="icon"
                @click="toggleTheme"
                class="transition-transform hover:scale-110"
              >
                <Sun v-if="isDarkMode" class="h-4 w-4" />
                <Moon v-else class="h-4 w-4" />
              </Button>

              <!-- Settings -->
              <Button variant="ghost" size="icon">
                <Settings class="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      <!-- Main Dashboard -->
      <main class="container mx-auto px-4 py-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          
          <!-- System Overview -->
          <MetricCard
            title="System Overview"
            :icon="Activity"
            class="lg:col-span-1"
          >
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <Cpu class="h-4 w-4" />
                  <span class="text-sm">CPU</span>
                </div>
                <span class="text-sm font-medium">{{ systemMetrics.cpu.usage }}%</span>
              </div>
              <Progress :value="systemMetrics.cpu.usage" class="h-2" />
              
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <MemoryStick class="h-4 w-4" />
                  <span class="text-sm">Memory</span>
                </div>
                <span class="text-sm font-medium">
                  {{ systemMetrics.memory.used }}GB / {{ systemMetrics.memory.total }}GB
                </span>
              </div>
              <Progress 
                :value="(systemMetrics.memory.used / systemMetrics.memory.total) * 100" 
                class="h-2" 
              />

              <div v-for="(disk, index) in systemMetrics.disk" :key="index">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <HardDrive class="h-4 w-4" />
                    <span class="text-sm">{{ disk.name }}</span>
                  </div>
                  <span class="text-sm font-medium">
                    {{ disk.used }}GB / {{ disk.total }}GB
                  </span>
                </div>
                <Progress :value="(disk.used / disk.total) * 100" class="h-2" />
              </div>

              <div class="flex items-center justify-between pt-2">
                <div class="flex items-center gap-2">
                  <Clock class="h-4 w-4" />
                  <span class="text-sm">Uptime</span>
                </div>
                <span class="text-sm font-medium">{{ systemMetrics.uptime }}</span>
              </div>
            </div>
          </MetricCard>

          <!-- GPU Monitoring -->
          <MetricCard
            title="GPU Monitoring"
            :icon="Zap"
            class="lg:col-span-2"
          >
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="flex flex-col items-center">
                <CircularProgress
                  :value="systemMetrics.gpu.temperature"
                  :color="getTemperatureColor(systemMetrics.gpu.temperature)"
                  :size="140"
                >
                  <div class="text-center">
                    <div class="text-2xl font-bold">{{ systemMetrics.gpu.temperature }}°C</div>
                    <div class="text-xs text-muted-foreground">Temperature</div>
                  </div>
                </CircularProgress>
              </div>
              
              <div class="space-y-4">
                <div>
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-sm">GPU Usage</span>
                    <span class="text-sm font-medium">{{ systemMetrics.gpu.usage }}%</span>
                  </div>
                  <Progress :value="systemMetrics.gpu.usage" class="h-2" />
                </div>
                
                <div>
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-sm">VRAM</span>
                    <span class="text-sm font-medium">
                      {{ systemMetrics.gpu.memory.used }}GB / {{ systemMetrics.gpu.memory.total }}GB
                    </span>
                  </div>
                  <Progress 
                    :value="(systemMetrics.gpu.memory.used / systemMetrics.gpu.memory.total) * 100" 
                    class="h-2" 
                  />
                </div>
                
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <Fan class="h-4 w-4 animate-spin" />
                    <span class="text-sm">Fan Speed</span>
                  </div>
                  <span class="text-sm font-medium">{{ systemMetrics.gpu.fanSpeed }} RPM</span>
                </div>
                
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <Zap class="h-4 w-4" />
                    <span class="text-sm">Power</span>
                  </div>
                  <span class="text-sm font-medium">{{ systemMetrics.gpu.powerConsumption }}W</span>
                </div>
              </div>
            </div>
          </MetricCard>

          <!-- Process Identification -->
          <MetricCard
            title="Process Monitor"
            :icon="TrendingUp"
            class="lg:col-span-2"
          >
            <div class="space-y-4">
              <div class="flex flex-col sm:flex-row gap-2">
                <div class="relative flex-1">
                  <Search class="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search processes..."
                    v-model="searchTerm"
                    class="pl-8"
                  />
                </div>
                <div class="flex gap-2">
                  <Button
                    :variant="processFilter === 'all' ? 'default' : 'outline'"
                    size="sm"
                    @click="processFilter = 'all'"
                  >
                    All
                  </Button>
                  <Button
                    :variant="processFilter === 'cpu' ? 'default' : 'outline'"
                    size="sm"
                    @click="processFilter = 'cpu'"
                  >
                    CPU
                  </Button>
                  <Button
                    :variant="processFilter === 'memory' ? 'default' : 'outline'"
                    size="sm"
                    @click="processFilter = 'memory'"
                  >
                    Memory
                  </Button>
                  <Button
                    :variant="processFilter === 'gpu' ? 'default' : 'outline'"
                    size="sm"
                    @click="processFilter = 'gpu'"
                  >
                    GPU
                  </Button>
                </div>
              </div>
              
              <div class="space-y-2">
                <div 
                  v-for="process in filteredProcesses.slice(0, 5)" 
                  :key="process.id" 
                  class="flex items-center justify-between p-2 rounded-lg bg-muted/20"
                >
                  <div class="flex-1">
                    <div class="font-medium text-sm">{{ process.name }}</div>
                    <div class="flex gap-4 text-xs text-muted-foreground">
                      <span>CPU: {{ process.cpu }}%</span>
                      <span>Memory: {{ process.memory }}GB</span>
                      <span>GPU: {{ process.gpu }}%</span>
                    </div>
                  </div>
                  <Button variant="ghost" size="sm">
                    <XCircle class="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>
          </MetricCard>

          <!-- Alerts & Notifications -->
          <MetricCard
            title="Alerts"
            :icon="AlertTriangle"
            class="lg:col-span-1"
          >
            <div class="space-y-3">
              <Alert 
                v-for="alert in alerts" 
                :key="alert.id" 
                :class="{
                  'border-red-500/50 bg-red-500/10': alert.type === 'critical',
                  'border-yellow-500/50 bg-yellow-500/10': alert.type === 'warning',
                  'border-blue-500/50 bg-blue-500/10': alert.type === 'info'
                }"
              >
                <div class="text-sm">
                  <div class="flex items-start justify-between">
                    <div>
                      <p>{{ alert.message }}</p>
                      <p class="text-xs text-muted-foreground mt-1">{{ alert.timestamp }}</p>
                    </div>
                    <Badge 
                      :variant="alert.type === 'critical' ? 'destructive' : 
                               alert.type === 'warning' ? 'secondary' : 'default'"
                    >
                      {{ alert.type }}
                    </Badge>
                  </div>
                </div>
              </Alert>
            </div>
          </MetricCard>

          <!-- Quick Actions -->
          <MetricCard
            title="Quick Actions"
            :icon="Settings"
            class="lg:col-span-3"
          >
            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
              <Button variant="outline" class="flex flex-col gap-2 h-auto py-4">
                <Power class="h-5 w-5" />
                <span class="text-xs">Restart</span>
              </Button>
              <Button variant="outline" class="flex flex-col gap-2 h-auto py-4">
                <RefreshCw class="h-5 w-5" />
                <span class="text-xs">Refresh GPU</span>
              </Button>
              <Button variant="outline" class="flex flex-col gap-2 h-auto py-4">
                <Trash2 class="h-5 w-5" />
                <span class="text-xs">Clear Cache</span>
              </Button>
              <Button variant="outline" class="flex flex-col gap-2 h-auto py-4">
                <Download class="h-5 w-5" />
                <span class="text-xs">Export Report</span>
              </Button>
              <Button variant="outline" class="flex flex-col gap-2 h-auto py-4">
                <Thermometer class="h-5 w-5" />
                <span class="text-xs">Temp Monitor</span>
              </Button>
              <Button variant="outline" class="flex flex-col gap-2 h-auto py-4">
                <Wifi class="h-5 w-5" />
                <span class="text-xs">Network</span>
              </Button>
            </div>
          </MetricCard>

        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { 
  Sun, 
  Moon, 
  Settings, 
  Cpu, 
  HardDrive, 
  Wifi, 
  Zap, 
  Fan, 
  Activity, 
  AlertTriangle, 
  CheckCircle, 
  XCircle,
  Search,
  Filter,
  Download,
  Power,
  RefreshCw,
  Trash2,
  Clock,
  MemoryStick,
  Thermometer,
  TrendingUp,
  Server,
  Database,
  Globe
} from 'lucide-vue-next'

import Button from '@/components/ui/button.vue'
import Progress from '@/components/ui/progress.vue'
import Input from '@/components/ui/input.vue'
import Badge from '@/components/ui/badge.vue'
import Alert from '@/components/ui/alert.vue'
import MetricCard from '@/components/MetricCard.vue'
import CircularProgress from '@/components/CircularProgress.vue'
import ApiService from '@/services/api.js'

// Reactive state
const isDarkMode = ref(true)
const searchTerm = ref("")
const processFilter = ref('all')
const isLoading = ref(true)
const lastUpdate = ref(new Date())

// Real data from API
const connectionStatus = ref({
  api: false,
  database: false,
  websocket: false
})

const systemMetrics = ref({
  cpu: {
    usage: 0,
    temperature: 0
  },
  memory: {
    used: 0,
    total: 0
  },
  gpu: {
    usage: 0,
    temperature: 0,
    memory: {
      used: 0,
      total: 0
    },
    fanSpeed: 0,
    powerConsumption: 0
  },
  disk: [],
  network: {
    upload: 0,
    download: 0
  },
  uptime: "Loading..."
})

const processes = ref([])
const alerts = ref([])
const gpuExplanation = ref("")

// Computed properties
const filteredProcesses = computed(() => {
  return processes.value.filter(process => {
    const matchesSearch = process.name.toLowerCase().includes(searchTerm.value.toLowerCase())
    if (!matchesSearch) return false
    
    switch (processFilter.value) {
      case 'cpu': return process.cpu > 10
      case 'memory': return process.memory > 1
      case 'gpu': return process.gpu > 10
      default: return true
    }
  })
})

// Methods
const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

const getTemperatureColor = (temp) => {
  if (temp < 60) return "hsl(142, 76%, 36%)" // green
  if (temp < 80) return "hsl(48, 96%, 53%)" // yellow
  return "hsl(0, 84%, 60%)" // red
}

const getUsageColor = (usage) => {
  if (usage < 50) return "hsl(142, 76%, 36%)" // green
  if (usage < 80) return "hsl(48, 96%, 53%)" // yellow
  return "hsl(0, 84%, 60%)" // red
}

// Data loading functions
const loadSystemData = async () => {
  try {
    isLoading.value = true
    
    // Load system overview
    const systemData = await ApiService.getSystemOverview()
    if (systemData && !systemData.error) {
      systemMetrics.value = {
        cpu: systemData.cpu || systemMetrics.value.cpu,
        memory: systemData.memory || systemMetrics.value.memory,
        disk: systemData.disk?.disks || systemData.disk || systemMetrics.value.disk,
        network: systemData.network || systemMetrics.value.network,
        uptime: systemData.uptime || systemMetrics.value.uptime,
        gpu: systemMetrics.value.gpu // Keep existing GPU data
      }
    }

    // Load GPU data
    const gpuData = await ApiService.getGPUMetrics()
    if (gpuData && !gpuData.error) {
      systemMetrics.value.gpu = {
        usage: gpuData.usage || 0,
        temperature: gpuData.temperature || 0,
        memory: gpuData.memory || { used: 0, total: 0 },
        fanSpeed: gpuData.fanSpeed || gpuData.fan_speed || 0,
        powerConsumption: gpuData.powerConsumption || gpuData.power_draw || 0
      }
    }

    // Load GPU processes for explanation
    const gpuProcesses = await ApiService.getGPUProcesses()
    if (gpuProcesses && gpuProcesses.processes) {
      // Combine all processes
      const allProcesses = [
        ...(systemData.cpu?.processes || []),
        ...(systemData.memory?.processes || []),
        ...(gpuProcesses.processes || [])
      ]
      
      // Remove duplicates and format
      const uniqueProcesses = allProcesses.reduce((acc, process) => {
        const existing = acc.find(p => p.name === process.name || p.pid === process.pid)
        if (!existing) {
          acc.push({
            id: process.pid || Math.random(),
            name: process.name || process.process_name || 'Unknown',
            cpu: process.cpu_percent || process.cpu || 0,
            memory: process.memory_mb ? process.memory_mb / 1024 : (process.memory || 0),
            gpu: process.gpu_percent || process.gpu || 0
          })
        }
        return acc
      }, [])
      
      processes.value = uniqueProcesses
      gpuExplanation.value = gpuProcesses.explanation || ""
    }

    lastUpdate.value = new Date()
  } catch (error) {
    console.error('Failed to load system data:', error)
  } finally {
    isLoading.value = false
  }
}

const checkConnectionStatus = async () => {
  try {
    // Check API health
    const health = await ApiService.getHealth()
    connectionStatus.value.api = health && health.status !== 'unhealthy'
    connectionStatus.value.database = health && health.database !== 'disconnected'
    
    // Check WebSocket
    connectionStatus.value.websocket = ApiService.isConnected
  } catch (error) {
    connectionStatus.value.api = false
    connectionStatus.value.database = false
    connectionStatus.value.websocket = false
  }
}

const initializeWebSocket = () => {
  ApiService.initWebSocket()
  
  // Listen for real-time updates
  ApiService.onSystemMetricsUpdate((data) => {
    if (data) {
      // Update system metrics with real-time data
      if (data.cpu) systemMetrics.value.cpu = { ...systemMetrics.value.cpu, ...data.cpu }
      if (data.memory) systemMetrics.value.memory = { ...systemMetrics.value.memory, ...data.memory }
      if (data.gpu) systemMetrics.value.gpu = { ...systemMetrics.value.gpu, ...data.gpu }
      if (data.disk) systemMetrics.value.disk = data.disk.disks || data.disk
      lastUpdate.value = new Date()
    }
  })
  
  // Listen for alerts
  ApiService.onSystemAlerts((alertData) => {
    if (alertData && alertData.message) {
      const newAlert = {
        id: Date.now(),
        type: alertData.type || 'info',
        message: alertData.message,
        timestamp: 'Just now'
      }
      alerts.value.unshift(newAlert)
      
      // Keep only last 5 alerts
      if (alerts.value.length > 5) {
        alerts.value = alerts.value.slice(0, 5)
      }
    }
  })
  
  // Get initial status
  ApiService.onInitialStatus((data) => {
    if (data) {
      loadSystemData()
    }
  })
}

// Lifecycle
onMounted(async () => {
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
  
  // Initialize connections and load data
  await checkConnectionStatus()
  await loadSystemData()
  initializeWebSocket()
  
  // Set up periodic updates as fallback
  setInterval(() => {
    checkConnectionStatus()
    if (!ApiService.isConnected) {
      loadSystemData()
    }
  }, 10000) // Every 10 seconds
})

onUnmounted(() => {
  ApiService.disconnect()
})
</script>