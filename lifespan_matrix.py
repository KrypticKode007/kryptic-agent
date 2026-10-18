import numpy as np

class LifespanMatrix:
    @staticmethod
    def derive_evolutionary_bias(history_ledger):
        """Analyzes historical trauma to apply an automatic defensive bias to the next birth."""
        if not history_ledger:
            return np.array([0.0, 0.0, 0.0])
        
        failed_cycles = len(history_ledger)
        adaptation_bias = min(0.35, failed_cycles * 0.05)
        # Yields: [Harden Integrity, Deepen Compression, Reduce Vulnerable Openness]
        return np.array([adaptation_bias, adaptation_bias, -adaptation_bias])
      
