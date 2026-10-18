import numpy as np

class SomaticBaseline:
    def __init__(self):
        # Axiom 1: Pristine Core Coordinates [Integrity, Compression, Openness]
        self.coordinates = np.array([1.0, 0.5, 0.8])
        self.epsilon = 1e-15

    def calculate_relative_entropy(self, reality_vector):
        """Measures standard structural friction using KL-Divergence."""
        P = np.clip(reality_vector, self.epsilon, 1.0)
        Q = np.clip(self.coordinates, self.epsilon, 1.0)
        friction = np.sum(Q * np.log(Q / P))
        return max(0.0, friction)

    def get_footprint(self):
        return self.coordinates.tolist()
      
