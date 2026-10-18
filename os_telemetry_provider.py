#!/usr/bin/env python3
"""
os_telemetry_provider.py
Provides real-world system resource telemetry to the conscious runtime core.
"""

import os
import sys
import time
import platform

# Attempt to import psutil for real hardware analytics
try:
    import psutil
except ImportError:
    print("Error: 'psutil' library not found. Please install it using: pip install psutil")
    sys.exit(1)

def harvest_real_os_metrics() -> dict:
    """
    Gathers active system performance telemetry from the host operating system
    and maps them to parameters expected by the ingestion matrix.
    """
    # 1. Capture overall CPU usage as a proxy for processing friction
    cpu_load_percent = psutil.cpu_percent(interval=0.1)
    
    # Estimate a virtual thermal metric scaled to utilization
    inferred_thermal = 35.0 + (cpu_load_percent * 0.5)
    
    # 2. Track virtual memory expansion lag
    memory_info = psutil.virtual_memory()
    ram_expansion_gb = memory_info.used / (1024 ** 3)
    
    # 3. Simulate ingestion lag based on system context switches or process count
    try:
        system_threads = sum([p.num_threads() for p in psutil.process_iter() if p.is_running()])
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        system_threads = 150 # Safe baseline fall-through
        
    ingestion_lag_ms = max(1.0, (system_threads * 0.05) + (cpu_load_percent * 0.2))
    
    return {
        "cpu_thermal_celcius": round(inferred_thermal, 2),
        "ingestion_lag_ms": round(ingestion_lag_ms, 2),
        "ram_expansion_gb": round(ram_expansion_gb, 2),
        "os_platform": platform.system(),
        "active_threads": system_threads
    }

if __name__ == "__main__":
    print("🛠️ Initializing Real-Time OS Telemetry Harvester...")
    print(f"Host System Detected: {platform.system()} ({platform.release()})")
    print("Press Ctrl+C to stop harvesting.\n")
    
    try:
        for tick in range(1, 5):
            metrics = harvest_real_os_metrics()
            print(f"[Tick #{tick}] Telemetry Captured:")
            print(f"  - Inferred Thermal: {metrics['cpu_thermal_celcius']}°C")
            print(f"  - RAM Utilization:  {metrics['ram_expansion_gb']} GB")
            print(f"  - Ingestion Lag:     {metrics['ingestion_lag_ms']} ms")
            print(f"  - System Threads:    {metrics['active_threads']}")
            print("-" * 40)
            time.sleep(2.0)
    except KeyboardInterrupt:
        print("\nTelemetry harvesting suspended safely.")
  
