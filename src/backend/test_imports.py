#!/usr/bin/env python3
"""Quick test to check what's causing the backend hang"""

print("Testing imports...")

try:
    print("1. Basic imports...")
    import os
    import sys
    print("✅ OS imports OK")
    
    from flask import Flask, jsonify
    print("✅ Flask imports OK")
    
    from flask_socketio import SocketIO
    print("✅ SocketIO imports OK")
    
    from flask_cors import CORS
    print("✅ CORS imports OK")
    
    print("2. Testing GPU monitoring imports...")
    from monitoring import GPUMonitoringService
    print("✅ GPU monitoring imports OK")
    
    print("3. Creating GPU service...")
    gpu_service = GPUMonitoringService(update_interval=2.0)
    print("✅ GPU service created OK")
    
    print("4. Testing GPU service methods...")
    summary = gpu_service.get_summary()
    print(f"✅ GPU summary: {summary}")
    
    print("5. All tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()