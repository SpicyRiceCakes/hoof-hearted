#!/usr/bin/env python3
"""
🐎 Hoof Hearted - System Monitoring Test Script
Test the comprehensive system monitoring with process attribution
"""

import sys
import os
import json
import time
sys.path.append('/Users/davidkim/SpicyRiceCakes/projects/1018-hoof-hearted/src/backend')

from monitoring.system_monitor import system_monitor, SystemProcessClassifier

def test_system_monitoring():
    """Test the system monitoring functionality"""
    
    print("🖥️ Testing System Monitoring Capabilities")
    print("=" * 60)
    
    # Test system metrics collection
    print("\n📊 Getting system metrics...")
    try:
        metrics = system_monitor.get_system_metrics(force_update=True)
        
        print(f"✅ System metrics collected successfully")
        print(f"   Platform: {metrics.platform_info['system']} {metrics.platform_info['release']}")
        print(f"   CPU cores: {metrics.cpu.core_count} cores, {metrics.cpu.thread_count} threads")
        print(f"   Memory: {metrics.memory.total_mb}MB total")
        print(f"   Disks: {len(metrics.disks)} mounted drives")
        print(f"   Network: {len(metrics.network.interfaces)} interfaces")
        print(f"   Processes: {len(metrics.top_processes)} monitored")
        
    except Exception as e:
        print(f"❌ Failed to get system metrics: {e}")
        return False
    
    # Test CPU monitoring
    print(f"\n🔥 CPU Status:")
    print(f"   Usage: {metrics.cpu.usage_percent:.1f}%")
    print(f"   Per-core: {[f'{usage:.1f}%' for usage in metrics.cpu.per_core_usage[:4]]}...")
    if metrics.cpu.frequency_mhz:
        print(f"   Frequency: {metrics.cpu.frequency_mhz:.0f}MHz")
    if metrics.cpu.temperature_celsius:
        print(f"   Temperature: {metrics.cpu.temperature_celsius:.1f}°C")
    if metrics.cpu.load_average:
        print(f"   Load average: {metrics.cpu.load_average}")
    
    # Test memory monitoring
    print(f"\n💾 Memory Status:")
    print(f"   Used: {metrics.memory.used_percent:.1f}% ({metrics.memory.used_mb}MB / {metrics.memory.total_mb}MB)")
    print(f"   Available: {metrics.memory.available_mb}MB")
    if metrics.memory.swap_total_mb > 0:
        print(f"   Swap: {metrics.memory.swap_used_percent:.1f}% ({metrics.memory.swap_used_mb}MB / {metrics.memory.swap_total_mb}MB)")
    
    # Test disk monitoring
    print(f"\n💿 Disk Status:")
    for i, disk in enumerate(metrics.disks[:3]):  # Show first 3 disks
        print(f"   {disk.device} ({disk.mountpoint}): {disk.used_percent:.1f}% used")
        print(f"     {disk.used_mb}MB / {disk.total_mb}MB ({disk.filesystem})")
        if disk.io_read_bytes_per_sec is not None:
            read_mb = disk.io_read_bytes_per_sec / (1024 * 1024)
            write_mb = disk.io_write_bytes_per_sec / (1024 * 1024)
            print(f"     I/O: {read_mb:.2f}MB/s read, {write_mb:.2f}MB/s write")
    
    # Test network monitoring
    print(f"\n🌐 Network Status:")
    print(f"   Active connections: {metrics.network.active_connections}")
    active_interfaces = [name for name, iface in metrics.network.interfaces.items() if iface.is_up]
    print(f"   Active interfaces: {active_interfaces}")
    
    for name, interface in list(metrics.network.interfaces.items())[:2]:  # Show first 2 interfaces
        if interface.is_up:
            print(f"   {name}: {len(interface.addresses)} addresses")
            if interface.bytes_sent_per_sec is not None:
                sent_mb = interface.bytes_sent_per_sec / (1024 * 1024)
                recv_mb = interface.bytes_recv_per_sec / (1024 * 1024)
                print(f"     Traffic: {sent_mb:.3f}MB/s sent, {recv_mb:.3f}MB/s received")
    
    # Test process monitoring and classification
    print(f"\n⚡ Top Resource-Intensive Processes:")
    intensive_processes = [p for p in metrics.top_processes if p.cpu_percent > 1.0 or p.memory_percent > 1.0]
    
    for i, proc in enumerate(intensive_processes[:5]):
        print(f"   {i+1}. {proc.name} (PID {proc.pid})")
        print(f"      CPU: {proc.cpu_percent:.1f}%, Memory: {proc.memory_percent:.1f}% ({proc.memory_mb}MB)")
        print(f"      Type: {proc.process_type}, Status: {proc.status}")
        if proc.username:
            print(f"      User: {proc.username}")
        if proc.is_system_intensive:
            print(f"      🚨 System-intensive process")
        if proc.command_line and len(proc.command_line) < 80:
            print(f"      Command: {proc.command_line}")
    
    return True

def test_process_classification():
    """Test the extended process classification system"""
    
    print("\n\n🎯 Testing Process Classification System")
    print("=" * 60)
    
    test_cases = [
        # System backup processes
        ("Time Machine", "backupd", "/System/Library/CoreServices/backupd"),
        ("rsync", "rsync -av /home/user/ /backup/", "/usr/bin/rsync"),
        
        # Development processes
        ("gcc", "gcc -O2 main.c -o main", "/usr/bin/gcc"),
        ("npm", "npm run build", "/usr/local/bin/npm"),
        ("Docker Desktop", "com.docker.backend", "/Applications/Docker.app"),
        
        # Database processes
        ("postgres", "postgres: user db [local]", "/usr/local/bin/postgres"),
        ("mysqld", "mysqld --defaults-file=/etc/mysql/my.cnf", "/usr/sbin/mysqld"),
        
        # System processes
        ("kernel_task", "kernel_task", ""),
        ("WindowServer", "WindowServer -daemon", "/System/Library/Frameworks/ApplicationServices.framework"),
        ("mds", "mds", "/System/Library/Frameworks/CoreServices.framework"),
    ]
    
    for process_name, command_line, executable_path in test_cases:
        classification = SystemProcessClassifier.classify_process(
            process_name, command_line, executable_path
        )
        
        print(f"\n📋 Process: {process_name}")
        print(f"   Command: {command_line}")
        print(f"   Type: {classification['process_type']}")
        print(f"   Confidence: {classification['confidence']:.1f}")
        print(f"   Reason: {classification['reason']}")
        if classification.get('is_system_intensive'):
            print(f"   🚨 System-intensive: Yes")

def test_system_summary():
    """Test the system summary functionality"""
    
    print("\n\n📋 Testing System Summary")
    print("=" * 60)
    
    try:
        summary = system_monitor.get_summary()
        
        print("System Summary:")
        print(json.dumps(summary, indent=2))
        
        print(f"\n🎯 System Load Explanation:")
        print(f"   {summary['explanation']}")
        
        print(f"\n📊 Quick Stats:")
        print(f"   CPU: {summary['cpu']['usage_percent']:.1f}%")
        print(f"   Memory: {summary['memory']['used_percent']:.1f}%")
        print(f"   Platform: {summary['platform']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to get system summary: {e}")
        return False

def test_api_simulation():
    """Simulate what the API responses would look like"""
    
    print("\n\n🔥 API Response Simulation")
    print("=" * 60)
    
    try:
        # Simulate /api/system/overview
        overview = system_monitor.get_summary()
        print("GET /api/system/overview:")
        print(f"Status: 200 OK")
        print(f"Response: {json.dumps(overview, indent=2)[:300]}...")
        
        # Simulate /api/system/cpu
        metrics = system_monitor.get_system_metrics()
        cpu_data = {
            'cpu': {
                'usage_percent': metrics.cpu.usage_percent,
                'per_core_usage': metrics.cpu.per_core_usage,
                'core_count': metrics.cpu.core_count,
                'temperature_celsius': metrics.cpu.temperature_celsius
            },
            'top_processes': len([p for p in metrics.top_processes if p.cpu_percent > 1.0])
        }
        print(f"\nGET /api/system/cpu:")
        print(f"Status: 200 OK")
        print(f"Response: {json.dumps(cpu_data, indent=2)}")
        
        print(f"\n✅ All API endpoints would return valid data!")
        return True
        
    except Exception as e:
        print(f"❌ API simulation failed: {e}")
        return False

if __name__ == "__main__":
    print("🐎 Hoof Hearted - System Monitoring Test Suite")
    print("🌶️ SpicyRiceCakes - Testing comprehensive system monitoring")
    print()
    
    # Run all tests
    tests = [
        ("System Monitoring", test_system_monitoring),
        ("Process Classification", test_process_classification),
        ("System Summary", test_system_summary),
        ("API Simulation", test_api_simulation)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("🧪 Test Results Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System monitoring is ready!")
        print("🎯 The system can now answer 'Why is my server fan running?' by:")
        print("   • Monitoring CPU, memory, disk, and network usage")
        print("   • Identifying resource-intensive processes")
        print("   • Classifying processes (backup, development, database, etc.)")
        print("   • Providing clear explanations for high system load")
        print("   • Offering detailed metrics through API endpoints")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please check the implementation.")