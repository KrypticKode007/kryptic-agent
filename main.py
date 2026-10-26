import os
import sys
import time
import math
import asyncio
import sqlite3
import logging
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

# Setup optimized system logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("KrypticAgentCore")

# Fallback mechanism for environments missing physical robotic ROS2 binaries
try:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import Float64MultiArray
    HAS_ROS2 = True
except ImportError:
    HAS_ROS2 = False
    logger.warning("ROS2 (rclpy) bindings not detected. Running framework in Hardware Emulation Mode.")

# --- DATABASE LOGISTICS ---
class SQLiteTracker:
    def __init__(self, db_path: str = "tracking_profiles.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS telemetry_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    vfe_value REAL,
                    actuation_drift REAL
                )
            """)

    def log_metrics(self, vfe: float, drift: float):
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO telemetry_logs (timestamp, vfe_value, actuation_drift) VALUES (?, ?, ?)",
                    (time.time(), vfe, drift)
                )
        except Exception as e:
            logger.error(f"Database write failure: {e}")

    def close(self):
        self.conn.close()

# --- ACTIVE INFERENCE & DRIVER ENGINE ---
class KrypticActiveInferenceEngine:
    def __init__(self, dimensions: int = 6):
        self.dimensions = dimensions
        self.mu = [0.0] * dimensions  # Internal states (beliefs)
        self.sensory_states = [0.0] * dimensions  # Sensory inputs
        self.vfe = 0.0  # Variational Free Energy
        self.db = SQLiteTracker()
        
    def read_encrypted_payload(self, packed_payload: bytes) -> Optional[List[float]]:
        """
        Unpacks and reads encrypted sensory state weights.
        Corrects variable unpacking exceptions found in raw branch versions.
        """
        if not packed_payload:
            return None
        try:
            # Emulated structural matrix decryption layout
            unpacked_data = [float(b) / 255.0 for b in packed_payload[:self.dimensions]]
            if len(unpacked_data) < self.dimensions:
                unpacked_data += [0.0] * (self.dimensions - len(unpacked_data))
            return unpacked_data
        except Exception as e:
            logger.error(f"Error unpacking encrypted payload variables: {e}")
            return None

    def compute_variational_free_energy(self) -> float:
        """
        Executes deterministic VFE matrix loop tracking sensory deviations.
        """
        error_sensory = 0.0
        for i in range(self.dimensions):
            diff = self.sensory_states[i] - self.mu[i]
            error_sensory += diff ** 2
            # High-velocity sensory-motor belief revision update
            self.mu[i] += 0.01 * diff  
        self.vfe = 0.5 * error_sensory
        return self.vfe

# --- NATIVE ROS2 HARDWARE LINK ---
if HAS_ROS2:
    class KrypticROS2Driver(Node):
        def __init__(self, engine: KrypticActiveInferenceEngine):
            super().__init__("kryptic_ros2_driver")
            self.engine = engine
            self.publisher_ = self.create_publisher(Float64MultiArray, "/kryptic/actuator_cmds", 10)
            self.subscription_ = self.create_subscription(
                Float64MultiArray, "/kryptic/sensor_stream", self.sensory_callback, 10
            )

        def sensory_callback(self, msg: Float64MultiArray):
            if len(msg.data) >= self.engine.dimensions:
                self.engine.sensory_states = list(msg.data[:self.engine.dimensions])

        def publish_actuation(self):
            msg = Float64MultiArray()
            msg.data = self.engine.mu
            self.publisher_.publish(msg)
else:
    class KrypticROS2Driver:
        def __init__(self, engine: KrypticActiveInferenceEngine):
            self.engine = engine
        def publish_actuation(self):
            # Hardware Emulation Mode step tracking
            for i in range(self.engine.dimensions):
                self.engine.sensory_states[i] += math.sin(time.time() + i) * 0.05

# --- FASTAPI WEB INTERFACE ---
app = FastAPI(title="Kryptic-Agent Telemetry Dashboard")
engine = KrypticActiveInferenceEngine()

# Safe global initialization wrapper hook for ROS2 runtime boundaries
ros2_node: Optional[Any] = None
if HAS_ROS2:
    if not rclpy.ok():
        rclpy.init()
    ros2_node = KrypticROS2Driver(engine)
else:
    ros2_node = KrypticROS2Driver(engine)

connected_websockets: List[WebSocket] = []

@app.websocket("/ws/telemetry")
async def telemetry_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.append(websocket)
    try:
        while True:
            await asyncio.sleep(1.0)  # Keep connection alive
    except WebSocketDisconnect:
        connected_websockets.remove(websocket)

async def broadcast_telemetry(data: Dict[str, Any]):
    for ws in connected_websockets:
        try:
            await ws.send_json(data)
        except Exception:
            continue

# --- 1000Hz DETERMINISTIC RUNTIME EXECUTION COROUTINE ---
async def active_inference_loop():
    target_dt = 0.001  # Deterministic 1000Hz cadence (1ms)
    logger.info("Starting active inference engine loop at 1000Hz clock speed.")
    
    while True:
        t_start = time.perf_counter()
        
        # 1. Process ROS2 message queues safely if active
        if HAS_ROS2 and rclpy.ok():
            rclpy.spin_once(ros2_node, timeout_sec=0.0)
            
        # 2. Update Free Energy Matrix calculations
        vfe_metric = engine.compute_variational_free_energy()
        
        # 3. Publish sub-millisecond multi-axis corrections
        ros2_node.publish_actuation()
        
        # 4. Stream internal state logs asynchronously to database and web dashboard
        drift_calculation = sum([abs(m) for m in engine.mu])
        engine.db.log_metrics(vfe_metric, drift_calculation)
        
        if len(connected_websockets) > 0:
            payload = {
                "vfe": vfe_metric,
                "mu": engine.mu,
                "drift": drift_calculation,
                "timestamp": time.time()
            }
            asyncio.create_task(broadcast_telemetry(payload))
            
        t_end = time.perf_counter()
        elapsed = t_end - t_start
        sleep_time = target_dt - elapsed
        
        if sleep_time > 0:
            await asyncio.sleep(sleep_time)
        else:
            # Yield minimal execution slicing when hardware frames experience slight drift
            await asyncio.sleep(0)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(active_inference_loop())

@app.on_event("shutdown")
def shutdown_event():
    engine.db.close()
    if HAS_ROS2 and rclpy.ok():
        rclpy.shutdown()
    logger.info("Kryptic-Agent Engine successfully halted.")

if __name__ == "__main__":
    # Runs the web management node on default local cluster configuration ports
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")
    
