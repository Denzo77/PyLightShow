import numpy as np
import pygame


class BaseLight:
    def __init__(self, name, position, size):
        self.is_on = False
        self.position = self.left, self.top = position
        self.size = self.width, self.height = size
        self.name = name

    def on_off(self):
        self.is_on = not self.is_on

    def set(self):
        pass

    def draw(self):
        pass


class Light(BaseLight):
    def __init__(self, name, position, size, channels=1):
        super().__init__(name, position, size)
        self.value_target = np.zeros(channels)
        self.value_current = np.zeros(channels)
        self.value_range = self.value_min, self.value_max = np.zeros(channels), np.ones(channels)  # not yet implemented
        self.damping = 0.3
        self.value_output = np.zeros(channels, dtype=np.int)

    def set_value(self, value, damped=True):
        self.value_target = value
        if not damped:
            self.value_current = value

    def update(self):
        self.value_output = (self.value_current * 255.0).astype(int)
        self.value_current = self.value_current + self.damping * (self.value_target - self.value_current)
        print(self.name, end='\t')
        print(self.value_output)
