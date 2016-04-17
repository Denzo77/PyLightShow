import numpy as np
import pygame


class BaseLight:
    def __init__(self, name, position, size):
        self.is_enabled = True
        self.is_on = False
        self.position = self.left, self.top = position
        self.size = self.width, self.height = size
        self.name = name

    def enable(self, enabled):
        self.is_enabled = enabled

    def toggle(self):
        self.is_on = not self.is_on

    def set(self, on):
        self.is_on = on

    def draw(self, surface):
        pass


class SingleLight(BaseLight):
    def __init__(self, name, position, size):
        super().__init__(name, position, size)
        self.value_target = 0.0
        self.value_current = 0.0
        self.value_range = self.value_min, self.value_max = 0.0, 1.0  # not yet implemented
        self.damping = 0.3
        self.value_output = 0

    def set(self, value, damped=True):
        self.value_target = np.clip(value, self.value_min, self.value_max)
        if not damped:
            self.value_current = np.clip(value, self.value_min, self.value_max)

    def update(self):
        self.value_output = int(self.value_current * 255.0)
        self.value_current = self.value_current + self.damping * (self.value_target - self.value_current)

    def draw(self, surface):
        pygame.draw.rect(surface, (self.value_output, self.value_output, self.value_output),
                         (self.position, self.size))


class MultiLight(BaseLight):
    def __init__(self, name, position, size, channels=3):
        super().__init__(name, position, size)
        self.value_target = np.zeros(channels)
        self.value_current = np.zeros(channels)
        self.value_range = self.value_min, self.value_max = np.zeros(channels), np.ones(channels)
        self.damping = 0.3
        self.value_output = np.zeros(channels, dtype=np.int)

    def set(self, value, damped=True):
        self.value_target = np.clip(value, self.value_min, self.value_max)
        if not damped:
            self.value_current = np.clip(value, self.value_min, self.value_max)

    def update(self):
        self.value_output = (self.value_current * 255.0).astype(int)
        self.value_current = self.value_current + self.damping * (self.value_target - self.value_current)
        print(self.name, end='\t')
        print(self.value_output)

    def draw(self, surface):
        pygame.draw.rect(surface, self.value_output, (self.position, self.size))
