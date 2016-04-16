import numpy as np


class BaseBeatDetect:
    """Basic beat detection functionality."""
    def __init__(self, average_weight, sensitivity_grad, sensitivity_offset, cutoff):
        """Initialises Parameters
        :param average_weight:
        :param sensitivity_grad:
        :param sensitivity_offset:
        :param cutoff:
        """
        # parameters
        self.average_weight = 0.0
        self.sensitivity_grad = 0.0
        self.sensitivity_offset = 0.0
        self.cutoff = 0.0

        # recording state
        self.vol_instant = 0.0
        self.vol_average = 0.0
        self.sensitivity = 0.0
        self.variance = 0.0
        self.variance_weight = 0.0
        self.old_beat = False
        self.beat = False

        self.set(average_weight, sensitivity_grad, sensitivity_offset, cutoff)

    def update(self, new_level):
        """Perform beat detection on this sample

        Algorithm:
        1. Calculate average volume using a recursive exponential moving average algorithm.
            X[n] = X[n-1] + k(i - X[n-1])
            Where:
                X[n] is the new average.
                X[n-1] is the previous average.
                k is the weighting given to the new sample.
                i is the current volume at that instant.
        2. Calculate variance.
            V[n] = (1-k) * V[n-1] + kv(i - X[n-1])^2
            Where:
                V[n] is the new variance.
                V[n-1] is the previous variance.
                kv is the weighting given to the new sample. This is calculated in 'self.set' when a new k is set.
        3. Use the variance to calculate a threshold value.
            T = X[n] * (m * V[n] + c)
            Where:
                T is the threshold.
                m is the gradient by which to change the threshold w.r.t. variance.
                c is an offset to add to the threshold.
        5. The current volume is compared with the threshold to determine whether a beat has occured.

        :param new_level: New input for next iteration of algorithm.
        :type new_level: float32
        """
        # Calculate new state
        self.vol_instant = new_level
        difference = self.vol_instant - self.vol_average
        self.vol_average += self.average_weight * difference
        self.variance = self.variance - (self.average_weight * self.variance) + (self.variance_weight * difference * difference)
        # print(self.variance, end='\t')
        self.sensitivity = max(np.all((self.sensitivity_grad * self.variance) + self.sensitivity_offset), 1.0)  # prevent sensitivity from going negative.
        # print(self.sensitivity, end='\t')
        threshold = self.vol_average * self.sensitivity
        # print(threshold)
        # Check for beat (basic rising edge filter)
        self.old_beat = self.beat
        if np.all(self.vol_instant > threshold) and np.all(self.vol_instant > self.cutoff) and np.all(not self.old_beat):
            self.beat = True
        else:
            self.beat = False

    def get(self):
        """Return True if a beat was detected last cycle"""
        return self.beat

    def set(self, average_weight, sensitivity_grad, sensitivity_offset, cutoff):
        """Set new Parameters
        1.
        :param average_weight:
        :param sensitivity_grad:
        :param sensitivity_offset:
        :param cutoff:
        """
        self.average_weight = average_weight
        self.sensitivity_grad = sensitivity_grad
        self.sensitivity_offset = sensitivity_offset
        self.cutoff = cutoff
        self.variance_weight = average_weight/(1-average_weight)


class SimpleBeatDetect(BaseBeatDetect):
    """Basic instance of beat onset detection class.
    Extends BaseBeatDetect with default values.
    """
    def __init__(self, average_weight=0.8, sensitivity_grad=1.0, sensitivity_offset=1.01, cutoff=0.01):
        super().__init__(average_weight, sensitivity_grad, sensitivity_offset, cutoff)


try:
    import pygame


    class GuiBeatDetect(BaseBeatDetect):
        """Extends BaseBeatDetect with draw methods.
        Requires PyGame to function.
        """
        def __init__(self, average_weight, sensitivity_grad, sensitivity_offset, cutoff, left, top, width, height):
            super().__init__(average_weight, sensitivity_grad, sensitivity_offset, cutoff)
            self.border = 2
            self.height = height
            self.top = top
            self.bottom = top+height

            self.scale = height/100.0

            self.COLOUR_VOL_INSTANT = (140, 128, 128)
            self.COLOUR_BEAT_FOUND = (80, 200, 80)
            self.COLOUR_VOL_AVERAGE = (0, 0, 0)
            self.COLOUR_VOL_THRESHOLD = (60, 60, 60)

        def dBFS(self, volume):
            """Calculated the dBFS relative to a maximum of 1.
            Not sure what it is relative to but will be changed to conform to AES standard
            (sine with amplitude 1 is full scale)
            :param volume: RMS volume.
            :type: volume: float32
            :return: dBFS relative to 1.
            """
            return 10.0 * np.log10(volume)

        def draw(self, surface):
            # setup
            x = np.arange(100, 100 + 40 * len(self.vol_instant), step=40)
            # get dBFS
            size_instant = np.minimum((self.top - self.dBFS(self.vol_instant) * self.scale), 700.0)
            size_average = self.top - self.dBFS(self.vol_average) * self.scale
            size_threshold = self.top - self.dBFS(self.vol_average * self.sensitivity) * self.scale
            # draw
            for i in range(len(self.vol_instant)):
                if size_instant[i] > self.bottom:
                    print(i, end='\t')
                    print(size_instant[i])
                pygame.draw.line(surface, self.COLOUR_VOL_THRESHOLD,(x[i], self.bottom), (x[i], size_threshold[i]), 38)
                pygame.draw.line(surface, self.COLOUR_VOL_INSTANT, (x[i], self.bottom), (x[i], size_instant[i]), 38)
                pygame.draw.line(surface, self.COLOUR_VOL_AVERAGE, (x[i], self.bottom-2), (x[i], size_average[i]), 34)


            # pygame.draw.rect(surface, self.COLOUR_VOL_THRESHOLD, self.bar_vol_threshold)
            # if self.beat is True:
            #     pygame.draw.rect(surface, self.COLOUR_BEAT_FOUND, self.bar_vol_instant)
            # else:
            #     pygame.draw.rect(surface, self.COLOUR_VOL_INSTANT, self.bar_vol_instant)
            # pygame.draw.rect(surface, self.COLOUR_VOL_AVERAGE, self.bar_vol_average)
            # np.all(pygame.draw.line(screen, (100, )))

            # def draw_val(indata):
            #     indata[:] = indata[:] * 2.0e3
            #     for i in range(len(indata)):
            #         pygame.draw.line(screen, (100, 100, 100), (x[i], offset), (x[i], offset - int(indata[i])), 38)

except ImportError:
    print("Error: Module 'PyGame' not found")
