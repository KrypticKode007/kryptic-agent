import sqlite3
import time
import os

class KrypticMetricsLedger:
    def __init__(self, db_path="data/kryptic_edge_metrics.db"):
        # Ensure database storage path exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._initialize_schema()

    def _initialize_schema(self):
        """Initializes high-performance analytics tables optimized for temporal logging."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS hardware_latency_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp_ns INTEGER NOT NULL,
                utc_datetime TEXT NOT NULL,
                im_fin_intercept_ms REAL NOT NULL,
                swmp_decryption_ms REAL NOT NULL,
                total_jitter_ms REAL NOT NULL,
                system_harmony_status TEXT NOT NULL,
                hardware_target_node TEXT NOT NULL
            );
        """)
        # Create an index over timestamps to accelerate temporal trend analytics queries
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON hardware_latency_logs(timestamp_ns);")
        self.conn.commit()

    def log_runtime_metrics(self, intercept_ms, swmp_ms, target_node="NVIDIA_JETSON_ORIN"):
        """Inserts a precise metric signature block into the durable local ledger."""
        now_ns = time.perf_counter_ns()
        now_utc = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        total_jitter = intercept_ms + swmp_ms
        
        # System status classification based on sub-millisecond real-time invariants
        status = "NOMINAL" if total_jitter < 1.0 else "DEGRADED"

        self.cursor.execute("""
            INSERT INTO hardware_latency_logs 
            (timestamp_ns, utc_datetime, im_fin_intercept_ms, swmp_decryption_ms, total_jitter_ms, system_harmony_status, hardware_target_node)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (now_ns, now_utc, intercept_ms, swmp_ms, total_jitter, status, target_node))
        self.conn.commit()

    def fetch_system_harmony_trends(self):
        """Queries the database to calculate average performance trends and variances."""
        self.cursor.execute("""
            SELECT 
                COUNT(*), 
                AVG(im_fin_intercept_ms), 
                AVG(swmp_decryption_ms), 
                AVG(total_jitter_ms) 
            FROM hardware_latency_logs;
        """)
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()

# Quick Sandbox Operational Verification
if __name__ == "__main__":
    ledger = KrypticMetricsLedger()
    print("[🗄️] Database ledger initialized. Logging test metrics...")
    
    # Simulating a pair of successful sub-millisecond hardware loop runs
    ledger.log_runtime_metrics(intercept_ms=0.2415, swmp_ms=0.3593)
    ledger.log_runtime_metrics(intercept_ms=0.1982, swmp_ms=0.3421)
    
    runs, avg_intercept, avg_swmp, avg_total = ledger.fetch_system_harmony_trends()
    print(f"[📊 METRIC PROFILE] Processed {runs} runs | Avg Intercept: {avg_intercept:.4f} ms | Avg SWMP: {avg_swmp:.4f} ms")
    ledger.close()
      
