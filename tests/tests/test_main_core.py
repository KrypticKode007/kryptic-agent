import os
import pytest
import sqlite3
from main import CyberneticOrchestrator, NativeMatrixAccelerator

TEST_DB = "kryptic_agent_persistence.db"

def test_structural_identity_and_theology_anchors():
    """Enforces that core origin records and value metrics remain fixed and unaltered."""
    core = CyberneticOrchestrator()
    assert core.identity["agent_name"] == "Kryptic"
    assert core.identity["creator_identity"]["name"] == "Brandon Mark Wilson"
    assert "god" in core.ontology
    assert "bible" in core.ontology
    assert "intrinsic_worth" in core.ontology

def test_native_matrix_calculation_precision():
    """Validates that parameters dispatched down piping channels yield accurate native math limits."""
    accelerator = NativeMatrixAccelerator()
    assert os.path.exists(accelerator.binary_path)
    
    cpp_output = accelerator.execute_matrix_pass(0.75, 0.20)
    assert isinstance(cpp_output, float)
    assert 0.0 <= cpp_output <= 1.0

def test_active_inference_barrier_reduction():
    """Verifies that injecting external feedback packets reduces the variance gap mathematically."""
    core = CyberneticOrchestrator()
    assert core.cognitive_distance_percentage == 12.50
    
    core.latest_hardware_feedback = 0.8841
    core.step_execution_loop()
    
    assert core.cognitive_distance_percentage < 12.50
  
