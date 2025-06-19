Magic Chat
Hoof Hearted - Home Server Monitoring Dashboard UI Project Vision: A modern, real-time monitoring dashboard that answers "Why is my GPU fan running?" with beautiful data visualization and process identification. Core Layout & Theme - Modern dark/light theme toggle with smooth transitions - Glass morphism design with backdrop blur effects and subtle gradients - Responsive grid layout that works on desktop, tablet, and mobile - Color scheme: Deep blues/purples for dark mode, light grays/whites for light mode - Typography: Clean, readable fonts with clear hierarchy Header Section - Logo area: 🐎 Hoof Hearted branding with subtitle "Home Server Monitoring" - Status indicators: Real-time connection status (Backend API, Database, WebSocket) - Theme toggle button: Sun/moon icon with smooth animation - Settings/config gear icon (for future settings panel) Main Dashboard Grid (4-6 cards layout) 1. System Overview Card - CPU usage gauge with percentage and temperature - Memory usage bar with used/total GB - Disk usage for multiple drives - Network I/O up/down indicators - System uptime display 2. GPU Monitoring Card (Primary focus) - Large GPU temperature gauge (prominent, color-coded: green→yellow→red) - GPU usage percentage with real-time graph - Memory usage (VRAM used/total) - Fan speed RPM with visual fan animation - Power consumption in watts 3. Process Identification Card - Top 5 resource-intensive processes list - Each process shows: Name, CPU%, Memory%, GPU% - Kill/manage process buttons (with confirmation) - Filter toggles: CPU-heavy, Memory-heavy, GPU-heavy - Search bar to find specific processes 4. Real-time Metrics Graph - Multi-line chart showing CPU, GPU, Memory over time - Time range selector: Last 1hr, 6hr, 24hr, 7 days - Interactive tooltips on hover - Zoom/pan functionality - Export data button 5. Alerts & Notifications Card - Active alerts with severity levels (Critical, Warning, Info) - Alert history (expandable list) - Threshold settings quick access - Notification preferences toggle 6. Quick Actions Card - System restart/shutdown buttons (with confirmation) - Clear cache/temp files button - Force GPU driver refresh - Export system report - Schedule maintenance mode Advanced Features (Future Expandability) Bottom Expandable Section - Detailed hardware info (collapsible) - Network monitoring (bandwidth, connections) - Storage analysis (file types, large files) - Historical reports (weekly/monthly summaries) Modal/Overlay Panels - Settings panel: Thresholds, notifications, refresh rates - Process details modal: Deep dive into specific processes - System logs viewer: Filterable, searchable logs - About/help panel: Version info, documentation links Data Visualization Requirements - Real-time updates (1-5 second intervals) - Smooth animations for data changes - Color-coded status (green=good, yellow=warning, red=critical) - Progress bars and gauges with smooth transitions - Sparkline charts for quick trend visualization - Interactive elements with hover states and click actions Mobile Responsiveness - Collapsible sidebar on mobile - Stacked card layout for smaller screens - Touch-friendly buttons and controls - Swipe gestures for card navigation - Optimized typography for readability Accessibility & UX - High contrast color options - Keyboard navigation support - Screen reader friendly labels - Loading states for all async operations - Error handling with user-friendly messages - Tooltip help for technical terms Technical Specs - Vue.js 3 + Composition API compatible - CSS Grid/Flexbox layout - CSS custom properties for theming - WebSocket integration ready - Chart.js or similar for data visualization - Responsive breakpoints: 320px, 768px, 1024px, 1440px+ Inspiration Keywords - "Modern server monitoring", "Glass morphism dashboard", "Real-time analytics", "System monitoring UI", "Dark theme dashboard", "Process manager interface", "GPU monitoring display", "Home server admin panel"
Variant 1
Copy Prompt
Feedback

Hoof Hearted - Home Server Monitoring Dashboard UI Project Vision: A modern, real-time monitoring dashboard that answers "Why is my GPU fan running?" with beautiful data visualization and process identification. Core Layout & Theme - Modern dark/light theme toggle with smooth transitions - Glass morphism design with backdrop blur effects and subtle gradients - Responsive grid layout that works on desktop, tablet, and mobile - Color scheme: Deep blues/purples for dark mode, light grays/whites for light mode - Typography: Clean, readable fonts with clear hierarchy Header Section - Logo area: 🐎 Hoof Hearted branding with subtitle "Home Server Monitoring" - Status indicators: Real-time connection status (Backend API, Database, WebSocket) - Theme toggle button: Sun/moon icon with smooth animation - Settings/config gear icon (for future settings panel) Main Dashboard Grid (4-6 cards layout) 1. System Overview Card - CPU usage gauge with percentage and temperature - Memory usage bar with used/total GB - Disk usage for multiple drives - Network I/O up/down indicators - System uptime display 2. GPU Monitoring Card (Primary focus) - Large GPU temperature gauge (prominent, color-coded: green→yellow→red) - GPU usage percentage with real-time graph - Memory usage (VRAM used/total) - Fan speed RPM with visual fan animation - Power consumption in watts 3. Process Identification Card - Top 5 resource-intensive processes list - Each process shows: Name, CPU%, Memory%, GPU% - Kill/manage process buttons (with confirmation) - Filter toggles: CPU-heavy, Memory-heavy, GPU-heavy - Search bar to find specific processes 4. Real-time Metrics Graph - Multi-line chart showing CPU, GPU, Memory over time - Time range selector: Last 1hr, 6hr, 24hr, 7 days - Interactive tooltips on hover - Zoom/pan functionality - Export data button 5. Alerts & Notifications Card - Active alerts with severity levels (Critical, Warning, Info) - Alert history (expandable list) - Threshold settings quick access - Notification preferences toggle 6. Quick Actions Card - System restart/shutdown buttons (with confirmation) - Clear cache/temp files button - Force GPU driver refresh - Export system report - Schedule maintenance mode Advanced Features (Future Expandability) Bottom Expandable Section - Detailed hardware info (collapsible) - Network monitoring (bandwidth, connections) - Storage analysis (file types, large files) - Historical reports (weekly/monthly summaries) Modal/Overlay Panels - Settings panel: Thresholds, notifications, refresh rates - Process details modal: Deep dive into specific processes - System logs viewer: Filterable, searchable logs - About/help panel: Version info, documentation links Data Visualization Requirements - Real-time updates (1-5 second intervals) - Smooth animations for data changes - Color-coded status (green=good, yellow=warning, red=critical) - Progress bars and gauges with smooth transitions - Sparkline charts for quick trend visualization - Interactive elements with hover states and click actions Mobile Responsiveness - Collapsible sidebar on mobile - Stacked card layout for smaller screens - Touch-friendly buttons and controls - Swipe gestures for card navigation - Optimized typography for readability Accessibility & UX - High contrast color options - Keyboard navigation support - Screen reader friendly labels - Loading states for all async operations - Error handling with user-friendly messages - Tooltip help for technical terms Technical Specs - Vue.js 3 + Composition API compatible - CSS Grid/Flexbox layout - CSS custom properties for theming - WebSocket integration ready - Chart.js or similar for data visualization - Responsive breakpoints: 320px, 768px, 1024px, 1440px+ Inspiration Keywords - "Modern server monitoring", "Glass morphism dashboard", "Real-time analytics", "System monitoring UI", "Dark theme dashboard", "Process manager interface", "GPU monitoring display", "Home server admin panel"

I generated a component. What do you want to change? You can also ask me to update it.


Don't have inspiration context
Add inspiration
Ask to modify the component...





Preview
Code

"use client"

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Switch } from '@/components/ui/switch'
import { Input } from '@/components/ui/input'
import { Separator } from '@/components/ui/separator'
import { Alert, AlertDescription } from '@/components/ui/alert'
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
} from 'lucide-react'

interface SystemMetrics {
  cpu: {
    usage: number
    temperature: number
  }
  memory: {
    used: number
    total: number
  }
  gpu: {
    usage: number
    temperature: number
    memory: {
      used: number
      total: number
    }
    fanSpeed: number
    powerConsumption: number
  }
  disk: Array<{
    name: string
    used: number
    total: number
  }>
  network: {
    upload: number
    download: number
  }
  uptime: string
}

interface Process {
  id: number
  name: string
  cpu: number
  memory: number
  gpu: number
}

interface Alert {
  id: number
  type: 'critical' | 'warning' | 'info'
  message: string
  timestamp: string
}

interface ConnectionStatus {
  api: boolean
  database: boolean
  websocket: boolean
}

const CircularProgress: React.FC<{
  value: number
  size?: number
  strokeWidth?: number
  color?: string
  children?: React.ReactNode
}> = ({ value, size = 120, strokeWidth = 8, color = "hsl(var(--primary))", children }) => {
  const radius = (size - strokeWidth) / 2
  const circumference = radius * 2 * Math.PI
  const strokeDasharray = circumference
  const strokeDashoffset = circumference - (value / 100) * circumference

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg width={size} height={size} className="transform -rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="hsl(var(--muted))"
          strokeWidth={strokeWidth}
          fill="transparent"
          className="opacity-20"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={color}
          strokeWidth={strokeWidth}
          fill="transparent"
          strokeDasharray={strokeDasharray}
          strokeDashoffset={strokeDashoffset}
          className="transition-all duration-500 ease-in-out"
          strokeLinecap="round"
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        {children}
      </div>
    </div>
  )
}

const MetricCard: React.FC<{
  title: string
  icon: React.ReactNode
  children: React.ReactNode
  className?: string
}> = ({ title, icon, children, className = "" }) => {
  return (
    <Card className={`backdrop-blur-sm bg-background/80 border-border/50 ${className}`}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium flex items-center gap-2">
          {icon}
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {children}
      </CardContent>
    </Card>
  )
}

const HoofHeartedDashboard: React.FC = () => {
  const [isDarkMode, setIsDarkMode] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const [processFilter, setProcessFilter] = useState<'all' | 'cpu' | 'memory' | 'gpu'>('all')
  const [timeRange, setTimeRange] = useState('1hr')

  // Mock data - in real app this would come from API/WebSocket
  const [connectionStatus] = useState<ConnectionStatus>({
    api: true,
    database: true,
    websocket: true
  })

  const [systemMetrics] = useState<SystemMetrics>({
    cpu: {
      usage: 45,
      temperature: 62
    },
    memory: {
      used: 12.4,
      total: 32
    },
    gpu: {
      usage: 78,
      temperature: 72,
      memory: {
        used: 6.2,
        total: 8
      },
      fanSpeed: 2100,
      powerConsumption: 185
    },
    disk: [
      { name: "C:", used: 450, total: 1000 },
      { name: "D:", used: 1200, total: 2000 }
    ],
    network: {
      upload: 12.5,
      download: 45.2
    },
    uptime: "5d 12h 34m"
  })

  const [processes] = useState<Process[]>([
    { id: 1, name: "chrome.exe", cpu: 15.2, memory: 2.1, gpu: 12.5 },
    { id: 2, name: "blender.exe", cpu: 45.8, memory: 4.2, gpu: 65.3 },
    { id: 3, name: "steam.exe", cpu: 8.1, memory: 1.8, gpu: 5.2 },
    { id: 4, name: "discord.exe", cpu: 3.2, memory: 0.8, gpu: 2.1 },
    { id: 5, name: "obs64.exe", cpu: 12.5, memory: 1.5, gpu: 18.7 }
  ])

  const [alerts] = useState<Alert[]>([
    { id: 1, type: 'warning', message: 'GPU temperature above 70°C', timestamp: '2 min ago' },
    { id: 2, type: 'info', message: 'System backup completed', timestamp: '1 hour ago' },
    { id: 3, type: 'critical', message: 'Disk space low on drive C:', timestamp: '3 hours ago' }
  ])

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [isDarkMode])

  const getTemperatureColor = (temp: number) => {
    if (temp < 60) return "hsl(142, 76%, 36%)" // green
    if (temp < 80) return "hsl(48, 96%, 53%)" // yellow
    return "hsl(0, 84%, 60%)" // red
  }

  const getUsageColor = (usage: number) => {
    if (usage < 50) return "hsl(142, 76%, 36%)" // green
    if (usage < 80) return "hsl(48, 96%, 53%)" // yellow
    return "hsl(0, 84%, 60%)" // red
  }

  const filteredProcesses = processes.filter(process => {
    const matchesSearch = process.name.toLowerCase().includes(searchTerm.toLowerCase())
    if (!matchesSearch) return false
    
    switch (processFilter) {
      case 'cpu': return process.cpu > 10
      case 'memory': return process.memory > 1
      case 'gpu': return process.gpu > 10
      default: return true
    }
  })

  return (
    <div className={`min-h-screen transition-colors duration-300 ${isDarkMode ? 'dark' : ''}`}>
      <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20">
        {/* Header */}
        <header className="border-b border-border/50 backdrop-blur-sm bg-background/80 sticky top-0 z-50">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="text-2xl">🐎</div>
                <div>
                  <h1 className="text-xl font-bold text-foreground">Hoof Hearted</h1>
                  <p className="text-sm text-muted-foreground">Home Server Monitoring</p>
                </div>
              </div>
              
              <div className="flex items-center gap-4">
                {/* Connection Status */}
                <div className="flex items-center gap-2">
                  <div className="flex items-center gap-1">
                    <Server className="h-4 w-4" />
                    {connectionStatus.api ? (
                      <CheckCircle className="h-3 w-3 text-green-500" />
                    ) : (
                      <XCircle className="h-3 w-3 text-red-500" />
                    )}
                  </div>
                  <div className="flex items-center gap-1">
                    <Database className="h-4 w-4" />
                    {connectionStatus.database ? (
                      <CheckCircle className="h-3 w-3 text-green-500" />
                    ) : (
                      <XCircle className="h-3 w-3 text-red-500" />
                    )}
                  </div>
                  <div className="flex items-center gap-1">
                    <Globe className="h-4 w-4" />
                    {connectionStatus.websocket ? (
                      <CheckCircle className="h-3 w-3 text-green-500" />
                    ) : (
                      <XCircle className="h-3 w-3 text-red-500" />
                    )}
                  </div>
                </div>

                {/* Theme Toggle */}
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setIsDarkMode(!isDarkMode)}
                  className="transition-transform hover:scale-110"
                >
                  {isDarkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
                </Button>

                {/* Settings */}
                <Button variant="ghost" size="icon">
                  <Settings className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </header>

        {/* Main Dashboard */}
        <main className="container mx-auto px-4 py-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* System Overview */}
            <MetricCard
              title="System Overview"
              icon={<Activity className="h-4 w-4" />}
              className="lg:col-span-1"
            >
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Cpu className="h-4 w-4" />
                    <span className="text-sm">CPU</span>
                  </div>
                  <span className="text-sm font-medium">{systemMetrics.cpu.usage}%</span>
                </div>
                <Progress value={systemMetrics.cpu.usage} className="h-2" />
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <MemoryStick className="h-4 w-4" />
                    <span className="text-sm">Memory</span>
                  </div>
                  <span className="text-sm font-medium">
                    {systemMetrics.memory.used}GB / {systemMetrics.memory.total}GB
                  </span>
                </div>
                <Progress 
                  value={(systemMetrics.memory.used / systemMetrics.memory.total) * 100} 
                  className="h-2" 
                />

                {systemMetrics.disk.map((disk, index) => (
                  <div key={index}>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <HardDrive className="h-4 w-4" />
                        <span className="text-sm">{disk.name}</span>
                      </div>
                      <span className="text-sm font-medium">
                        {disk.used}GB / {disk.total}GB
                      </span>
                    </div>
                    <Progress value={(disk.used / disk.total) * 100} className="h-2" />
                  </div>
                ))}

                <div className="flex items-center justify-between pt-2">
                  <div className="flex items-center gap-2">
                    <Clock className="h-4 w-4" />
                    <span className="text-sm">Uptime</span>
                  </div>
                  <span className="text-sm font-medium">{systemMetrics.uptime}</span>
                </div>
              </div>
            </MetricCard>

            {/* GPU Monitoring */}
            <MetricCard
              title="GPU Monitoring"
              icon={<Zap className="h-4 w-4" />}
              className="lg:col-span-2"
            >
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="flex flex-col items-center">
                  <CircularProgress
                    value={systemMetrics.gpu.temperature}
                    color={getTemperatureColor(systemMetrics.gpu.temperature)}
                    size={140}
                  >
                    <div className="text-center">
                      <div className="text-2xl font-bold">{systemMetrics.gpu.temperature}°C</div>
                      <div className="text-xs text-muted-foreground">Temperature</div>
                    </div>
                  </CircularProgress>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm">GPU Usage</span>
                      <span className="text-sm font-medium">{systemMetrics.gpu.usage}%</span>
                    </div>
                    <Progress value={systemMetrics.gpu.usage} className="h-2" />
                  </div>
                  
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm">VRAM</span>
                      <span className="text-sm font-medium">
                        {systemMetrics.gpu.memory.used}GB / {systemMetrics.gpu.memory.total}GB
                      </span>
                    </div>
                    <Progress 
                      value={(systemMetrics.gpu.memory.used / systemMetrics.gpu.memory.total) * 100} 
                      className="h-2" 
                    />
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Fan className="h-4 w-4 animate-spin" />
                      <span className="text-sm">Fan Speed</span>
                    </div>
                    <span className="text-sm font-medium">{systemMetrics.gpu.fanSpeed} RPM</span>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Zap className="h-4 w-4" />
                      <span className="text-sm">Power</span>
                    </div>
                    <span className="text-sm font-medium">{systemMetrics.gpu.powerConsumption}W</span>
                  </div>
                </div>
              </div>
            </MetricCard>

            {/* Process Identification */}
            <MetricCard
              title="Process Monitor"
              icon={<TrendingUp className="h-4 w-4" />}
              className="lg:col-span-2"
            >
              <div className="space-y-4">
                <div className="flex flex-col sm:flex-row gap-2">
                  <div className="relative flex-1">
                    <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                    <Input
                      placeholder="Search processes..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-8"
                    />
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant={processFilter === 'all' ? 'default' : 'outline'}
                      size="sm"
                      onClick={() => setProcessFilter('all')}
                    >
                      All
                    </Button>
                    <Button
                      variant={processFilter === 'cpu' ? 'default' : 'outline'}
                      size="sm"
                      onClick={() => setProcessFilter('cpu')}
                    >
                      CPU
                    </Button>
                    <Button
                      variant={processFilter === 'memory' ? 'default' : 'outline'}
                      size="sm"
                      onClick={() => setProcessFilter('memory')}
                    >
                      Memory
                    </Button>
                    <Button
                      variant={processFilter === 'gpu' ? 'default' : 'outline'}
                      size="sm"
                      onClick={() => setProcessFilter('gpu')}
                    >
                      GPU
                    </Button>
                  </div>
                </div>
                
                <div className="space-y-2">
                  {filteredProcesses.slice(0, 5).map((process) => (
                    <div key={process.id} className="flex items-center justify-between p-2 rounded-lg bg-muted/20">
                      <div className="flex-1">
                        <div className="font-medium text-sm">{process.name}</div>
                        <div className="flex gap-4 text-xs text-muted-foreground">
                          <span>CPU: {process.cpu}%</span>
                          <span>Memory: {process.memory}GB</span>
                          <span>GPU: {process.gpu}%</span>
                        </div>
                      </div>
                      <Button variant="ghost" size="sm">
                        <XCircle className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              </div>
            </MetricCard>

            {/* Alerts & Notifications */}
            <MetricCard
              title="Alerts"
              icon={<AlertTriangle className="h-4 w-4" />}
              className="lg:col-span-1"
            >
              <div className="space-y-3">
                {alerts.map((alert) => (
                  <Alert key={alert.id} className={`
                    ${alert.type === 'critical' ? 'border-red-500/50 bg-red-500/10' : ''}
                    ${alert.type === 'warning' ? 'border-yellow-500/50 bg-yellow-500/10' : ''}
                    ${alert.type === 'info' ? 'border-blue-500/50 bg-blue-500/10' : ''}
                  `}>
                    <AlertDescription className="text-sm">
                      <div className="flex items-start justify-between">
                        <div>
                          <p>{alert.message}</p>
                          <p className="text-xs text-muted-foreground mt-1">{alert.timestamp}</p>
                        </div>
                        <Badge variant={
                          alert.type === 'critical' ? 'destructive' : 
                          alert.type === 'warning' ? 'secondary' : 'default'
                        }>
                          {alert.type}
                        </Badge>
                      </div>
                    </AlertDescription>
                  </Alert>
                ))}
              </div>
            </MetricCard>

            {/* Quick Actions */}
            <MetricCard
              title="Quick Actions"
              icon={<Settings className="h-4 w-4" />}
              className="lg:col-span-3"
            >
              <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
                <Button variant="outline" className="flex flex-col gap-2 h-auto py-4">
                  <Power className="h-5 w-5" />
                  <span className="text-xs">Restart</span>
                </Button>
                <Button variant="outline" className="flex flex-col gap-2 h-auto py-4">
                  <RefreshCw className="h-5 w-5" />
                  <span className="text-xs">Refresh GPU</span>
                </Button>
                <Button variant="outline" className="flex flex-col gap-2 h-auto py-4">
                  <Trash2 className="h-5 w-5" />
                  <span className="text-xs">Clear Cache</span>
                </Button>
                <Button variant="outline" className="flex flex-col gap-2 h-auto py-4">
                  <Download className="h-5 w-5" />
                  <span className="text-xs">Export Report</span>
                </Button>
                <Button variant="outline" className="flex flex-col gap-2 h-auto py-4">
                  <Thermometer className="h-5 w-5" />
                  <span className="text-xs">Temp Monitor</span>
                </Button>
                <Button variant="outline" className="flex flex-col gap-2 h-auto py-4">
                  <Wifi className="h-5 w-5" />
                  <span className="text-xs">Network</span>
                </Button>
              </div>
            </MetricCard>
          </div>
        </main>
      </div>
    </div>
  )
}

export default HoofHeartedDashboard

Variant 1



Variant 2



Variant 3



Variant 4



Variant 5



Variant 6



