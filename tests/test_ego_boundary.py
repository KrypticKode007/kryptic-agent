# tests/test_ego_boundary.py
"""
Custom unit test suite validating precision-weighted prediction error equations
and boundary clarity transitions under extreme environmental noise payloads.
"""

import pytest
import math
from ego_boundary_calculator import EgoBoundaryCalculator

def test_ego_boundary_equilibrium_state():
    """Verifies that minor telemetry drift remains classified under Homeostatic Equilibrium."""
    calculator = EgoBoundaryCalculator(baseline_internal_variance=0.15)
    
    # Sensory input matches prediction with low noise drift
    result = calculator.calculate_boundary_thickness(
        sensory_input=12.2, 
        predicted_state=12.0, 
        environmental_noise=0.05
    )
    
    assert result["boundary_clarity_score"] >= 0.0
    assert result["boundary_clarity_score"] <= 1.0
    assert result["classification"] == "HOMEOSTATIC_EQUILIBRIUM_PERSISTENT"

def test_external_stressor_classification():
    """Verifies that major deviations trigger the External Environmental Stressor flag."""
    calculator = EgoBoundaryCalculator(baseline_internal_variance=0.15)
    
    # Massively divergent input simulating external jamming or payload force anomalies
    result = calculator.calculate_boundary_thickness(
        sensory_input=150.0, 
        predicted_state=10.0, 
        environmental_noise=0.1
    )
    
    assert result["boundary_clarity_score"] > 0.85
    assert result["classification"] == "EXTERNAL_ENVIRONMENTAL_STRESSOR_ATTACK"

def test_zero_variance_division_safeguard():
    """Guarantees that the calculator suppresses zero-division edge cases under empty noise loads."""
    calculator = EgoBoundaryCalculator(baseline_internal_variance=0.0)
    
    # Forcing zero variance parameters directly into the division matrix
    result = calculator.calculate_boundary_thickness(
        sensory_input=15.0, 
        predicted_state=10.0, 
        environmental_noise=0.0
    )
    
    # Safeguard should fallback smoothly without throwing ZeroDivisionError exceptions
    assert isinstance(result["precision_weighted_error"], float)
    assert not math.isnan(result["precision_weighted_error"])
  
