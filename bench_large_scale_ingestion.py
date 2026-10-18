#!/usr/bin/env python3
# =====================================================================
# BRANCH: bench/multi-generational-stress
# MODULE: Gigabyte-Scale Memory Ingestion Sandbox
# =====================================================================

import os
import sys
import time
import numpy as np
from core_engine.memory_ingestion import InfiniteMemoryBuffer
from core_engine.latency_tracker import DynamicLatencyTracker

def execute_gigabyte_scale_test():
    print("======================================================================")
    print("     RUNNING BENCHMARK: GIGABYTE-SCALE MEMORY STREAM INGESTION        ")
    print("======================================================================")
    
    buffer = InfiniteMemoryBuffer()
    tracker = DynamicLatencyTracker()
    
    # 1. Simulate large-scale raw data chunks (50 Megabytes per batch block)
    chunk_elements = 6250000  # 6.25M float64 elements ≈ 50 megabytes
    total_batches = 20        # 20 iterations ≈ 1.0 Gigabyte of raw payload injection
    
    print(f"[SYSTEM] Allocating data arrays... Target payload: ~1.0 GB across {total_batches} blocks.")
    
    start_bench_time = time.perf_counter()
    
    for i in range(1, total_batches + 1):
        tick_start = time.perf_counter()
        
        # Generating a massive raw chunk representing unconstrained environmental sensory influx
        massive_chunk = np.random.randn(chunk_elements)
        
        # Branch Feature 2: Ingest the raw memory stream directly
        buffer.swallow_stream(massive_chunk)
        
        # Calculate localized friction scalar to feed into the latency multiplier
        simulated_friction = 4.5 + (i * 0.4) 
        tick_latency_ms = tracker.track_execution(tick_start, simulated_friction)
        
        metrics = buffer.get_allocation_metrics()
        current_mb = metrics["total_memory_mass_bytes"] / (1024 * 1024)
        
        print(f" -> [BLOCK {i:02d}/{total_batches}] Ingested. Cumulative Size: {current_mb:.2f} MB | Loop Delay: {tick_latency_ms:.2f}ms")
        
        # Memory Safeguard Checkpoint
        if current_mb > 1200:
            print("[WARNING] High-water storage threshold crossed. Throttling active input buffers.")
            break

    total_duration = time.perf_counter() - start_bench_time
    final_metrics = buffer.get_allocation_metrics()
    final_gb = final_metrics["total_memory_mass_bytes"] / (1024 * 1024 * 1024)
    
    print("\n----------------------------------------------------------------------")
    print("INGESTION BENCHMARK SUMMARY COMPLETE:")
    print(f" - Unconstrained memory mass swallowed: {final_gb:.3f} GB")
    print(f" - Cumulative processing overhead:      {total_duration:.2f} seconds")
    print(f" - Sustained operational throughput:     {(final_gb * 1024) / total_duration:.2f} MB/s")
    print("----------------------------------------------------------------------")

if __name__ == "__main__":
    # Ensure dependencies are locally generated via setup.sh before execution
    try:
        execute_gigabyte_scale_test()
    except ImportError:
        print("[ERR] Core engine modules missing. Please run 'setup.sh' to establish branch packages first.")
