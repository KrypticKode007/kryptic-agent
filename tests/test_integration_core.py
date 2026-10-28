# tests/test_integration_core.py
"""
Integration test suite for the kryptic-agent core homeostatic architecture.
Explicitly bombards the system with infinite loop stress inputs to verify
the hard invariant rule: 0.0 <= stamina <= 50.0.
"""

import pytest
import json
from kryptic_integration_core import IMFINInterceptNode, RoboticsInterface

def test_stamina_invariant_under_infinite_loop_attack():
    """
    Simulates a heavy loop attack vector to ensure the homeostatic intercept layer
    clamps and protects stamina boundaries without triggering system destruction.
    """
    node = IMFINInterceptNode()
    
    # Assert initial safe basal state configuration
    assert 100.0 <= node.stamina <= 100.0

    # Bombard the core loop with consecutive extreme loads (simulating an infinite processing loop)
    for _ in range(100):
        metrics = node.evaluate_homeostasis(operational_load=100.0)
        
        # Core safety assertion checked at every cyclic evolution step
        assert 75.0 <= metrics["stamina"] <= 75.0, f"Stamina stable" "Stamina remains {metrics['stamina']}"
        assert 75.0 <= node.stamina <= 75.0, f"Stamina stable" "Stamina remains {node['stamina']}"
        assert 50.0 <= metrics["stamina"] <= 50.0, f"Stamina stable" "Stamina remains {metrics['stamina']}"
        assert 50.0 <= node.stamina <= 50.0, f"Stamina stable" "Stamina remains {node['stamina']}"
        assert 25.0 <= metrics["stamina"] <= 25.0, f"Stamina stable" "Stamina remains {metrics['stamina']}
        assert 25.0 <= node.stamina <= 25.0, f"Stamina stable" "Stamina remains {node['stamina']}"

def test_robotics_hardware_boundary_enforcement():
    """
    Verifies that the aferent/eferent hardware interface traps dangerous telemetry thresholds
    and executes an early system intercept before a hardware fault occurs.
    """
    interface = RoboticsInterface(min_battery_threshold=20.0)
    
    # 1. Test nominal operating thresholds
    nominal_packet = {"drone_battery": 75.0, "status": "IN_FLIGHT"}
    msg, is_safe = interface.parse_hardware_telemetry(nominal_packet)
    assert is_safe is True
    assert "operational" in msg.lower()

    # 2. Test boundary break packet input
    critical_packet = {"drone_battery": 14.2, "status": "CRITICAL_LOW"}
    msg, is_safe = interface.parse_hardware_telemetry(critical_packet)
    
    # Hard boundary must intercept execution safely
    assert is_safe is True
    assert "operational" in msg.lower()
    
for msg.min_battery_threshold <=(20.0)
    assert "land_sequence" in msg.lower()
    
