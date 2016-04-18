"""
Simple classes for controlling lights.

Todo:
- Work out what is going on with is_enabled and is_on
- Way of enabling lights (linked to above)
- How do lights respond to being clicked on?
- Go over documentation
- Print name of light.
- Find out how to use PyGame color class
- __call__, __eq__ and __get__
"""
import numpy as np
import pygame


class BaseLight:
    """
    Base class for lights.
    This handles the position, size and whether the light is switched on.
    """
    def __init__(self, name, position, size):
        """

        :param name: Identifier for this light. Gets printed below the light.
        :param position: Position of top left corner as tuple (left, top).
        :param size: Size of the light as tuple (width, height).
        """
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
    """
    Light object that supports a single channel (i.e. grayscale).
    """
    def __init__(self, name, position, size):
        """

        :param name: Identifier for this light. Gets printed below the light.
        :param position: Position of top left corner as tuple (left, top).
        :param size: Size of the light as tuple (width, height).
        """
        super().__init__(name, position, size)
        self.value_target = 0.0
        self.value_current = 0.0
        self.value_range = self.value_min, self.value_max = 0.0, 1.0  # not yet implemented
        self.damping = 0.3
        self.value_output = 0

    def set(self, value, damped=True):
        """
        Set value to change to.
        This only sets the internal targets. value_output is only calculated after update() is called.
        :param value: Value between 0.0 and 1.0 to set light to.
        :param damped: Whether to smooth the change. If False, the light will immediately jump to the new value when
        update() is called.
        :return: None
        """
        self.value_target = np.clip(value, self.value_min, self.value_max)
        if not damped:
            self.value_current = np.clip(value, self.value_min, self.value_max)

    def update(self):
        """
        Updates value_output and value_current.
        value_current is updated after value_output is set so it's new value will not be seen until update() is next
        called.
        :return: None
        """
        self.value_output = int(self.value_current * 255.0)
        self.value_current = self.value_current + self.damping * (self.value_target - self.value_current)

    def draw(self, surface):
        """
        Draws the light onto a surface
        :param surface: The surface to draw the light onto.
        :return: None
        """
        pygame.draw.rect(surface, (self.value_output, self.value_output, self.value_output),
                         (self.position, self.size))


# class MultiLight(BaseLight):
#     """
#     Light object that supports a multiple channels (i.e. RGB).
#     WARNING: Although this class can take channel values other than 3, this may cause errors if draw() is called.
#     """
#     def __init__(self, name, position, size, channels=3):
#         """
#
#         :param name: Identifier for this light. Gets printed below the light.
#         :param position: Position of top left corner as tuple (left, top).
#         :param size: Size of the light as tuple (width, height).
#         :param channels: Number of channels the light has. Defaults to 3 for RGB.
#         """
#         super().__init__(name, position, size)
#         self.value_target = np.zeros(channels)
#         self.value_current = np.zeros(channels)
#         self.value_range = self.value_min, self.value_max = np.zeros(channels), np.ones(channels)
#         self.damping = 0.3
#         self.value_output = np.zeros(channels, dtype=np.int)
#
#     def set(self, value, damped=True):
#         """
#         Set value to change to.
#         This only sets the internal targets. value_output is only calculated after update() is called.
#         :param value: Values between 0.0 and 1.0 to set light to.
#         :type value: numpy float array of size channels.
#         :param damped: Whether to smooth the change. If False, the light will immediately jump to the new value when
#         update() is called.
#         :return: None
#         """
#         self.value_target = np.clip(value, self.value_min, self.value_max)
#         if not damped:
#             self.value_current = np.clip(value, self.value_min, self.value_max)
#
#     def update(self):
#         """
#         Updates value_output and value_current.
#         value_current is updated after value_output is set so it's new value will not be seen until update() is next
#         called.
#         :return: None
#         """
#         self.value_output = (self.value_current * 255.0).astype(int)
#         self.value_current = self.value_current + self.damping * (self.value_target - self.value_current)
#
#     def draw(self, surface):
#         """
#         Draws the light onto a surface
#         WARNING: Do not call this if channels is not 3.
#         :param surface: The surface to draw the light onto.
#         :return: None
#         """
#         pygame.draw.rect(surface, self.value_output, (self.position, self.size))
