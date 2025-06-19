#!/usr/bin/env python3
"""
🐎 Hoof Hearted - Process Identification Test Script
Test the ProcessClassifier with various process examples
"""

import sys
import os
sys.path.append('/Users/davidkim/SpicyRiceCakes/projects/1018-hoof-hearted/src/backend')

from monitoring.gpu_monitor import ProcessClassifier

def test_process_classification():
    """Test the ProcessClassifier with various process examples"""
    
    test_cases = [
        # Crypto miners
        ("xmrig", "xmrig --config=config.json", "/usr/bin/xmrig"),
        ("T-Rex", "t-rex.exe -a ethash -o stratum+tcp://pool.com", "C:/mining/t-rex.exe"),
        ("miner", "claymore_miner.exe -epool pool.com", ""),
        
        # ML/AI Training
        ("python", "python train_model.py --gpu --epochs 100", "/usr/bin/python"),
        ("jupyter-lab", "jupyter-lab --ip=0.0.0.0", "/opt/conda/bin/jupyter-lab"),
        ("python", "python -m torch.distributed.launch train.py", "/usr/bin/python"),
        
        # Video Processing
        ("ffmpeg", "ffmpeg -i input.mp4 -c:v h264_nvenc output.mp4", "/usr/bin/ffmpeg"),
        ("HandBrakeCLI", "HandBrakeCLI -i movie.mkv -o movie.mp4", "/usr/bin/HandBrakeCLI"),
        ("blender", "blender --background scene.blend --render-anim", "/usr/bin/blender"),
        
        # Games
        ("valheim.exe", "valheim.exe -windowed", "C:/Steam/steamapps/common/Valheim/valheim.exe"),
        ("minecraft", "java -Xmx8G -jar minecraft.jar", "/usr/bin/java"),
        ("steam", "steam.exe", "C:/Program Files/Steam/steam.exe"),
        
        # Unknown processes
        ("chrome", "chrome --gpu-sandbox", "/usr/bin/chrome"),
        ("unknown_proc", "some_process arg1 arg2", "/usr/bin/unknown"),
    ]
    
    print("🎯 Testing Process Classification System")
    print("=" * 60)
    
    for process_name, command_line, executable_path in test_cases:
        classification = ProcessClassifier.classify_process(
            process_name, command_line, executable_path
        )
        
        print(f"\n📋 Process: {process_name}")
        print(f"   Command: {command_line}")
        print(f"   Type: {classification['process_type']}")
        print(f"   Confidence: {classification['confidence']:.1f}")
        print(f"   Reason: {classification['reason']}")
        
        # Show flags
        flags = []
        if classification['is_suspected_miner']:
            flags.append("🚨 MINER")
        if classification['is_ml_training']:
            flags.append("🧠 ML")
        if classification['is_video_processing']:
            flags.append("🎥 VIDEO")
        if classification['is_game']:
            flags.append("🎮 GAME")
        
        if flags:
            print(f"   Flags: {' '.join(flags)}")

def test_api_simulation():
    """Simulate what the API response would look like"""
    print("\n\n🔥 API Response Simulation")
    print("=" * 60)
    
    # Simulate a system with various GPU processes
    simulated_response = {
        "summary": "GPU fan running because of: 1 game(s), 1 ML training process(es), ⚠️ 1 suspected miner(s)",
        "processes": [
            {
                "pid": 1234,
                "name": "valheim.exe",
                "process_type": "gaming",
                "gpu_memory_mb": 2048,
                "is_game": True,
                "command_line": "valheim.exe -windowed"
            },
            {
                "pid": 5678,
                "name": "python", 
                "process_type": "ml",
                "gpu_memory_mb": 4096,
                "is_ml_training": True,
                "command_line": "python train_model.py --gpu"
            },
            {
                "pid": 9999,
                "name": "xmrig",
                "process_type": "mining", 
                "gpu_memory_mb": 1024,
                "is_suspected_miner": True,
                "command_line": "xmrig --config=config.json"
            }
        ],
        "insights": {
            "total_processes": 3,
            "games": 1,
            "ml_training": 1,
            "suspected_miners": 1,
            "warnings": [
                "⚠️ Suspected cryptocurrency miner detected: xmrig (PID 9999)",
                "💾 High GPU memory usage: python using 4096MB",
                "💾 High GPU memory usage: valheim.exe using 2048MB"
            ]
        }
    }
    
    print("Summary:", simulated_response["summary"])
    print(f"\nDetected {len(simulated_response['processes'])} GPU processes:")
    
    for proc in simulated_response["processes"]:
        print(f"  • {proc['name']} (PID {proc['pid']}) - {proc['process_type']}")
        print(f"    GPU Memory: {proc['gpu_memory_mb']}MB")
        print(f"    Command: {proc['command_line']}")
        print()
    
    print("Warnings:")
    for warning in simulated_response["insights"]["warnings"]:
        print(f"  {warning}")

if __name__ == "__main__":
    test_process_classification()
    test_api_simulation()
    
    print("\n\n✅ Process Identification System Ready!")
    print("🎯 This system can now answer 'Why is my GPU fan running?' by:")
    print("   • Identifying cryptocurrency miners")
    print("   • Detecting ML/AI training processes") 
    print("   • Recognizing video processing applications")
    print("   • Classifying gaming applications")
    print("   • Providing detailed process attribution")