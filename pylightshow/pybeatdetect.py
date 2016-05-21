"""
Beat onset detection class.

How To Use:

TODO!

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
"""
import numpy as np


class BaseBeatDetect:
    """
    Basic beat detection functionality.
    """
    def __init__(self, average_weight, sensitivity_grad, sensitivity_offset, cutoff):
        """Initialises Parameters
        :param: average_weight: The weighting assigned to a new value when updating the average.
        :param: sensitivity_grad:
        :param: sensitivity_offset:
        :param: cutoff: The minimum signal level that must be present for a beat to be returned.
        """
        # parameters
        self.average_weight = np.array([0.0])
        self.sensitivity_grad = np.array([0.0])
        self.sensitivity_offset = np.array([0.0])
        self.cutoff = np.array([0.0])

        # recording state
        self.vol_instant = np.array([0.0])
        self.vol_average = np.array([0.0])
        self.sensitivity = np.array([0.0])
        self.variance = np.array([0.0])
        self.variance_weight = np.array([0.0])
        self.old_beat = np.array([False])
        self.beat = np.array([False])

        self.set(average_weight, sensitivity_grad, sensitivity_offset, cutoff)

    def update(self, new_level):
        """
        Takes in a new sample and runs the beat onset detection algorithm.

        :param new_level: New input for next iteration of algorithm.
        :type new_level: float32
        :return: None
        """
        # Calculate new state
        self.vol_instant = new_level
        difference = self.vol_instant - self.vol_average
        self.vol_average = self.vol_average + self.average_weight * difference
        self.variance = self.variance - (self.average_weight * self.variance) + (self.variance_weight * np.power(difference, 2))
        # print(self.variance, end='\t')
        self.sensitivity = np.maximum(((self.sensitivity_grad * self.variance) + self.sensitivity_offset), 1.0)  # prevent sensitivity from going negative.
        # print(self.sensitivity, end='\t')
        threshold = self.vol_average * self.sensitivity
        # Check for beat (basic rising edge filter)
        self.old_beat = self.beat
        self.beat = np.logical_and(self.vol_instant > threshold, self.vol_instant > self.cutoff)
        self.beat = np.logical_and(self.beat, np.logical_not(self.old_beat))

    def get(self):  # TODO Replace this with __eq__(self)
        """
        :returns: True if a beat has been detected.
        """
        return self.beat

    def set(self, average_weight, sensitivity_grad, sensitivity_offset, cutoff):
        """
        Sets new parameters and calculates the new weighting of the variance.

        :param: average_weight: The weighting assigned to a new value when updating the average.
        :param: sensitivity_grad:
        :param: sensitivity_offset:
        :param: cutoff: The minimum signal level that must be present for a beat to be returned.
        :return: None
        """
        self.average_weight = average_weight
        self.sensitivity_grad = sensitivity_grad
        self.sensitivity_offset = sensitivity_offset
        self.cutoff = cutoff
        self.variance_weight = average_weight/(1.0-average_weight)


class SimpleBeatDetect(BaseBeatDetect):
    """
    Basic instance of beat onset detection class.
    Extends BaseBeatDetect with default values.
    """
    def __init__(self, average_weight=0.8, sensitivity_grad=1.0, sensitivity_offset=1.01, cutoff=0.01):
        super().__init__(average_weight, sensitivity_grad, sensitivity_offset, cutoff)


try:  # Trying to make it pygame agnostic.
    import pygame


    class PlotBeatDetect(BaseBeatDetect):
        """
        Extends BaseBeatDetect with draw methods.
        Requires PyGame to function.
        """
        def __init__(self, average_weight, sensitivity_grad, sensitivity_offset, cutoff, position, size):
            """

            :param: average_weight: The weighting assigned to a new value when updating the average.
            :param: sensitivity_grad:
            :param: sensitivity_offset:
            :param: cutoff: The minimum signal level that must be present for a beat to be returned.
            :param position:
            :param size:
            """
            super().__init__(average_weight, sensitivity_grad, sensitivity_offset, cutoff)
            self.border = 0
            self.position = self.left, self.top = position
            self.size = self.width, self.height = size
            self.bottom = self.top + self.height
            self.scale = self.height / 100.0

            self.bar_width = self.width - self.border

            self.COLOUR_VOL_INSTANT = (255, 100, 100)
            self.COLOUR_BEAT_FOUND = (100, 255, 100)
            self.COLOUR_VOL_AVERAGE = (0, 0, 0)
            self.COLOUR_VOL_THRESHOLD = (100, 100, 100)

        def dBFS(self, volume):
            """
            Calculated the dBFS relative to a maximum of 1.
            Not sure what it is relative to but will be changed to conform to AES standard
            (sine with amplitude 1 is full scale)
            :param volume: RMS volume.
            :type: volume: float32
            :return: dBFS relative to 1.
            """
            return 10.0 * np.log10(volume)

        def draw(self, surface):  # TODO! Force draw to be above bottom of plot
            """
            Draws a plot of the beat detection object(s) on a surface.
            The plot is drawn at self.position and is bounded by self.size.
            :param surface: The surface to draw the plot on.
            :return: None
            """
            # get dBFS
            size_instant = np.minimum((self.top - self.dBFS(self.vol_instant) * self.scale), 700.0)
            size_average = self.top - self.dBFS(self.vol_average) * self.scale
            size_threshold = self.top - self.dBFS(self.vol_average * self.sensitivity) * self.scale
            # draw lines
            pygame.draw.line(surface, self.COLOUR_VOL_THRESHOLD, (self.left, self.bottom),
                             (self.left, size_threshold), self.bar_width)
            pygame.draw.line(surface, self.COLOUR_VOL_AVERAGE, (self.left, self.bottom),
                             (self.left, size_average), self.bar_width)
            # Change the colour of the instantaneous volume plot if there is a beat.
            if self.beat:
                pygame.draw.line(surface, self.COLOUR_BEAT_FOUND, (self.left, size_average),
                                 (self.left, size_instant), self.bar_width)
            else:
                pygame.draw.line(surface, self.COLOUR_VOL_INSTANT, (self.left, size_average),
                                 (self.left, size_instant), self.bar_width)

            # # Loop through beat detection instances, drawing them all.
            # for i in range(len(self.vol_instant)):
            #     pygame.draw.line(surface, self.COLOUR_VOL_THRESHOLD, (self.bar_x_pos[i], self.bottom),
            #                      (self.bar_x_pos[i], size_threshold[i]), self.bar_width)
            #     pygame.draw.line(surface, self.COLOUR_VOL_AVERAGE, (self.bar_x_pos[i], self.bottom),
            #                      (self.bar_x_pos[i], size_average[i]), self.bar_width)
            #     # Change the colour of the instantaneous volume plot if there is a beat.
            #     if self.beat[i]:
            #         pygame.draw.line(surface, self.COLOUR_BEAT_FOUND, (self.bar_x_pos[i], size_average[i]),
            #                          (self.bar_x_pos[i], size_instant[i]), self.bar_width)
            #     else:
            #         pygame.draw.line(surface, self.COLOUR_VOL_INSTANT, (self.bar_x_pos[i], size_average[i]),
            #                          (self.bar_x_pos[i], size_instant[i]), self.bar_width)


except ImportError:
    print("Error: Module 'PyGame' not found")
