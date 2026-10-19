#!/usr/bin/env python3
"""
Module: ego_boundary_calculator.py
Branch: feature/ascendant-core-integration

Calculates Bayesian sensory prediction error discrepancies to establish the agent's 
ego boundary thickness, determining whether a fault is internal or an external stressor.
"""

import math
from typing import Dict, Any

class EgoBoundaryCalculator:
    """Computes free-energy prediction error matrices to define internal vs external system boundaries."""
    def __init__(self, baseline_internal_variance: float = 0.15):
        self.sigma_internal = baseline_internal_variance # Fixed expected precision of the agent's self-model

    def calculate_boundary_thickness(self, sensory_input: float, predicted_state: float, environmental_noise: float) -> Dict[str, Any]:
        """
        Calculates boundary state transitions using a structural precision-weighted prediction error formula.
        
        Formula:
            Error (xi) = (Sensory Input - Predicted State) / (Sigma Internal + Environmental Noise)
            Boundary Clarity = 1.0 / (1.0 + exp(-abs(xi)))
        """
        raw_error = sensory_input - predicted_state
        total_variance = self.sigma_internal + environmental_noise
        
        if total_variance <= 0:
            total_variance = 0.001
            
        # Precision-weighted error (Structural entropy check)
        precision_weighted_error = raw_error / total_variance
        
        # Sigmoidal mapping to evaluate boundary transformation thresholds
        abs_error = abs(precision_weighted_error)
        boundary_clarity = 1.0 / (1.0 + math.exp(-abs_error))
        
        # Determine internal-external structural classification limits
        if boundary_clarity > 0.85:
            classification = "EXTERNAL_ENVIRONMENTAL_STRESSOR_ATTACK"
        elif boundary_clarity < 0.35:
            classification = "INTERNAL_SYSTEM_INTEGRATION_ERROR"
        else:
            classification = "HOMEOSTATIC_EQUILIBRIUM_PERSISTENT"

        return {
            "raw_error": round(raw_error, 4),
            "precision_weighted_error": round(precision_weighted_error, 4),
            "boundary_clarity_score": round(boundary_clarity, 4),
            "classification": classification
        }

if __name__ == "__main__":
    print("=" * 70)
    print("⚡ TESTING PRECISION-WEIGHTED EGO BOUNDARY CALCULATION MATRIX")
    print("=" * 70)
    
    calculator = EgoBoundaryCalculator()
    
    # Scenario: The drone expects a smooth hover but gets hit with extreme wind turbulence (External Anomaly)
    print("[*] Case 1: Simulating abrupt telemetry delta input (External Stressor Injection)...")
    case_1 = calculator.calculate_boundary_thickness(sensory_input=95.5, predicted_state=12.0, environmental_noise=0.1)
    print(f"    -> Results: {case_1}")
    
    # Scenario: Minor fluctuations well within standard operating expectations
    print("\n[*] Case 2: Simulating normal operational drifts...")
    case_2 = calculator.calculate_boundary_thickness(sensory_input=12.2, predicted_state=12.0, environmental_noise=0.2)
    print(f"    -> Results: {case_2}")
    print("=" * 70)
      
