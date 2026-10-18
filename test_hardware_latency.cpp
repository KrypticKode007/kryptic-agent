/**
 * @file test_hardware_latency.cpp
 * @brief High-precision performance harness validating sub-millisecond execution 
 *        overhead of the core homeostatic tracking loops using system microsecond clocks.
 */

#include <iostream>
#include <chrono>
#include <cassert>
#include "kryptic_hardware_node.hpp"

int main() {
    std::cout << "======================================================================" << std::endl;
    std::cout << "⚡ RUNNING BARE-METAL LATENCY BENCHMARK ON IM-FIN RUNTIME CORE" << std::endl;
    std::cout << "======================================================================" << std::endl;

    kryptic::IMFINEngine engine;

    // 1. Benchmark Nominal Telemetry Execution Processing Speed
    auto start_nominal = std::chrono::high_resolution_clock::now();
    
    // Simulate processing 1,000 sequential telemetry cycles
    for (int i = 0; i < 1000; ++i) {
        bool is_stable = engine.evaluate_telemetry_invariants(45.2f, 9.81f);
        (void)is_stable; // Prevent compiler warning for unused variable
    }
    
    auto end_nominal = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> nominal_duration = end_nominal - start_nominal;
    double average_latency_ns = (nominal_duration.count() / 1000.0) * 1000000.0;

    std::cout << "[+] Processed 1,000 Nominal Hardware Cycles Safely." << std::endl;
    std::cout << "[+] Average Loop Execution Latency: " << average_latency_ns << " nanoseconds." << std::endl;
    
    // Hard architectural validation verification check (<1ms constraint)
    assert(average_latency_ns < 1000000.0 && "Architectural error: Execution latency exceeds 1ms target!");
    std::cout << "    -> CRITICAL PERFORMANCE LIMIT CONFIRMED: Sub-millisecond Execution Loop." << std::endl;

    // 2. Test Invariant Hard Boundary Tripping Mechanism
    std::cout << "[*] Injecting boundary break anomaly packet (Critical Low Battery)..." << std::endl;
    bool system_status = engine.evaluate_telemetry_invariants(12.5f, 9.81f);
    
    if (!system_status) {
        std::cout << "✅ SUCCESS: Invariant breach trapped instantly. Failsafe mode engaged." << std::endl;
    } else {
        std::cout << "❌ FAILURE: Safety node failed to intercept critical exception layout." << std::endl;
        return 1;
    }

    std::cout << "======================================================================" << std::endl;
    std::cout << "⚡ BENCHMARK SUITE EXECUTION COMPLETED: SYSTEM COMPLIANT" << std::endl;
    std::cout << "======================================================================" << std::endl;
    return 0;
}
