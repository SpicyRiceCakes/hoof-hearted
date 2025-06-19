#!/usr/bin/env python3
"""
🐎 Hoof Hearted - GPU Monitoring System
SpicyRiceCakes - Multi-vendor GPU monitoring with process attribution

Answers "Why is my GPU fan running?" by identifying GPU usage and processes.
"""

import logging
import time
import re
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Optional, Union
from enum import Enum

logger = logging.getLogger(__name__)


class GPUVendor(Enum):
    """GPU vendor enumeration"""
    NVIDIA = "nvidia"
    AMD = "amd"
    INTEL = "intel"
    UNKNOWN = "unknown"


@dataclass
class GPUProcess:
    """Process using GPU resources - answers 'Why is my GPU fan running?'"""
    pid: int
    name: str
    gpu_memory_mb: int
    gpu_utilization: float
    command_line: Optional[str] = None
    
    # Enhanced process identification
    username: Optional[str] = None
    process_type: Optional[str] = None  # 'gaming', 'ml', 'mining', 'video', 'unknown'
    cpu_percent: Optional[float] = None
    memory_mb: Optional[int] = None
    runtime_seconds: Optional[float] = None
    executable_path: Optional[str] = None
    
    # Process classification
    is_suspected_miner: bool = False
    is_ml_training: bool = False
    is_video_processing: bool = False
    is_game: bool = False


@dataclass
class GPUMetrics:
    """Unified GPU metrics across all vendors"""
    gpu_id: int
    name: str
    vendor: GPUVendor
    
    # Usage metrics
    utilization_percent: float
    memory_used_mb: int
    memory_total_mb: int
    memory_percent: float
    
    # Thermal metrics
    temperature_c: Optional[int] = None
    fan_speed_percent: Optional[int] = None
    
    # Power metrics
    power_draw_watts: Optional[float] = None
    power_limit_watts: Optional[float] = None
    
    # Process attribution
    processes: List[GPUProcess] = None
    
    # Status
    driver_version: Optional[str] = None
    is_available: bool = True
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()
        if self.processes is None:
            self.processes = []


class ProcessClassifier:
    """Intelligent process classification to answer 'Why is my GPU fan running?'"""
    
    # Known process patterns for classification
    MINERS = [
        r'.*miner.*', r'.*mining.*', r'.*xmrig.*', r'.*claymore.*', 
        r'.*phoenix.*', r'.*nicehash.*', r'.*t-rex.*', r'.*gminer.*',
        r'.*bminer.*', r'.*lolminer.*', r'.*nanominer.*'
    ]
    
    ML_TRAINING = [
        r'python.*tensorflow.*', r'python.*pytorch.*', r'python.*train.*',
        r'python.*model.*', r'jupyter.*', r'.*cuda.*ml.*', r'python.*gpu.*',
        r'python.*deep.*', r'python.*neural.*', r'python.*keras.*'
    ]
    
    VIDEO_PROCESSING = [
        r'.*ffmpeg.*', r'.*handbrake.*', r'.*davinci.*', r'.*premiere.*',
        r'.*after.*effects.*', r'.*blender.*', r'.*obs.*', r'.*nvenc.*',
        r'.*video.*encode.*', r'.*transcode.*'
    ]
    
    GAMES = [
        r'.*\.exe$', r'.*steam.*', r'.*game.*', r'.*unity.*', r'.*unreal.*',
        r'.*wow.*', r'.*minecraft.*', r'.*valorant.*', r'.*league.*'
    ]
    
    @staticmethod
    def classify_process(process_name: str, command_line: str = "", executable_path: str = "") -> Dict[str, any]:
        """Classify a process to determine why it's using GPU"""
        classification = {
            'process_type': 'unknown',
            'is_suspected_miner': False,
            'is_ml_training': False,
            'is_video_processing': False,
            'is_game': False,
            'confidence': 0.0,
            'reason': 'Unknown process type'
        }
        
        # Combine all available text for analysis
        text_to_analyze = f"{process_name} {command_line} {executable_path}".lower()
        
        # Check for miners (highest priority due to security concerns)
        for pattern in ProcessClassifier.MINERS:
            if re.search(pattern, text_to_analyze, re.IGNORECASE):
                classification.update({
                    'process_type': 'mining',
                    'is_suspected_miner': True,
                    'confidence': 0.9,
                    'reason': f'Suspected cryptocurrency miner (pattern: {pattern})'
                })
                return classification
        
        # Check for ML/AI training
        for pattern in ProcessClassifier.ML_TRAINING:
            if re.search(pattern, text_to_analyze, re.IGNORECASE):
                classification.update({
                    'process_type': 'ml',
                    'is_ml_training': True,
                    'confidence': 0.8,
                    'reason': 'Machine learning or AI training process'
                })
                return classification
        
        # Check for video processing
        for pattern in ProcessClassifier.VIDEO_PROCESSING:
            if re.search(pattern, text_to_analyze, re.IGNORECASE):
                classification.update({
                    'process_type': 'video',
                    'is_video_processing': True,
                    'confidence': 0.8,
                    'reason': 'Video encoding or processing application'
                })
                return classification
        
        # Check for games
        for pattern in ProcessClassifier.GAMES:
            if re.search(pattern, text_to_analyze, re.IGNORECASE):
                classification.update({
                    'process_type': 'gaming',
                    'is_game': True,
                    'confidence': 0.7,
                    'reason': 'Gaming application'
                })
                return classification
        
        # High GPU memory usage without clear classification
        classification['reason'] = 'Unknown GPU-using process'
        return classification


class GPUMonitor(ABC):
    """Abstract base class for GPU monitoring implementations"""
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if this GPU monitoring backend is available"""
        pass
    
    @abstractmethod
    def get_gpu_count(self) -> int:
        """Get number of available GPUs"""
        pass
    
    @abstractmethod
    def get_gpu_metrics(self, gpu_id: int = None) -> Union[GPUMetrics, List[GPUMetrics]]:
        """Get metrics for specific GPU or all GPUs"""
        pass
    
    @abstractmethod
    def get_driver_version(self) -> Optional[str]:
        """Get GPU driver version"""
        pass


class NVIDIAMonitor(GPUMonitor):
    """NVIDIA GPU monitoring using nvidia-ml-py"""
    
    def __init__(self):
        self._nvml_initialized = False
        self._initialize_nvml()
    
    def _initialize_nvml(self):
        """Initialize NVIDIA Management Library"""
        try:
            import pynvml
            pynvml.nvmlInit()
            self._nvml_initialized = True
            self._pynvml = pynvml
            logger.info("🔥 NVIDIA GPU monitoring initialized successfully")
        except ImportError:
            logger.warning("nvidia-ml-py not installed - NVIDIA monitoring unavailable")
        except Exception as e:
            logger.error(f"Failed to initialize NVIDIA monitoring: {e}")
    
    def is_available(self) -> bool:
        return self._nvml_initialized
    
    def get_gpu_count(self) -> int:
        if not self.is_available():
            return 0
        try:
            return self._pynvml.nvmlDeviceGetCount()
        except Exception as e:
            logger.error(f"Failed to get NVIDIA GPU count: {e}")
            return 0
    
    def get_driver_version(self) -> Optional[str]:
        if not self.is_available():
            return None
        try:
            return self._pynvml.nvmlSystemGetDriverVersion().decode('utf-8')
        except Exception as e:
            logger.error(f"Failed to get NVIDIA driver version: {e}")
            return None
    
    def get_gpu_metrics(self, gpu_id: int = None) -> Union[GPUMetrics, List[GPUMetrics]]:
        """Get NVIDIA GPU metrics with full process attribution"""
        if not self.is_available():
            return []
        
        try:
            gpu_count = self.get_gpu_count()
            if gpu_count == 0:
                return []
            
            if gpu_id is not None:
                return self._get_single_gpu_metrics(gpu_id)
            else:
                return [self._get_single_gpu_metrics(i) for i in range(gpu_count)]
        
        except Exception as e:
            logger.error(f"Failed to get NVIDIA GPU metrics: {e}")
            return []
    
    def _get_single_gpu_metrics(self, gpu_id: int) -> GPUMetrics:
        """Get metrics for a single NVIDIA GPU"""
        handle = self._pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
        
        # Basic GPU info
        name = self._pynvml.nvmlDeviceGetName(handle).decode('utf-8')
        
        # Memory info
        memory_info = self._pynvml.nvmlDeviceGetMemoryInfo(handle)
        memory_used_mb = memory_info.used // (1024 * 1024)
        memory_total_mb = memory_info.total // (1024 * 1024)
        memory_percent = (memory_info.used / memory_info.total) * 100
        
        # Utilization
        utilization = self._pynvml.nvmlDeviceGetUtilizationRates(handle)
        utilization_percent = utilization.gpu
        
        # Temperature
        try:
            temperature_c = self._pynvml.nvmlDeviceGetTemperature(handle, self._pynvml.NVML_TEMPERATURE_GPU)
        except:
            temperature_c = None
        
        # Fan speed
        try:
            fan_speed_percent = self._pynvml.nvmlDeviceGetFanSpeed(handle)
        except:
            fan_speed_percent = None
        
        # Power
        try:
            power_draw_watts = self._pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0  # mW to W
        except:
            power_draw_watts = None
        
        try:
            power_limit_watts = self._pynvml.nvmlDeviceGetPowerManagementLimitConstraints(handle)[1] / 1000.0
        except:
            power_limit_watts = None
        
        # Process attribution - THE KEY FEATURE!
        processes = self._get_gpu_processes(handle)
        
        return GPUMetrics(
            gpu_id=gpu_id,
            name=name,
            vendor=GPUVendor.NVIDIA,
            utilization_percent=utilization_percent,
            memory_used_mb=memory_used_mb,
            memory_total_mb=memory_total_mb,
            memory_percent=memory_percent,
            temperature_c=temperature_c,
            fan_speed_percent=fan_speed_percent,
            power_draw_watts=power_draw_watts,
            power_limit_watts=power_limit_watts,
            processes=processes,
            driver_version=self.get_driver_version()
        )
    
    def _get_gpu_processes(self, handle) -> List[GPUProcess]:
        """Get processes using this GPU - answers 'Why is my GPU fan running?'"""
        try:
            processes = []
            # Get GPU processes using NVIDIA-ML
            gpu_processes = self._pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
            
            for proc in gpu_processes:
                try:
                    # Get process info using psutil for additional details
                    import psutil
                    ps_proc = psutil.Process(proc.pid)
                    
                    # Gather comprehensive process information
                    process_name = ps_proc.name()
                    command_line = ' '.join(ps_proc.cmdline()) if ps_proc.cmdline() else ""
                    executable_path = ps_proc.exe() if hasattr(ps_proc, 'exe') else ""
                    username = ps_proc.username() if hasattr(ps_proc, 'username') else None
                    
                    # Get system resource usage
                    cpu_percent = ps_proc.cpu_percent()
                    memory_info = ps_proc.memory_info()
                    memory_mb = memory_info.rss // (1024 * 1024)  # RSS in MB
                    runtime_seconds = time.time() - ps_proc.create_time()
                    
                    # Classify the process to understand why it's using GPU
                    classification = ProcessClassifier.classify_process(
                        process_name, command_line, executable_path
                    )
                    
                    # Create enhanced GPU process object
                    gpu_proc = GPUProcess(
                        pid=proc.pid,
                        name=process_name,
                        gpu_memory_mb=proc.usedGpuMemory // (1024 * 1024),  # Bytes to MB
                        gpu_utilization=0.0,  # NVIDIA-ML doesn't provide per-process utilization
                        command_line=command_line,
                        
                        # Enhanced process identification
                        username=username,
                        process_type=classification['process_type'],
                        cpu_percent=cpu_percent,
                        memory_mb=memory_mb,
                        runtime_seconds=runtime_seconds,
                        executable_path=executable_path,
                        
                        # Process classification flags
                        is_suspected_miner=classification['is_suspected_miner'],
                        is_ml_training=classification['is_ml_training'],
                        is_video_processing=classification['is_video_processing'],
                        is_game=classification['is_game']
                    )
                    
                    processes.append(gpu_proc)
                    
                    # Log interesting processes for debugging
                    if classification['confidence'] > 0.5:
                        logger.info(
                            f"🎯 Identified GPU process: {process_name} (PID {proc.pid}) - "
                            f"{classification['reason']} "
                            f"[{proc.usedGpuMemory // (1024 * 1024)}MB GPU memory]"
                        )
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    # Process might have ended or be inaccessible
                    logger.warning(f"Could not access process {proc.pid}: {e}")
                    processes.append(GPUProcess(
                        pid=proc.pid,
                        name="<unknown>",
                        gpu_memory_mb=proc.usedGpuMemory // (1024 * 1024),
                        gpu_utilization=0.0,
                        process_type="unknown"
                    ))
                except Exception as e:
                    logger.error(f"Error processing GPU process {proc.pid}: {e}")
            
            return processes
        except Exception as e:
            logger.error(f"Failed to get GPU processes: {e}")
            return []


class AMDMonitor(GPUMonitor):
    """AMD GPU monitoring using amdsmi (future implementation)"""
    
    def __init__(self):
        # TODO: Implement AMD monitoring with amdsmi
        logger.info("AMD GPU monitoring not yet implemented")
    
    def is_available(self) -> bool:
        return False
    
    def get_gpu_count(self) -> int:
        return 0
    
    def get_gpu_metrics(self, gpu_id: int = None) -> Union[GPUMetrics, List[GPUMetrics]]:
        return []
    
    def get_driver_version(self) -> Optional[str]:
        return None


class BasicMonitor(GPUMonitor):
    """Basic GPU monitoring using system calls (fallback)"""
    
    def __init__(self):
        logger.info("Using basic GPU monitoring (limited functionality)")
    
    def is_available(self) -> bool:
        return True
    
    def get_gpu_count(self) -> int:
        # Try to detect GPUs using basic methods
        try:
            import GPUtil
            return len(GPUtil.getGPUs())
        except:
            return 0
    
    def get_gpu_metrics(self, gpu_id: int = None) -> Union[GPUMetrics, List[GPUMetrics]]:
        """Basic GPU metrics using GPUtil (NVIDIA only)"""
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            
            if not gpus:
                return []
            
            if gpu_id is not None:
                if gpu_id < len(gpus):
                    return self._gpu_to_metrics(gpus[gpu_id], gpu_id)
                return None
            
            return [self._gpu_to_metrics(gpu, i) for i, gpu in enumerate(gpus)]
        
        except Exception as e:
            logger.error(f"Failed to get basic GPU metrics: {e}")
            return []
    
    def _gpu_to_metrics(self, gpu, gpu_id: int) -> GPUMetrics:
        """Convert GPUtil GPU to our metrics format"""
        return GPUMetrics(
            gpu_id=gpu_id,
            name=gpu.name,
            vendor=GPUVendor.NVIDIA,  # GPUtil only supports NVIDIA
            utilization_percent=gpu.load * 100,
            memory_used_mb=gpu.memoryUsed,
            memory_total_mb=gpu.memoryTotal,
            memory_percent=(gpu.memoryUsed / gpu.memoryTotal) * 100,
            temperature_c=int(gpu.temperature) if gpu.temperature else None,
            driver_version=gpu.driver,
            processes=[]  # No process attribution in basic mode
        )
    
    def get_driver_version(self) -> Optional[str]:
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            return gpus[0].driver if gpus else None
        except:
            return None


class GPUMonitorFactory:
    """Factory for creating appropriate GPU monitor based on available hardware"""
    
    @staticmethod
    def create_monitor() -> GPUMonitor:
        """Create the best available GPU monitor"""
        
        # Try NVIDIA first (most comprehensive)
        nvidia_monitor = NVIDIAMonitor()
        if nvidia_monitor.is_available():
            logger.info("🔥 Using NVIDIA GPU monitoring with full process attribution")
            return nvidia_monitor
        
        # Try AMD next
        amd_monitor = AMDMonitor()
        if amd_monitor.is_available():
            logger.info("🔴 Using AMD GPU monitoring")
            return amd_monitor
        
        # Fallback to basic monitoring
        logger.warning("⚠️ Using basic GPU monitoring - limited functionality")
        return BasicMonitor()


class GPUMonitoringService:
    """Main service for GPU monitoring with caching and error handling"""
    
    def __init__(self, update_interval: float = 2.0):
        self.monitor = GPUMonitorFactory.create_monitor()
        self.update_interval = update_interval
        self._last_update = 0
        self._cached_metrics = []
        self._is_monitoring = False
    
    def get_gpu_metrics(self, force_update: bool = False) -> List[GPUMetrics]:
        """Get GPU metrics with caching"""
        current_time = time.time()
        
        if force_update or (current_time - self._last_update) >= self.update_interval:
            try:
                metrics = self.monitor.get_gpu_metrics()
                if isinstance(metrics, GPUMetrics):
                    metrics = [metrics]
                
                self._cached_metrics = metrics
                self._last_update = current_time
                
                # Log interesting findings for debugging
                self._log_gpu_status(metrics)
                
            except Exception as e:
                logger.error(f"Failed to update GPU metrics: {e}")
        
        return self._cached_metrics
    
    def _log_gpu_status(self, metrics: List[GPUMetrics]):
        """Log GPU status for debugging 'Why is my GPU fan running?'"""
        for gpu in metrics:
            if gpu.utilization_percent > 50 or len(gpu.processes) > 0:
                process_summary = f"{len(gpu.processes)} processes" if gpu.processes else "no processes"
                logger.info(
                    f"🔥 GPU {gpu.gpu_id} ({gpu.name}): "
                    f"{gpu.utilization_percent:.1f}% usage, "
                    f"{gpu.memory_percent:.1f}% memory, "
                    f"{gpu.temperature_c}°C, "
                    f"{process_summary}"
                )
                
                # Log individual processes
                for proc in gpu.processes:
                    if proc.gpu_memory_mb > 100:  # Only log processes using significant memory
                        logger.info(
                            f"  └── PID {proc.pid} ({proc.name}): "
                            f"{proc.gpu_memory_mb}MB GPU memory"
                        )
    
    def get_gpu_count(self) -> int:
        """Get number of available GPUs"""
        return self.monitor.get_gpu_count()
    
    def is_available(self) -> bool:
        """Check if GPU monitoring is available"""
        return self.monitor.is_available()
    
    def get_summary(self) -> Dict:
        """Get summary information for dashboard"""
        metrics = self.get_gpu_metrics()
        
        if not metrics:
            return {
                "gpu_count": 0,
                "monitoring_available": False,
                "message": "No GPUs detected or monitoring unavailable"
            }
        
        total_processes = sum(len(gpu.processes) for gpu in metrics)
        max_utilization = max(gpu.utilization_percent for gpu in metrics)
        max_temperature = max(gpu.temperature_c for gpu in metrics if gpu.temperature_c)
        
        return {
            "gpu_count": len(metrics),
            "monitoring_available": True,
            "total_processes": total_processes,
            "max_utilization": max_utilization,
            "max_temperature": max_temperature,
            "gpus": [
                {
                    "id": gpu.gpu_id,
                    "name": gpu.name,
                    "vendor": gpu.vendor.value,
                    "utilization": gpu.utilization_percent,
                    "memory_percent": gpu.memory_percent,
                    "temperature": gpu.temperature_c,
                    "process_count": len(gpu.processes)
                }
                for gpu in metrics
            ]
        }