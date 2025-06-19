#!/usr/bin/env python3
# 🐎 Hoof Hearted - Backend Application Entry Point
# SpicyRiceCakes Home Server Monitoring Dashboard

import os
import sys
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import logging
from threading import Thread
import time

# Import our monitoring systems
from monitoring import GPUMonitoringService
from monitoring.system_monitor import system_monitor
from monitoring.real_time_monitor import RealTimeMonitor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("🐎 Hoof Hearted Backend - GPU Monitoring System")
print("🌶️ SpicyRiceCakes - Making dreams reality!")

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-in-production')
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'postgresql://hoof_hearted:hoof_hearted_dev@localhost:5432/hoof_hearted')
    
    # Enable CORS for frontend communication
    CORS(app, origins="*")
    
    # Initialize SocketIO for real-time updates
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # Initialize monitoring services
    gpu_service = GPUMonitoringService(update_interval=2.0)
    app.gpu_service = gpu_service
    app.system_monitor = system_monitor
    
    # Initialize real-time monitoring system (Sophie's approved architecture)
    real_time_monitor = RealTimeMonitor(socketio, gpu_service, system_monitor)
    app.real_time_monitor = real_time_monitor
    
    @app.route('/health')
    def health_check():
        """Health check endpoint for Docker"""
        return jsonify({
            'status': 'healthy',
            'service': 'hoof-hearted-backend',
            'version': '1.0.0',
            'spicyricecakes': '🌶️🍚🍰'
        })
    
    @app.route('/api/health')
    def api_health_check():
        """API health check endpoint for frontend"""
        gpu_status = "available" if gpu_service.is_available() else "unavailable"
        return jsonify({
            'status': 'healthy',
            'service': 'hoof-hearted-backend',
            'version': '1.0.0',
            'database': 'connected',
            'gpu_monitoring': gpu_status,
            'spicyricecakes': '🌶️🍚🍰'
        })
    
    @app.route('/api/status')
    def api_status():
        """API status endpoint with system information"""
        try:
            # Get basic system info
            system_summary = system_monitor.get_summary()
            gpu_summary = gpu_service.get_summary()
            
            return jsonify({
                'api_version': '1.0.0',
                'status': 'operational',
                'message': 'Hoof Hearted Backend is running!',
                'port': '0909',
                'korean_fart_humor': '공구공구 (gong-goo-gong-goo)',
                'spicyricecakes': 'Emotion → Logic → Joy',
                'monitoring': {
                    'gpu_available': gpu_summary.get('monitoring_available', False),
                    'gpu_count': gpu_summary.get('gpu_count', 0),
                    'system_available': system_summary.get('monitoring_available', False),
                    'platform': system_summary.get('platform', 'unknown')
                },
                'quick_status': {
                    'cpu_usage': system_summary.get('cpu', {}).get('usage_percent', 0),
                    'memory_usage': system_summary.get('memory', {}).get('used_percent', 0),
                    'explanation': system_summary.get('explanation', 'System status unknown')
                }
            })
        except Exception as e:
            logger.error(f"Failed to get status with system info: {e}")
            return jsonify({
                'api_version': '1.0.0',
                'status': 'operational',
                'message': 'Hoof Hearted Backend is running!',
                'port': '0909',
                'korean_fart_humor': '공구공구 (gong-goo-gong-goo)',
                'spicyricecakes': 'Emotion → Logic → Joy',
                'monitoring': {
                    'gpu_available': False,
                    'system_available': False,
                    'error': 'Failed to get monitoring status'
                }
            })
    
    @app.route('/api/gpu/summary')
    def gpu_summary():
        """GPU monitoring summary for dashboard"""
        try:
            summary = gpu_service.get_summary()
            return jsonify(summary)
        except Exception as e:
            logger.error(f"Failed to get GPU summary: {e}")
            return jsonify({
                'error': 'Failed to get GPU information',
                'gpu_count': 0,
                'monitoring_available': False
            }), 500
    
    @app.route('/api/gpu/metrics')
    def gpu_metrics():
        """Detailed GPU metrics with process attribution"""
        try:
            metrics = gpu_service.get_gpu_metrics()
            
            # Convert to JSON-serializable format
            result = []
            for gpu in metrics:
                gpu_data = {
                    'gpu_id': gpu.gpu_id,
                    'name': gpu.name,
                    'vendor': gpu.vendor.value,
                    'utilization_percent': gpu.utilization_percent,
                    'memory_used_mb': gpu.memory_used_mb,
                    'memory_total_mb': gpu.memory_total_mb,
                    'memory_percent': gpu.memory_percent,
                    'temperature_c': gpu.temperature_c,
                    'fan_speed_percent': gpu.fan_speed_percent,
                    'power_draw_watts': gpu.power_draw_watts,
                    'power_limit_watts': gpu.power_limit_watts,
                    'driver_version': gpu.driver_version,
                    'timestamp': gpu.timestamp,
                    'processes': [
                        {
                            'pid': proc.pid,
                            'name': proc.name,
                            'gpu_memory_mb': proc.gpu_memory_mb,
                            'gpu_utilization': proc.gpu_utilization,
                            'command_line': proc.command_line,
                            
                            # Enhanced process identification
                            'username': proc.username,
                            'process_type': proc.process_type,
                            'cpu_percent': proc.cpu_percent,
                            'memory_mb': proc.memory_mb,
                            'runtime_seconds': proc.runtime_seconds,
                            'executable_path': proc.executable_path,
                            
                            # Process classification flags
                            'is_suspected_miner': proc.is_suspected_miner,
                            'is_ml_training': proc.is_ml_training,
                            'is_video_processing': proc.is_video_processing,
                            'is_game': proc.is_game
                        }
                        for proc in gpu.processes
                    ]
                }
                result.append(gpu_data)
            
            return jsonify({
                'gpus': result,
                'timestamp': time.time(),
                'count': len(result)
            })
        
        except Exception as e:
            logger.error(f"Failed to get GPU metrics: {e}")
            return jsonify({
                'error': 'Failed to get GPU metrics',
                'gpus': []
            }), 500
    
    @app.route('/api/gpu/processes')
    def gpu_processes():
        """Detailed process analysis - answers 'Why is my GPU fan running?'"""
        try:
            metrics = gpu_service.get_gpu_metrics()
            
            all_processes = []
            insights = {
                'total_processes': 0,
                'suspected_miners': 0,
                'ml_training': 0,
                'video_processing': 0,
                'games': 0,
                'unknown': 0,
                'high_memory_usage': 0,
                'warnings': []
            }
            
            for gpu in metrics:
                for proc in gpu.processes:
                    # Add GPU context to process info
                    process_info = {
                        'gpu_id': gpu.gpu_id,
                        'gpu_name': gpu.name,
                        'pid': proc.pid,
                        'name': proc.name,
                        'process_type': proc.process_type,
                        'gpu_memory_mb': proc.gpu_memory_mb,
                        'cpu_percent': proc.cpu_percent,
                        'memory_mb': proc.memory_mb,
                        'runtime_seconds': proc.runtime_seconds,
                        'username': proc.username,
                        'command_line': proc.command_line,
                        'executable_path': proc.executable_path,
                        
                        # Classification flags
                        'is_suspected_miner': proc.is_suspected_miner,
                        'is_ml_training': proc.is_ml_training,
                        'is_video_processing': proc.is_video_processing,
                        'is_game': proc.is_game
                    }
                    
                    all_processes.append(process_info)
                    
                    # Update insights
                    insights['total_processes'] += 1
                    if proc.is_suspected_miner:
                        insights['suspected_miners'] += 1
                        insights['warnings'].append(f"⚠️ Suspected cryptocurrency miner detected: {proc.name} (PID {proc.pid})")
                    elif proc.is_ml_training:
                        insights['ml_training'] += 1
                    elif proc.is_video_processing:
                        insights['video_processing'] += 1
                    elif proc.is_game:
                        insights['games'] += 1
                    else:
                        insights['unknown'] += 1
                    
                    # High memory usage warning
                    if proc.gpu_memory_mb > 1000:  # > 1GB GPU memory
                        insights['high_memory_usage'] += 1
                        insights['warnings'].append(f"💾 High GPU memory usage: {proc.name} using {proc.gpu_memory_mb}MB")
            
            # Generate summary message
            if insights['total_processes'] == 0:
                summary = "No GPU processes detected. GPU fan running due to background driver activity or thermal management."
            else:
                summary_parts = []
                if insights['games'] > 0:
                    summary_parts.append(f"{insights['games']} game(s)")
                if insights['ml_training'] > 0:
                    summary_parts.append(f"{insights['ml_training']} ML training process(es)")
                if insights['video_processing'] > 0:
                    summary_parts.append(f"{insights['video_processing']} video processing")
                if insights['suspected_miners'] > 0:
                    summary_parts.append(f"⚠️ {insights['suspected_miners']} suspected miner(s)")
                if insights['unknown'] > 0:
                    summary_parts.append(f"{insights['unknown']} unknown process(es)")
                
                summary = f"GPU fan running because of: {', '.join(summary_parts) if summary_parts else 'unknown processes'}"
            
            return jsonify({
                'summary': summary,
                'processes': all_processes,
                'insights': insights,
                'timestamp': time.time()
            })
        
        except Exception as e:
            logger.error(f"Failed to get GPU process analysis: {e}")
            return jsonify({
                'error': 'Failed to analyze GPU processes',
                'summary': 'Unable to determine why GPU fan is running',
                'processes': [],
                'insights': {}
            }), 500
    
    # System Monitoring Endpoints
    
    @app.route('/api/system/overview')
    def system_overview():
        """Complete system overview with process attribution"""
        try:
            summary = system_monitor.get_summary()
            return jsonify(summary)
        except Exception as e:
            logger.error(f"Failed to get system overview: {e}")
            return jsonify({
                'error': 'Failed to get system information',
                'monitoring_available': False
            }), 500
    
    @app.route('/api/system/cpu')
    def system_cpu():
        """Detailed CPU metrics and top CPU processes"""
        try:
            metrics = system_monitor.get_system_metrics()
            
            # Get top CPU processes
            cpu_processes = sorted(
                [p for p in metrics.top_processes if p.cpu_percent > 1.0],
                key=lambda x: x.cpu_percent, reverse=True
            )[:10]
            
            return jsonify({
                'cpu': {
                    'usage_percent': metrics.cpu.usage_percent,
                    'per_core_usage': metrics.cpu.per_core_usage,
                    'frequency_mhz': metrics.cpu.frequency_mhz,
                    'frequency_max_mhz': metrics.cpu.frequency_max_mhz,
                    'temperature_celsius': metrics.cpu.temperature_celsius,
                    'load_average': metrics.cpu.load_average,
                    'core_count': metrics.cpu.core_count,
                    'thread_count': metrics.cpu.thread_count,
                    'timestamp': metrics.cpu.timestamp
                },
                'top_processes': [
                    {
                        'pid': proc.pid,
                        'name': proc.name,
                        'cpu_percent': proc.cpu_percent,
                        'memory_mb': proc.memory_mb,
                        'memory_percent': proc.memory_percent,
                        'status': proc.status,
                        'username': proc.username,
                        'command_line': proc.command_line,
                        'process_type': proc.process_type,
                        'is_system_intensive': proc.is_system_intensive,
                        'runtime_seconds': proc.runtime_seconds
                    }
                    for proc in cpu_processes
                ],
                'timestamp': time.time()
            })
        except Exception as e:
            logger.error(f"Failed to get CPU metrics: {e}")
            return jsonify({
                'error': 'Failed to get CPU information'
            }), 500
    
    @app.route('/api/system/memory')
    def system_memory():
        """Memory usage with top memory consumers"""
        try:
            metrics = system_monitor.get_system_metrics()
            
            # Get top memory processes
            memory_processes = sorted(
                [p for p in metrics.top_processes if p.memory_percent > 1.0],
                key=lambda x: x.memory_percent, reverse=True
            )[:10]
            
            return jsonify({
                'memory': {
                    'total_mb': metrics.memory.total_mb,
                    'available_mb': metrics.memory.available_mb,
                    'used_mb': metrics.memory.used_mb,
                    'used_percent': metrics.memory.used_percent,
                    'free_mb': metrics.memory.free_mb,
                    'cached_mb': metrics.memory.cached_mb,
                    'buffers_mb': metrics.memory.buffers_mb,
                    'timestamp': metrics.memory.timestamp
                },
                'swap': {
                    'total_mb': metrics.memory.swap_total_mb,
                    'used_mb': metrics.memory.swap_used_mb,
                    'used_percent': metrics.memory.swap_used_percent,
                    'free_mb': metrics.memory.swap_free_mb
                },
                'top_processes': [
                    {
                        'pid': proc.pid,
                        'name': proc.name,
                        'memory_mb': proc.memory_mb,
                        'memory_percent': proc.memory_percent,
                        'cpu_percent': proc.cpu_percent,
                        'status': proc.status,
                        'username': proc.username,
                        'command_line': proc.command_line,
                        'process_type': proc.process_type,
                        'is_system_intensive': proc.is_system_intensive,
                        'runtime_seconds': proc.runtime_seconds
                    }
                    for proc in memory_processes
                ],
                'timestamp': time.time()
            })
        except Exception as e:
            logger.error(f"Failed to get memory metrics: {e}")
            return jsonify({
                'error': 'Failed to get memory information'
            }), 500
    
    @app.route('/api/system/disk')
    def system_disk():
        """Disk usage and I/O statistics"""
        try:
            metrics = system_monitor.get_system_metrics()
            
            return jsonify({
                'disks': [
                    {
                        'device': disk.device,
                        'mountpoint': disk.mountpoint,
                        'filesystem': disk.filesystem,
                        'total_mb': disk.total_mb,
                        'used_mb': disk.used_mb,
                        'free_mb': disk.free_mb,
                        'used_percent': disk.used_percent,
                        'io_read_bytes_per_sec': disk.io_read_bytes_per_sec,
                        'io_write_bytes_per_sec': disk.io_write_bytes_per_sec,
                        'io_read_count_per_sec': disk.io_read_count_per_sec,
                        'io_write_count_per_sec': disk.io_write_count_per_sec,
                        'timestamp': disk.timestamp
                    }
                    for disk in metrics.disks
                ],
                'summary': {
                    'total_disks': len(metrics.disks),
                    'max_usage_percent': max([d.used_percent for d in metrics.disks], default=0),
                    'total_used_mb': sum(d.used_mb for d in metrics.disks),
                    'total_free_mb': sum(d.free_mb for d in metrics.disks)
                },
                'timestamp': time.time()
            })
        except Exception as e:
            logger.error(f"Failed to get disk metrics: {e}")
            return jsonify({
                'error': 'Failed to get disk information'
            }), 500
    
    @app.route('/api/system/network')
    def system_network():
        """Network interface status and bandwidth"""
        try:
            metrics = system_monitor.get_system_metrics()
            
            return jsonify({
                'interfaces': {
                    name: {
                        'name': interface.name,
                        'bytes_sent': interface.bytes_sent,
                        'bytes_recv': interface.bytes_recv,
                        'packets_sent': interface.packets_sent,
                        'packets_recv': interface.packets_recv,
                        'bytes_sent_per_sec': interface.bytes_sent_per_sec,
                        'bytes_recv_per_sec': interface.bytes_recv_per_sec,
                        'is_up': interface.is_up,
                        'addresses': interface.addresses,
                        'timestamp': interface.timestamp
                    }
                    for name, interface in metrics.network.interfaces.items()
                },
                'summary': {
                    'total_bytes_sent': metrics.network.total_bytes_sent,
                    'total_bytes_recv': metrics.network.total_bytes_recv,
                    'total_bytes_sent_per_sec': metrics.network.total_bytes_sent_per_sec,
                    'total_bytes_recv_per_sec': metrics.network.total_bytes_recv_per_sec,
                    'active_connections': metrics.network.active_connections,
                    'active_interfaces': len([i for i in metrics.network.interfaces.values() if i.is_up])
                },
                'timestamp': time.time()
            })
        except Exception as e:
            logger.error(f"Failed to get network metrics: {e}")
            return jsonify({
                'error': 'Failed to get network information'
            }), 500
    
    @socketio.on('connect')
    def handle_connect():
        """Handle WebSocket connection"""
        client_id = request.sid if 'request' in globals() else 'unknown'
        print(f'🔗 Client connected to WebSocket: {client_id}')
        
        # Add client to real-time monitor
        real_time_monitor.add_client(client_id)
        
        # Send initial status
        try:
            gpu_summary = gpu_service.get_summary()
            system_summary = system_monitor.get_summary()
            
            emit('system:initial_status', {
                'gpu': gpu_summary,
                'system': system_summary,
                'timestamp': time.time()
            })
            
            # Start monitoring if this is the first client
            if len(real_time_monitor.connected_clients) == 1:
                real_time_monitor.start_monitoring()
                
        except Exception as e:
            logger.error(f"Failed to send initial status: {e}")
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle WebSocket disconnection"""
        client_id = request.sid if 'request' in globals() else 'unknown'
        print(f'🔌 Client disconnected from WebSocket: {client_id}')
        
        # Remove client from real-time monitor
        real_time_monitor.remove_client(client_id)
        
        # Stop monitoring if no clients connected
        if len(real_time_monitor.connected_clients) == 0:
            real_time_monitor.stop_monitoring()
    
    @socketio.on('request_gpu_update')
    def handle_gpu_update_request():
        """Handle request for immediate metrics update"""
        try:
            # Use real-time monitor for consistent data format
            real_time_monitor.force_update()
            logger.info("🔄 Manual metrics update requested")
        except Exception as e:
            logger.error(f"Failed to send manual update: {e}")
    
    @socketio.on('request_monitoring_stats')
    def handle_monitoring_stats_request():
        """Handle request for monitoring system statistics"""
        try:
            stats = real_time_monitor.get_monitoring_stats()
            emit('system:monitoring_stats', stats)
        except Exception as e:
            logger.error(f"Failed to send monitoring stats: {e}")
    
    # Add endpoint for monitoring system statistics
    @app.route('/api/monitoring/stats')
    def monitoring_stats():
        """Get real-time monitoring system performance statistics"""
        try:
            stats = real_time_monitor.get_monitoring_stats()
            return jsonify(stats)
        except Exception as e:
            logger.error(f"Failed to get monitoring stats: {e}")
            return jsonify({
                'error': 'Failed to get monitoring statistics',
                'active': False
            }), 500
    
    return app, socketio

if __name__ == '__main__':
    # Create Flask app and SocketIO
    app, socketio = create_app()
    
    # Configuration
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"🚀 Starting Hoof Hearted Backend on {host}:{port}")
    print(f"🌐 Dashboard will be available on port 0909 (공구공구!)")
    print(f"🌶️ SpicyRiceCakes philosophy: Emotion → Logic → Joy")
    
    # Start the application
    socketio.run(
        app,
        host=host,
        port=port,
        debug=debug,
        allow_unsafe_werkzeug=True  # For development
    )