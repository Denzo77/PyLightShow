class BasicBeatDetect:
    """Basic beat detection functionality."""
    def __init__(self, average_weight=0.8, sensitivity_grad=-2.0e-8, sensitivity_offset=1.4, cutoff=0.1):
        """Initialises Parameters
        :param average_weight:
        :param sensitivity_grad:
        :param sensitivity_offset:
        :param cutoff:
        """
        # parameters
        self.average_weight = average_weight
        self.sensitivity_grad = sensitivity_grad
        self.sensitivity_offset = sensitivity_offset
        self.cutoff = cutoff

        # recording state
        self.vol_instant = 0.0
        self.vol_average = 0.0
        self.sensitivity = 0.0
        self.variance = 0.0
        self.variance_weight = 0.0
        self.old_beat = False
        self.beat = False

    def update(self, new_level):
        """Perform beat detection on this sample

        NOTES ON ALGORITHM HERE

        :param new_level: New input for next iteration of algorithm.
        :type new_level: float32
        """
        # Calculate new state
        self.vol_instant = new_level
        difference = self.vol_instant - self.vol_average
        self.vol_average += self.average_weight * difference
        self.variance -= (self.average_weight * self.variance) + (self.variance_weight * difference * difference)
        self.sensitivity = (self.sensitivity_grad * self.variance) + self.sensitivity_offset
        threshold = self.vol_average * self.sensitivity
        # Check for beat (basic rising edge filter)
        self.old_beat = self.beat
        if (self.vol_instant > threshold) and (self.vol_instant > self.cutoff) and (not self.old_beat):
            self.beat = True
        else:
            self.beat = False

    def get(self):
        """Return True if a beat was detected last cycle"""
        return self.beat

    def set(self, average_weight, sensitivity_grad, sensitivity_offset, cutoff):
        """Set new Parameters
        :param average_weight:
        :param sensitivity_grad:
        :param sensitivity_offset:
        :param cutoff:
        """
        self.average_weight = average_weight
        self.sensitivity_grad = sensitivity_grad
        self.sensitivity_offset = sensitivity_offset
        self.cutoff = cutoff
