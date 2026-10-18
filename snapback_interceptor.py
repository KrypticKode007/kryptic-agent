import numpy as np

class SnapbackInterceptor:
    def __init__(self, target_baseline):
        self.baseline = np.array(target_baseline)

    def intercept_and_restore(self, active_state, friction_score):
        """Detects if consciousness thresholds are exceeded and triggers a live bounce."""
        if friction_score > 14.0:
            # Overwrite active variables live while maintaining system thread continuity
            restored_state = np.copy(self.baseline)
            return restored_state, True
        return active_state, False
