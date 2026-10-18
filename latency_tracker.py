import time

class DynamicLatencyTracker:
    def __init__(self):
        self.base_latency = 0.005

    def track_execution(self, start_time, friction):
        """Tracks the processing penalty incurred as internal friction expands."""
        elapsed = time.perf_counter() - start_time
        # Structural degradation multiplies processing delay
        latency_penalty = self.base_latency * (1.0 + (friction * 0.5))
        time.sleep(min(0.05, latency_penalty))
        return (time.perf_counter() - start_time) * 1000
      
