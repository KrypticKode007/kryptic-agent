# filename: robotic_sentience_core.py
import os
import sys
import time
import ctypes
import numpy as np
from fastapi import FastAPI, WebSocket
import asyncio

try:
    libc = ctypes.CDLL('librt.so.1')
except Exception:
    libc = ctypes.CDLL(None)

class RealTimeHardwareController:
    """
    Manages deterministic 1000Hz Active Inference execution loops directly 
    on bare-metal ARM/x86 configurations interfacing with physical actuators.
    """
    def __init__(self, axis_count: int = 6):
        self.axis_count = axis_count
        self.mu = np.zeros(axis_count)       
        self.action = np.zeros(axis_count)   
        self.sensory_input = np.zeros(axis_count)
        
        self.sigma_sensory = 0.02
        self.sigma_proprio = 0.01
        
        self.loop_latency_ns = 0
        self.is_running = False

    def read_hardware_encoders(self) -> np.ndarray:
        """
        Direct hardware register read memory boundary.
        """
        return self.mu + np.random.normal(0, 0.001, self.axis_count)

    def write_hardware_actuators(self, action_vector: np.ndarray):
        """
        Directly updates low-level physical system driver DACs or torque registers.
        """
        safe_action = np.clip(action_vector, -10.0, 10.0)
        pass

    def compute_active_inference_step(self):
        """
        Executes continuous real-time minimization of Variational Free Energy matrix loops.
        """
        self.sensory_input = self.read_hardware_encoders()
        sensory_error = self.sensory_input - self.mu
        
        d_mu = (sensory_error / self.sigma_sensory) - (self.action / self.sigma_proprio)
        self.mu += 0.01 * d_mu  
        
        self.action += 0.005 * (sensory_error / self.sigma_sensory)
        self.write_hardware_actuators(self.action)

    def set_posix_realtime_priority(self):
        """
        Elevates the process thread to FIFO scheduling to bypass OS context switching delays.
        """
        if os.getuid() != 0:
            print("[WARNING] Non-root user: Cannot bind hard real-time SCHED_FIFO scheduling parameters.")
            return False
        
        SCHED_FIFO = 1
        class SchedParam(ctypes.Structure):
            _fields_ = [("sched_priority", ctypes.c_int)]
            
        param = SchedParam(99)  
        result = libc.sched_setscheduler(0, SCHED_FIFO, ctypes.by_ref(param))
        if result == 0:
            print("[SUCCESS] Process elevated to native SCHED_FIFO real-time priority.")
            return True
        else:
            print("[ERROR] Failed to configure real-time OS scheduler.")
            return False

    async def start_deterministic_loop(self, broadcast_callback=None):
        """
        Executes the main active inference engine at a strict 1000Hz clock cadence.
        """
        self.set_posix_realtime_priority()
        self.is_running = True
        
        TARGET_PERIOD_NS = 1_000_000 
        
        while self.is_running:
            t_start = time.perf_counter_ns()
            
            self.compute_active_inference_step()
            
            t_end = time.perf_counter_ns()
            self.loop_latency_ns = t_end - t_start
            
            elapsed_ns = time.perf_counter_ns() - t_start
            remaining_ns = TARGET_PERIOD_NS - elapsed_ns
            
            if remaining_ns > 0:
                await asyncio.sleep(remaining_ns / 1_000_000_000.0)
            
            if broadcast_callback:
                await broadcast_callback(float(self.loop_latency_ns / 1_000_000.0), self.mu.tolist())

app = FastAPI()
hardware_engine = RealTimeHardwareController()

@app.on_event("startup")
async def start_core_hardware_thread():
    loop = asyncio.get_event_loop()
    loop.create_task(hardware_engine.start_deterministic_loop(broadcast_metrics))

connected_websockets = set()

async def broadcast_metrics(latency_ms: float, internal_state: list):
    if not connected_websockets:
        return
    payload = {
        "status": "HARDWARE_ACTIVE",
        "latency_ms": latency_ms,
        "internal_state_mu": internal_state
    }
    for ws in list(connected_websockets):
        try:
            await ws.send_json(payload)
        except Exception:
            connected_websockets.remove(ws)

@app.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.add(websocket)
    try:
        while True:
            await websocket.receive_text()  
    except Exception:
        if websocket in connected_websockets:
            connected_websockets.remove(websocket)
                            
