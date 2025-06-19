#!/usr/bin/env python3
# 🐎 Hoof Hearted - Real-Time Monitoring Engine
# SpicyRiceCakes Real-Time Data Collection and WebSocket Emission

import time
import logging
from typing import Dict, Any, Optional
from threading import Lock
import json

# Setup logging
logger = logging.getLogger(__name__)

class RealTimeMonitor:
    """
    Unified real-time monitoring system that collects GPU and system metrics
    and emits them via WebSocket with intelligent update frequencies.
    
    Implements Sophie's approved architecture with tiered updates and event-driven alerts.
    """
    
    # Tiered update frequencies (seconds)
    UPDATE_FREQUENCIES = {
        'critical': 1,      # CPU >90%, GPU temp >80°C, suspected miners
        'important': 2,     # GPU/CPU usage, process changes
        'standard': 5,      # Memory, basic system metrics
        'background': 10    # Network stats, disk I/O
    }
    
    def __init__(self, socketio, gpu_service, system_monitor):
        """
        Initialize the real-time monitoring system.
        
        Args:
            socketio: Flask-SocketIO instance for WebSocket emission
            gpu_service: GPUMonitoringService instance
            system_monitor: SystemMonitor instance
        """
        self.socketio = socketio
        self.gpu_service = gpu_service
        self.system_monitor = system_monitor
        
        # State management
        self.last_metrics = {}
        self.last_update_times = {}
        self.connected_clients = set()
        self.monitoring_active = False
        
        # Thread safety
        self._lock = Lock()
        
        # Performance tracking
        self.update_count = 0
        self.error_count = 0
        self.start_time = time.time()
        
        logger.info("🔧 RealTimeMonitor initialized with tiered update system")
    
    def start_monitoring(self):
        """Start the background monitoring task using SocketIO's task manager."""
        if self.monitoring_active:
            logger.warning("Real-time monitoring already active")
            return
            
        try:
            self.monitoring_active = True
            # Use SocketIO's background task manager (Sophie's recommendation)
            self.socketio.start_background_task(target=self._monitoring_loop)
            logger.info("🚀 Real-time monitoring started successfully")
        except Exception as e:
            logger.error(f"❌ Failed to start real-time monitoring: {e}")
            self.monitoring_active = False
            raise
    
    def stop_monitoring(self):
        """Stop the background monitoring task."""
        self.monitoring_active = False
        logger.info("⏹️ Real-time monitoring stopped")
    
    def add_client(self, client_id: str):
        """Add a connected client for tracking."""
        with self._lock:
            self.connected_clients.add(client_id)
        logger.info(f"👤 Client connected: {client_id} (Total: {len(self.connected_clients)})")
    
    def remove_client(self, client_id: str):
        """Remove a disconnected client."""
        with self._lock:
            self.connected_clients.discard(client_id)
        logger.info(f"👋 Client disconnected: {client_id} (Total: {len(self.connected_clients)})")
    
    def _monitoring_loop(self):
        """
        Main monitoring loop that collects and emits metrics based on tiered frequencies.
        Runs in background task managed by SocketIO.
        """
        logger.info("🔄 Real-time monitoring loop started")
        
        while self.monitoring_active:
            try:
                current_time = time.time()
                
                # Check if we have any connected clients
                if not self.connected_clients:
                    time.sleep(2)  # Sleep longer when no clients
                    continue
                
                # Collect and emit metrics based on update frequencies
                self._collect_and_emit_metrics(current_time)
                
                # Performance tracking
                self.update_count += 1
                
                # Sleep for shortest update interval (critical = 1 second)
                time.sleep(self.UPDATE_FREQUENCIES['critical'])
                
            except Exception as e:
                self.error_count += 1
                logger.error(f"❌ Error in monitoring loop: {e}")
                # Continue monitoring even if there's an error
                time.sleep(5)  # Sleep longer on error to prevent spam
    
    def _collect_and_emit_metrics(self, current_time: float):
        """
        Collect metrics from GPU and system monitors and emit via WebSocket
        using intelligent update frequency logic.
        """
        try:
            # Collect GPU metrics
            gpu_data = self._collect_gpu_metrics()
            
            # Collect system metrics  
            system_data = self._collect_system_metrics()
            
            # Determine update urgency and emit accordingly
            self._emit_tiered_updates(gpu_data, system_data, current_time)
            
        except Exception as e:
            logger.error(f"❌ Failed to collect and emit metrics: {e}")
            raise
    
    def _collect_gpu_metrics(self) -> Dict[str, Any]:
        """Collect GPU metrics with error handling."""
        try:
            if not self.gpu_service.is_available():
                return {'available': False, 'gpus': []}
            
            summary = self.gpu_service.get_summary()
            metrics = self.gpu_service.get_gpu_metrics()
            
            # Convert to JSON-serializable format
            gpu_data = []
            for gpu in metrics:
                gpu_info = {
                    'gpu_id': gpu.gpu_id,
                    'name': gpu.name,
                    'vendor': gpu.vendor.value,
                    'utilization_percent': gpu.utilization_percent,
                    'memory_percent': gpu.memory_percent,
                    'temperature_c': gpu.temperature_c,
                    'fan_speed_percent': gpu.fan_speed_percent,
                    'power_draw_watts': gpu.power_draw_watts,
                    'timestamp': gpu.timestamp,
                    'processes': [
                        {
                            'pid': proc.pid,
                            'name': proc.name,
                            'gpu_memory_mb': proc.gpu_memory_mb,
                            'process_type': proc.process_type,
                            'is_suspected_miner': proc.is_suspected_miner,
                            'is_ml_training': proc.is_ml_training,
                            'is_video_processing': proc.is_video_processing,
                            'is_game': proc.is_game
                        }
                        for proc in gpu.processes
                    ]
                }
                gpu_data.append(gpu_info)
            
            return {
                'available': True,
                'summary': summary,
                'gpus': gpu_data,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to collect GPU metrics: {e}")
            return {'available': False, 'error': str(e)}
    
    def _collect_system_metrics(self) -> Dict[str, Any]:
        """Collect system metrics with error handling."""
        try:
            summary = self.system_monitor.get_summary()
            metrics = self.system_monitor.get_system_metrics()
            
            return {
                'available': True,
                'summary': summary,
                'cpu': {
                    'usage_percent': metrics.cpu.usage_percent,
                    'per_core_usage': metrics.cpu.per_core_usage,
                    'temperature_celsius': metrics.cpu.temperature_celsius,
                    'load_average': metrics.cpu.load_average,
                    'frequency_mhz': metrics.cpu.frequency_mhz
                },
                'memory': {
                    'used_percent': metrics.memory.used_percent,
                    'used_mb': metrics.memory.used_mb,
                    'available_mb': metrics.memory.available_mb,
                    'total_mb': metrics.memory.total_mb
                },
                'top_processes': [
                    {
                        'pid': proc.pid,
                        'name': proc.name,
                        'cpu_percent': proc.cpu_percent,
                        'memory_percent': proc.memory_percent,
                        'process_type': proc.process_type,
                        'is_system_intensive': proc.is_system_intensive
                    }
                    for proc in metrics.top_processes[:10]  # Top 10 processes
                ],
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to collect system metrics: {e}")
            return {'available': False, 'error': str(e)}
    
    def _emit_tiered_updates(self, gpu_data: Dict, system_data: Dict, current_time: float):
        """
        Emit updates based on tiered frequency system and event-driven alerts.
        Implements Sophie's approved architecture for intelligent update management.
        """
        # Determine update urgency based on current metrics
        urgency_level = self._calculate_urgency(gpu_data, system_data)
        
        # Check if we should emit based on update frequency
        should_emit = self._should_emit_update(urgency_level, current_time)
        
        if should_emit:
            # Emit standard metrics update
            self._emit_metrics_update(gpu_data, system_data, urgency_level)
            
            # Check for and emit event-driven alerts
            self._check_and_emit_alerts(gpu_data, system_data)
            
            # Update last emission time
            self.last_update_times[urgency_level] = current_time
    
    def _calculate_urgency(self, gpu_data: Dict, system_data: Dict) -> str:
        """
        Calculate the urgency level of current metrics to determine update frequency.
        
        Returns:
            str: 'critical', 'important', 'standard', or 'background'
        """
        # Critical conditions (1-second updates)
        if system_data.get('available'):
            cpu_usage = system_data.get('cpu', {}).get('usage_percent', 0)
            cpu_temp = system_data.get('cpu', {}).get('temperature_celsius', 0)
            
            if cpu_usage > 90 or cpu_temp > 80:
                return 'critical'
        
        if gpu_data.get('available'):
            for gpu in gpu_data.get('gpus', []):
                temp = gpu.get('temperature_c', 0)
                utilization = gpu.get('utilization_percent', 0)
                
                # Critical: High temperature or suspected miner
                if temp > 80 or any(proc.get('is_suspected_miner') for proc in gpu.get('processes', [])):
                    return 'critical'
                
                # Important: High GPU usage or active processes
                if utilization > 50 or len(gpu.get('processes', [])) > 0:
                    return 'important'
        
        # Important conditions (2-second updates)
        if system_data.get('available'):
            cpu_usage = system_data.get('cpu', {}).get('usage_percent', 0)
            memory_usage = system_data.get('memory', {}).get('used_percent', 0)
            
            if cpu_usage > 70 or memory_usage > 80:
                return 'important'
        
        # Standard conditions (5-second updates)
        return 'standard'
    
    def _should_emit_update(self, urgency_level: str, current_time: float) -> bool:
        """Check if enough time has passed to emit an update for this urgency level."""
        frequency = self.UPDATE_FREQUENCIES[urgency_level]
        last_update = self.last_update_times.get(urgency_level, 0)
        
        return (current_time - last_update) >= frequency
    
    def _emit_metrics_update(self, gpu_data: Dict, system_data: Dict, urgency_level: str):
        """Emit the main metrics update via WebSocket."""
        try:
            update_payload = {
                'type': 'metrics_update',
                'urgency': urgency_level,
                'gpu': gpu_data,
                'system': system_data,
                'timestamp': time.time(),
                'update_count': self.update_count
            }
            
            # Use namespaced event names (Sophie's recommendation)
            self.socketio.emit('system:metrics_update', update_payload)
            
            # Also emit legacy events for backward compatibility
            if gpu_data.get('available'):
                self.socketio.emit('gpu_status_update', gpu_data.get('summary', {}))
            
        except Exception as e:
            logger.error(f"❌ Failed to emit metrics update: {e}")
    
    def _check_and_emit_alerts(self, gpu_data: Dict, system_data: Dict):
        """
        Check for alert conditions and emit event-driven notifications.
        Implements Sophie's approved event-driven alert system.
        """
        alerts = []
        
        # GPU-based alerts
        if gpu_data.get('available'):
            for gpu in gpu_data.get('gpus', []):
                gpu_id = gpu.get('gpu_id', 'unknown')
                temp = gpu.get('temperature_c', 0)
                utilization = gpu.get('utilization_percent', 0)
                
                # Temperature alerts
                if temp > 85:
                    alerts.append({
                        'type': 'critical',
                        'category': 'gpu_temperature',
                        'message': f"🔥 GPU {gpu_id} critical temperature: {temp}°C",
                        'gpu_id': gpu_id,
                        'value': temp,
                        'threshold': 85
                    })
                elif temp > 75:
                    alerts.append({
                        'type': 'warning',
                        'category': 'gpu_temperature',
                        'message': f"⚠️ GPU {gpu_id} high temperature: {temp}°C",
                        'gpu_id': gpu_id,
                        'value': temp,
                        'threshold': 75
                    })
                
                # Process-based alerts
                for proc in gpu.get('processes', []):
                    if proc.get('is_suspected_miner'):
                        alerts.append({
                            'type': 'security',
                            'category': 'suspected_miner',
                            'message': f"🚨 Suspected cryptocurrency miner detected: {proc.get('name')} (PID {proc.get('pid')})",
                            'process': proc,
                            'gpu_id': gpu_id
                        })
        
        # System-based alerts  
        if system_data.get('available'):
            cpu_usage = system_data.get('cpu', {}).get('usage_percent', 0)
            memory_usage = system_data.get('memory', {}).get('used_percent', 0)
            
            # High CPU usage alert
            if cpu_usage > 90:
                alerts.append({
                    'type': 'critical',
                    'category': 'cpu_usage',
                    'message': f"🔥 Critical CPU usage: {cpu_usage:.1f}%",
                    'value': cpu_usage,
                    'threshold': 90
                })
            
            # High memory usage alert
            if memory_usage > 90:
                alerts.append({
                    'type': 'critical',
                    'category': 'memory_usage',
                    'message': f"💾 Critical memory usage: {memory_usage:.1f}%",
                    'value': memory_usage,
                    'threshold': 90
                })
        
        # Emit alerts if any found
        if alerts:
            try:
                alert_payload = {
                    'alerts': alerts,
                    'timestamp': time.time(),
                    'count': len(alerts)
                }
                
                # Use namespaced event names (Sophie's recommendation)
                self.socketio.emit('system:alerts', alert_payload)
                
                # Also emit legacy high usage alert for backward compatibility
                if any(alert['category'] in ['gpu_temperature', 'suspected_miner'] for alert in alerts):
                    self.socketio.emit('high_gpu_usage_alert', alert_payload)
                
                logger.info(f"🚨 Emitted {len(alerts)} alert(s)")
                
            except Exception as e:
                logger.error(f"❌ Failed to emit alerts: {e}")
    
    def get_monitoring_stats(self) -> Dict[str, Any]:
        """Get performance statistics for the monitoring system."""
        uptime = time.time() - self.start_time
        
        return {
            'active': self.monitoring_active,
            'connected_clients': len(self.connected_clients),
            'update_count': self.update_count,
            'error_count': self.error_count,
            'uptime_seconds': uptime,
            'updates_per_minute': (self.update_count / uptime * 60) if uptime > 0 else 0,
            'error_rate': (self.error_count / self.update_count) if self.update_count > 0 else 0
        }
    
    def force_update(self):
        """Force an immediate update of all metrics (for manual refresh)."""
        try:
            if not self.monitoring_active:
                logger.warning("Cannot force update - monitoring not active")
                return
            
            current_time = time.time()
            
            # Collect metrics
            gpu_data = self._collect_gpu_metrics()
            system_data = self._collect_system_metrics()
            
            # Emit immediately regardless of frequency limits
            self._emit_metrics_update(gpu_data, system_data, 'critical')
            self._check_and_emit_alerts(gpu_data, system_data)
            
            logger.info("🔄 Forced metrics update completed")
            
        except Exception as e:
            logger.error(f"❌ Failed to force update: {e}")
            raise