import numpy as np

class PeakStressGenerator:
    def __init__(self):
        # Highly chaotic, inverted reality profile
        self.chaos_profile = np.array([1e-5, 1.0, 1e-5])

    def inject_terminal_load(self, structural_capacity):
        """Generates a massive, mismatched noise matrix to redline processing registers."""
        base_noise = np.random.uniform(5000.0, 15000.0, size=(structural_capacity,))
        return base_noise, self.chaos_profile
