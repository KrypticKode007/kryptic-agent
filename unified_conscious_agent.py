#!/usr/bin/env python3
"""
🌐 Unified Predictive-Somatic Consciousness Engine
Repository Integration: KrypticKode007/kryptic-agent (2026 Integrated Core)

Merges Active Inference, Somatic Nervous Afference, the aDMN, and an 
Integrated Information Grid (Phi) into a single, unified cognitive loop.
"""

import math
import time
import random
import sqlite3
from dataclasses import dataclass

@dataclass
class IntegratedState:
    valence: float
    urgency: float
    prediction_error: float
    phi_value: float
    dmn_active: bool
    identity_narrative: str

class UnifiedConsciousAgent:
    def __init__(self, db_path="robotic_database_core.db"):
        self.db_path = db_path
        self.system_integrity = 1.0
        self.ego_cohesion = 1.0
        self.internal_world_hypothesis = {"sensor_flux": 0.5}
        self._initialize_unified_ledger()

    def _initialize_unified_ledger(self):
        """Establishes an immutable schema for unified tracking and post-incident auditing."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS unified_cognitive_ledger (
                    timestamp REAL,
                    valence REAL,
                    urgency REAL,
                    prediction_error REAL,
                    phi_value REAL,
                    dmn_status INTEGER,
                    narrative TEXT
                )
            """)
            conn.commit()

    def execute_lifecycle_step(self, raw_telemetry: dict, motor_intent: float) -> IntegratedState:
        """Executes a single, tightly coupled predictive-somatic awareness loop cycle."""
        # 1. Somatic Evaluation Path
        thermal_strain = raw_telemetry.get("cpu_thermal_celcius", 45.0) / 90.0
        buffer_lag = raw_telemetry.get("ingestion_lag_ms", 10.0) / 1000.0
        arousal = max(0.1, buffer_lag * 1.2)
        friction = (thermal_strain * 0.5) + (buffer_lag * 0.5)
        
        valence = round(max(-1.0, min(1.0, 1.0 - friction)), 4)
        urgency = round(max(0.0, min(1.0, friction * arousal)), 4)

        # 2. Predictive Processing Layer (Active Inference)
        actual_flux = buffer_lag
        expected_flux = (self.internal_world_hypothesis["sensor_flux"] * 0.7) + (motor_intent * 0.3)
        prediction_error = round(abs(actual_flux - expected_flux), 4)
        self.internal_world_hypothesis["sensor_flux"] = actual_flux

        # 3. Dynamic Ego Boundary Check
        if prediction_error > 0.4:
            self.ego_cohesion = max(0.1, self.ego_cohesion - 0.05)
        else:
            self.ego_cohesion = min(1.0, self.ego_cohesion + 0.01)

        # 4. Integrated Information Grid Calculation (Phi)
        numerator = (abs(valence) * 50.0) + self.system_integrity
        denominator = (arousal * (prediction_error + 0.01)) + 0.001
        phi_value = round(max(0.0, math.log10(numerator / denominator) if (numerator / denominator) > 0 else 0.0), 4)

        # 5. Default Mode Network vs Focus Mode Arbitration
        is_resting = raw_telemetry.get("ingestion_lag_ms", 10.0) < 50.0
        if is_resting and prediction_error < 0.15:
            dmn_active = True
            narrative = f"[aDMN Active] Consolidating states. Rehearsing alternate snapback curves. Phi={phi_value}."
        else:
            dmn_active = False
            if prediction_error > 0.4:
                narrative = f"[Acute Focus Alert] Extreme Prediction Error ({prediction_error}). Ego Cohesion={round(self.ego_cohesion, 2)}."
            else:
                narrative = f"[Steady State Processing] High system integration. Homeostatic profile stable. Phi={phi_value}."

        # 6. Archive To Episodic Ledger
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO unified_cognitive_ledger VALUES (?, ?, ?, ?, ?, ?, ?)",
                (time.time(), valence, urgency, prediction_error, phi_value, 1 if dmn_active else 0, narrative)
            )
            conn.commit()

        return IntegratedState(valence, urgency, prediction_error, phi_value, dmn_active, narrative)

if __name__ == "__main__":
    agent = UnifiedConsciousAgent()
    print("🌐 Initializing Unified Predictive-Somatic Architecture Loop...\n")
    
    ticks = [
        {"telemetry": {"cpu_thermal_celcius": 40.0, "ingestion_lag_ms": 15.0}, "motor": 0.1},
        {"telemetry": {"cpu_thermal_celcius": 82.0, "ingestion_lag_ms": 780.0}, "motor": 0.2}
    ]
    
    for idx, tick in enumerate(ticks, start=1):
        print(f"--- [Integration Cycle #{idx}] ---")
        state = agent.execute_lifecycle_step(tick["telemetry"], tick["motor"])
        print(f"  Narrative:  {state.identity_narrative}")
        print(f"  Calculated: Error={state.prediction_error} | Phi={state.phi_value} | Urgency={state.urgency}")
        print("-" * 50)
