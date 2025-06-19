#!/usr/bin/env python3
"""
🐎 Hoof Hearted - System Monitoring Module
SpicyRiceCakes - Comprehensive system metrics with process attribution

Extends GPU monitoring to answer "Why is my server fan running?" 
with CPU, memory, disk, and network analysis.
"""

import logging
import time
import platform
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import psutil

logger = logging.getLogger(__name__)


@dataclass
class CPUMetrics:
    """CPU usage and performance metrics"""
    usage_percent: float
    per_core_usage: List[float]
    frequency_mhz: Optional[float]
    frequency_max_mhz: Optional[float]
    temperature_celsius: Optional[float]
    load_average: Optional[Tuple[float, float, float]]  # 1min, 5min, 15min
    core_count: int
    thread_count: int
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


@dataclass
class MemoryMetrics:
    """Memory usage and swap information"""
    total_mb: int
    available_mb: int
    used_mb: int
    used_percent: float
    free_mb: int
    swap_total_mb: int
    swap_used_mb: int
    swap_used_percent: float
    swap_free_mb: int
    cached_mb: Optional[int] = None
    buffers_mb: Optional[int] = None
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


@dataclass
class DiskMetrics:
    """Individual disk/partition metrics"""
    device: str
    mountpoint: str
    filesystem: str
    total_mb: int
    used_mb: int
    free_mb: int
    used_percent: float
    io_read_bytes_per_sec: Optional[float] = None
    io_write_bytes_per_sec: Optional[float] = None
    io_read_count_per_sec: Optional[float] = None
    io_write_count_per_sec: Optional[float] = None
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


@dataclass
class NetworkInterface:
    """Individual network interface metrics"""
    name: str
    bytes_sent: int
    bytes_recv: int
    packets_sent: int
    packets_recv: int
    bytes_sent_per_sec: Optional[float] = None
    bytes_recv_per_sec: Optional[float] = None
    is_up: bool = True
    addresses: List[str] = None
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()
        if self.addresses is None:
            self.addresses = []


@dataclass
class NetworkMetrics:
    """Network usage and interface information"""
    interfaces: Dict[str, NetworkInterface]
    total_bytes_sent: int
    total_bytes_recv: int
    active_connections: int
    total_bytes_sent_per_sec: Optional[float] = None
    total_bytes_recv_per_sec: Optional[float] = None
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


@dataclass
class SystemProcess:
    """Resource-intensive system process information"""
    pid: int
    name: str
    cpu_percent: float
    memory_mb: int
    memory_percent: float
    status: str
    username: Optional[str] = None
    command_line: Optional[str] = None
    executable_path: Optional[str] = None
    runtime_seconds: Optional[float] = None
    process_type: Optional[str] = None  # 'backup', 'system', 'development', 'database', 'unknown'
    is_system_intensive: bool = False
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


@dataclass
class SystemMetrics:
    """Complete system monitoring metrics"""
    cpu: CPUMetrics
    memory: MemoryMetrics
    disks: List[DiskMetrics]
    network: NetworkMetrics
    top_processes: List[SystemProcess]
    platform_info: Dict[str, str]
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class SystemProcessClassifier:
    """Extended process classifier for system-intensive processes"""
    
    # System maintenance and backup processes
    BACKUP_PROCESSES = [
        r'.*backup.*', r'.*time.?machine.*', r'.*rsync.*', r'.*rclone.*',
        r'.*duplicati.*', r'.*borg.*', r'.*restic.*', r'.*carbon.*copy.*',
        r'.*backblaze.*', r'.*crashplan.*'
    ]
    
    # Development and compilation processes
    DEVELOPMENT_PROCESSES = [
        r'.*gcc.*', r'.*clang.*', r'.*make.*', r'.*cmake.*', r'.*npm.*',
        r'.*yarn.*', r'.*webpack.*', r'.*docker.*', r'.*build.*', r'.*compile.*',
        r'.*gradle.*', r'.*maven.*', r'.*xcode.*', r'.*swift.*'
    ]
    
    # Database and data processing
    DATABASE_PROCESSES = [
        r'.*postgres.*', r'.*mysql.*', r'.*mongodb.*', r'.*redis.*',
        r'.*elasticsearch.*', r'.*cassandra.*', r'.*oracle.*', r'.*sqlite.*',
        r'.*influxdb.*', r'.*timescaledb.*'
    ]
    
    # System and OS processes
    SYSTEM_PROCESSES = [
        r'.*kernel.*', r'.*system.*', r'.*service.*', r'.*daemon.*',
        r'.*mds.*', r'.*spotlight.*', r'.*windowserver.*', r'.*finder.*',
        r'.*dock.*', r'.*activity.?monitor.*'
    ]
    
    @staticmethod
    def classify_process(process_name: str, command_line: str = "", executable_path: str = "") -> Dict[str, any]:
        """Classify system process to explain high resource usage"""
        from .gpu_monitor import ProcessClassifier
        
        # First try GPU-specific classification
        gpu_classification = ProcessClassifier.classify_process(process_name, command_line, executable_path)
        if gpu_classification['process_type'] != 'unknown':
            return gpu_classification
        
        # Extended classification for system processes
        classification = {
            'process_type': 'unknown',
            'is_system_intensive': False,
            'confidence': 0.0,
            'reason': 'Unknown process type'
        }
        
        text_to_analyze = f"{process_name} {command_line} {executable_path}".lower()
        
        # Check for backup processes
        for pattern in SystemProcessClassifier.BACKUP_PROCESSES:
            import re
            if re.search(pattern, text_to_analyze, re.IGNORECASE):
                classification.update({
                    'process_type': 'backup',
                    'is_system_intensive': True,
                    'confidence': 0.8,
                    'reason': 'Backup or synchronization process'
                })
                return classification
        
        # Check for development processes
        for pattern in SystemProcessClassifier.DEVELOPMENT_PROCESSES:
            import re
            if re.search(pattern, text_to_analyze, re.IGNORECASE):
                classification.update({
                    'process_type': 'development',
                    'is_system_intensive': True,
                    'confidence': 0.7,
                    'reason': 'Development or compilation process'
                })
                return classification
        
        # Check for database processes
        for pattern in SystemProcessClassifier.DATABASE_PROCESSES:
            import re
            if re.search(pattern, text_to_analyze, re.IGNORECASE):
                classification.update({
                    'process_type': 'database',
                    'is_system_intensive': True,
                    'confidence': 0.8,
                    'reason': 'Database or data processing service'
                })
                return classification
        
        # Check for system processes
        for pattern in SystemProcessClassifier.SYSTEM_PROCESSES:
            import re
            if re.search(pattern, text_to_analyze, re.IGNORECASE):
                classification.update({
                    'process_type': 'system',
                    'is_system_intensive': False,  # System processes are normal
                    'confidence': 0.6,
                    'reason': 'System or OS process'
                })
                return classification
        
        return classification


class SystemMonitor:
    """Comprehensive system monitoring service"""
    
    def __init__(self, update_interval: float = 2.0):
        self.update_interval = update_interval
        self._last_update = 0
        self._cached_metrics = None
        self._last_disk_io = None
        self._last_network_io = None
        self._platform_info = self._get_platform_info()
        
        logger.info("🖥️ System monitoring initialized")
    
    def _get_platform_info(self) -> Dict[str, str]:
        """Get platform and system information"""
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'hostname': platform.node()
        }
    
    def get_cpu_metrics(self) -> CPUMetrics:
        """Get comprehensive CPU metrics"""
        # CPU usage (with short interval for responsiveness)
        cpu_percent = psutil.cpu_percent(interval=0.1)
        per_core_usage = psutil.cpu_percent(interval=0.1, percpu=True)
        
        # CPU frequency
        try:
            cpu_freq = psutil.cpu_freq()
            frequency_mhz = cpu_freq.current if cpu_freq else None
            frequency_max_mhz = cpu_freq.max if cpu_freq else None
        except:
            frequency_mhz = None
            frequency_max_mhz = None
        
        # CPU temperature (platform-specific)
        temperature_celsius = self._get_cpu_temperature()
        
        # Load average (Unix-like systems)
        try:
            load_average = psutil.getloadavg()
        except:
            load_average = None
        
        # CPU counts
        core_count = psutil.cpu_count(logical=False) or 0
        thread_count = psutil.cpu_count(logical=True) or 0
        
        return CPUMetrics(
            usage_percent=cpu_percent,
            per_core_usage=per_core_usage,
            frequency_mhz=frequency_mhz,
            frequency_max_mhz=frequency_max_mhz,
            temperature_celsius=temperature_celsius,
            load_average=load_average,
            core_count=core_count,
            thread_count=thread_count
        )
    
    def _get_cpu_temperature(self) -> Optional[float]:
        """Get CPU temperature (platform-specific)"""
        try:
            # Try psutil sensors (Linux mainly)
            if hasattr(psutil, 'sensors_temperatures'):
                temps = psutil.sensors_temperatures()
                if temps:
                    # Look for common CPU temperature sensor names
                    for name, entries in temps.items():
                        if any(keyword in name.lower() for keyword in ['cpu', 'core', 'processor']):
                            if entries:
                                return entries[0].current
            
            # macOS-specific temperature reading would go here
            # Windows-specific temperature reading would go here
            
        except Exception as e:
            logger.debug(f"CPU temperature reading failed: {e}")
        
        return None
    
    def get_memory_metrics(self) -> MemoryMetrics:
        """Get comprehensive memory metrics"""
        # Virtual memory
        vmem = psutil.virtual_memory()
        
        # Swap memory
        swap = psutil.swap_memory()
        
        return MemoryMetrics(
            total_mb=vmem.total // (1024 * 1024),
            available_mb=vmem.available // (1024 * 1024),
            used_mb=vmem.used // (1024 * 1024),
            used_percent=vmem.percent,
            free_mb=vmem.free // (1024 * 1024),
            swap_total_mb=swap.total // (1024 * 1024),
            swap_used_mb=swap.used // (1024 * 1024),
            swap_used_percent=swap.percent,
            swap_free_mb=swap.free // (1024 * 1024),
            cached_mb=getattr(vmem, 'cached', 0) // (1024 * 1024),
            buffers_mb=getattr(vmem, 'buffers', 0) // (1024 * 1024)
        )
    
    def get_disk_metrics(self) -> List[DiskMetrics]:
        """Get disk usage and I/O metrics"""
        disk_metrics = []
        
        # Get disk usage for all mounted partitions
        partitions = psutil.disk_partitions()
        
        # Get current I/O counters for rate calculation
        try:
            current_disk_io = psutil.disk_io_counters(perdisk=True)
            current_time = time.time()
        except:
            current_disk_io = None
            current_time = None
        
        for partition in partitions:
            try:
                # Skip special filesystems on Unix-like systems
                if partition.fstype in ['devfs', 'proc', 'sysfs', 'tmpfs', 'devtmpfs']:
                    continue
                
                usage = psutil.disk_usage(partition.mountpoint)
                
                # Calculate I/O rates if we have previous data
                io_read_bytes_per_sec = None
                io_write_bytes_per_sec = None
                io_read_count_per_sec = None
                io_write_count_per_sec = None
                
                if (current_disk_io and self._last_disk_io and 
                    partition.device in current_disk_io and 
                    partition.device in self._last_disk_io):
                    
                    time_delta = current_time - self._last_update
                    if time_delta > 0:
                        curr_io = current_disk_io[partition.device]
                        last_io = self._last_disk_io[partition.device]
                        
                        io_read_bytes_per_sec = (curr_io.read_bytes - last_io.read_bytes) / time_delta
                        io_write_bytes_per_sec = (curr_io.write_bytes - last_io.write_bytes) / time_delta
                        io_read_count_per_sec = (curr_io.read_count - last_io.read_count) / time_delta
                        io_write_count_per_sec = (curr_io.write_count - last_io.write_count) / time_delta
                
                disk_metrics.append(DiskMetrics(
                    device=partition.device,
                    mountpoint=partition.mountpoint,
                    filesystem=partition.fstype,
                    total_mb=usage.total // (1024 * 1024),
                    used_mb=usage.used // (1024 * 1024),
                    free_mb=usage.free // (1024 * 1024),
                    used_percent=(usage.used / usage.total) * 100,
                    io_read_bytes_per_sec=io_read_bytes_per_sec,
                    io_write_bytes_per_sec=io_write_bytes_per_sec,
                    io_read_count_per_sec=io_read_count_per_sec,
                    io_write_count_per_sec=io_write_count_per_sec
                ))
                
            except PermissionError:
                # Skip drives we can't access
                continue
            except Exception as e:
                logger.warning(f"Failed to get disk metrics for {partition.device}: {e}")
                continue
        
        # Store current I/O data for next calculation
        self._last_disk_io = current_disk_io
        
        return disk_metrics
    
    def get_network_metrics(self) -> NetworkMetrics:
        """Get network interface and usage metrics"""
        # Get current network I/O counters
        try:
            net_io = psutil.net_io_counters(pernic=True)
            current_time = time.time()
        except:
            net_io = {}
            current_time = None
        
        # Get network interface addresses
        try:
            net_if_addrs = psutil.net_if_addrs()
        except:
            net_if_addrs = {}
        
        # Get interface statistics
        try:
            net_if_stats = psutil.net_if_stats()
        except:
            net_if_stats = {}
        
        interfaces = {}
        total_bytes_sent = 0
        total_bytes_recv = 0
        total_bytes_sent_per_sec = 0
        total_bytes_recv_per_sec = 0
        
        for interface_name, io_counters in net_io.items():
            # Skip loopback interfaces
            if interface_name.startswith('lo'):
                continue
            
            # Get interface addresses
            addresses = []
            if interface_name in net_if_addrs:
                addresses = [addr.address for addr in net_if_addrs[interface_name] 
                           if addr.family in (2, 10)]  # IPv4 and IPv6
            
            # Check if interface is up
            is_up = True
            if interface_name in net_if_stats:
                is_up = net_if_stats[interface_name].isup
            
            # Calculate transfer rates
            bytes_sent_per_sec = None
            bytes_recv_per_sec = None
            
            if (self._last_network_io and interface_name in self._last_network_io and current_time):
                time_delta = current_time - self._last_update
                if time_delta > 0:
                    last_io = self._last_network_io[interface_name]
                    bytes_sent_per_sec = (io_counters.bytes_sent - last_io.bytes_sent) / time_delta
                    bytes_recv_per_sec = (io_counters.bytes_recv - last_io.bytes_recv) / time_delta
                    
                    if bytes_sent_per_sec >= 0:  # Sanity check
                        total_bytes_sent_per_sec += bytes_sent_per_sec
                    if bytes_recv_per_sec >= 0:  # Sanity check
                        total_bytes_recv_per_sec += bytes_recv_per_sec
            
            interfaces[interface_name] = NetworkInterface(
                name=interface_name,
                bytes_sent=io_counters.bytes_sent,
                bytes_recv=io_counters.bytes_recv,
                packets_sent=io_counters.packets_sent,
                packets_recv=io_counters.packets_recv,
                bytes_sent_per_sec=bytes_sent_per_sec,
                bytes_recv_per_sec=bytes_recv_per_sec,
                is_up=is_up,
                addresses=addresses
            )
            
            total_bytes_sent += io_counters.bytes_sent
            total_bytes_recv += io_counters.bytes_recv
        
        # Store current network I/O data for next calculation
        self._last_network_io = net_io
        
        # Get active connections count
        try:
            active_connections = len(psutil.net_connections())
        except:
            active_connections = 0
        
        return NetworkMetrics(
            interfaces=interfaces,
            total_bytes_sent=total_bytes_sent,
            total_bytes_recv=total_bytes_recv,
            total_bytes_sent_per_sec=total_bytes_sent_per_sec if current_time else None,
            total_bytes_recv_per_sec=total_bytes_recv_per_sec if current_time else None,
            active_connections=active_connections
        )
    
    def get_top_processes(self, limit: int = 10) -> List[SystemProcess]:
        """Get top resource-consuming processes"""
        processes = []
        
        try:
            # Get all processes with resource usage
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 
                                           'memory_percent', 'status', 'username', 
                                           'cmdline', 'exe', 'create_time']):
                try:
                    info = proc.info
                    
                    # Skip kernel threads and very low usage processes
                    if info['cpu_percent'] < 0.1 and info['memory_percent'] < 0.1:
                        continue
                    
                    # Get additional process information
                    command_line = ' '.join(info['cmdline']) if info['cmdline'] else ""
                    executable_path = info['exe'] if info['exe'] else ""
                    runtime_seconds = time.time() - info['create_time'] if info['create_time'] else None
                    
                    # Classify process
                    classification = SystemProcessClassifier.classify_process(
                        info['name'], command_line, executable_path
                    )
                    
                    processes.append(SystemProcess(
                        pid=info['pid'],
                        name=info['name'],
                        cpu_percent=info['cpu_percent'],
                        memory_mb=info['memory_info'].rss // (1024 * 1024) if info['memory_info'] else 0,
                        memory_percent=info['memory_percent'],
                        status=info['status'],
                        username=info['username'],
                        command_line=command_line,
                        executable_path=executable_path,
                        runtime_seconds=runtime_seconds,
                        process_type=classification['process_type'],
                        is_system_intensive=classification.get('is_system_intensive', False)
                    ))
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                except Exception as e:
                    logger.debug(f"Error processing process {proc.pid}: {e}")
                    continue
            
            # Sort by CPU usage (descending) and limit results
            processes.sort(key=lambda p: p.cpu_percent, reverse=True)
            return processes[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get top processes: {e}")
            return []
    
    def get_system_metrics(self, force_update: bool = False) -> SystemMetrics:
        """Get complete system metrics with caching"""
        current_time = time.time()
        
        if force_update or (current_time - self._last_update) >= self.update_interval:
            try:
                cpu_metrics = self.get_cpu_metrics()
                memory_metrics = self.get_memory_metrics()
                disk_metrics = self.get_disk_metrics()
                network_metrics = self.get_network_metrics()
                top_processes = self.get_top_processes()
                
                self._cached_metrics = SystemMetrics(
                    cpu=cpu_metrics,
                    memory=memory_metrics,
                    disks=disk_metrics,
                    network=network_metrics,
                    top_processes=top_processes,
                    platform_info=self._platform_info
                )
                
                self._last_update = current_time
                
                # Log interesting system status
                self._log_system_status(self._cached_metrics)
                
            except Exception as e:
                logger.error(f"Failed to update system metrics: {e}")
                if self._cached_metrics is None:
                    # Return minimal metrics if we have nothing
                    self._cached_metrics = self._get_fallback_metrics()
        
        return self._cached_metrics
    
    def _get_fallback_metrics(self) -> SystemMetrics:
        """Get minimal fallback metrics when monitoring fails"""
        return SystemMetrics(
            cpu=CPUMetrics(0, [], None, None, None, None, 0, 0),
            memory=MemoryMetrics(0, 0, 0, 0, 0, 0, 0, 0, 0),
            disks=[],
            network=NetworkMetrics({}, 0, 0, None, None, 0),
            top_processes=[],
            platform_info=self._platform_info
        )
    
    def _log_system_status(self, metrics: SystemMetrics):
        """Log system status for debugging"""
        if metrics.cpu.usage_percent > 70:
            logger.info(f"🔥 High CPU usage: {metrics.cpu.usage_percent:.1f}%")
        
        if metrics.memory.used_percent > 80:
            logger.info(f"💾 High memory usage: {metrics.memory.used_percent:.1f}%")
        
        # Log high-resource processes
        intensive_processes = [p for p in metrics.top_processes if p.cpu_percent > 20 or p.memory_percent > 10]
        if intensive_processes:
            logger.info(f"⚡ {len(intensive_processes)} resource-intensive processes detected")
            for proc in intensive_processes[:3]:  # Log top 3
                logger.info(f"  └── {proc.name} (PID {proc.pid}): {proc.cpu_percent:.1f}% CPU, {proc.memory_percent:.1f}% memory")
    
    def get_summary(self) -> Dict:
        """Get system summary for dashboard"""
        metrics = self.get_system_metrics()
        
        # Identify why the system might be under load
        load_explanation = []
        intensive_processes = [p for p in metrics.top_processes if p.cpu_percent > 15 or p.memory_percent > 10]
        
        # Categorize processes
        process_categories = {
            'backup': [],
            'development': [],
            'database': [],
            'gaming': [],
            'ml': [],
            'video': [],
            'mining': [],
            'system': [],
            'unknown': []
        }
        
        for proc in intensive_processes:
            category = proc.process_type or 'unknown'
            process_categories[category].append(proc)
        
        # Build explanation
        for category, procs in process_categories.items():
            if procs:
                count = len(procs)
                if category == 'backup':
                    load_explanation.append(f"{count} backup process(es)")
                elif category == 'development':
                    load_explanation.append(f"{count} development/build process(es)")
                elif category == 'database':
                    load_explanation.append(f"{count} database process(es)")
                elif category == 'gaming':
                    load_explanation.append(f"{count} game(s)")
                elif category == 'ml':
                    load_explanation.append(f"{count} ML training process(es)")
                elif category == 'video':
                    load_explanation.append(f"{count} video processing process(es)")
                elif category == 'mining':
                    load_explanation.append(f"⚠️ {count} suspected miner(s)")
                elif category == 'unknown' and count > 2:
                    load_explanation.append(f"{count} other high-usage process(es)")
        
        explanation = "System load normal"
        if load_explanation:
            explanation = f"System load high due to: {', '.join(load_explanation)}"
        
        return {
            "monitoring_available": True,
            "explanation": explanation,
            "cpu": {
                "usage_percent": metrics.cpu.usage_percent,
                "temperature": metrics.cpu.temperature_celsius,
                "core_count": metrics.cpu.core_count
            },
            "memory": {
                "used_percent": metrics.memory.used_percent,
                "used_mb": metrics.memory.used_mb,
                "total_mb": metrics.memory.total_mb
            },
            "disk": {
                "total_disks": len(metrics.disks),
                "max_usage_percent": max([d.used_percent for d in metrics.disks], default=0)
            },
            "network": {
                "active_interfaces": len([i for i in metrics.network.interfaces.values() if i.is_up]),
                "active_connections": metrics.network.active_connections
            },
            "processes": {
                "total_monitored": len(metrics.top_processes),
                "intensive_count": len(intensive_processes)
            },
            "platform": metrics.platform_info['system']
        }


# Global system monitor instance
system_monitor = SystemMonitor()