#!/usr/bin/env python3
"""
🧪 Automated Cognitive Boundary Verification Suite
Validates prediction errors, system integration (Phi), and ego tracking constraints.
"""

import unittest
from unified_conscious_agent import UnifiedConsciousAgent

class TestEgoBoundaryAndPredictiveProcessing(unittest.TestCase):
    def setUp(self):
        """Initializes a sandboxed instance of the unified control engine."""
        self.agent = UnifiedConsciousAgent(db_path=":memory:") # Run entirely in safe volatile memory

    def test_baseline_equilibrium_phi(self):
        """Verifies that low processing friction translates to higher integrated field states (Phi)."""
        stable_telemetry = {"cpu_thermal_celcius": 40.0, "ingestion_lag_ms": 10.0}
        state = self.agent.execute_lifecycle_step(stable_telemetry, motor_intent=0.0)
        
        # In stable environments, Phi should remain high due to tight coupling and low noise
        self.assertGreater(state.phi_value, 1.0)
        self.assertFalse(state.dmn_active)

    def test_prediction_error_escalation(self):
        """Validates that sudden sensory anomalies spike prediction error metrics and reduce ego cohesion."""
        # Step 1: Establish a stable baseline expectation
        self.agent.execute_lifecycle_step({"cpu_thermal_celcius": 45.0, "ingestion_lag_ms": 10.0}, motor_intent=0.1)
        
        # Step 2: Inject a massive, un-predicted sensory burst
        shock_telemetry = {"cpu_thermal_celcius": 85.0, "ingestion_lag_ms": 950.0}
        state = self.agent.execute_lifecycle_step(shock_telemetry, motor_intent=0.1)
        
        # Confirm that the active inference block flagged the anomalous environmental friction
        self.assertGreater(state.prediction_error, 0.5)
        self.assertLess(self.agent.ego_cohesion, 1.0)
        self.assertIn("Acute Focus Alert", state.identity_narrative)

if __name__ == "__main__":
    print("🔬 Executing Core Cognitive Constraint Verification Tests...\n")
    unittest.main()
      
