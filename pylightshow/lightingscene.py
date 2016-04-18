"""
Framework for managing what the lights do.

Random Notes:
- All scenes need:
    - buffers in, e.g. audio, midi, osc.
    - buffers out to send stuff out, e.g. serial, dmx512, osc, midi.
- Scenes can share:
    - Lights.
    - Beat onset detectors.
    - GUI elements.
    - Sound streams.
- Each scene needs its own:
    - Name.
    - Setup method.
    - Update method.
    - Draw method.
    - Exit method.
"""


class BaseScene:
    def __init__(self, name):
        self.next = self
        self.name = name

    def process_input(self, events):
        print("You forgot to overide")

    def update(self):
        print("You forgot to overide")

    def draw(self, screen):
        print("You forgot to overide")

    def switch_to_scene(self, next_scene):
        self.next = next_scene


class LightScene(BaseScene):  # class myClass(baseClass): means myClass inherits from baseClass
    """
    Note this class expects a single beats object and a single lights object containing arrays of lights.
    Not convinced this is the best way, but it makes life quicker and easier at this point.
    """
    def __init__(self, name, beats, lights):
        super().__init__(name)
        self.beats = beats
        self.lights = lights

    # def process_input(self, events):

    def update(self):
        self.beats.update()
        self.lights.update()

    def draw(self, screen):
        self.beats.draw()
        self.lights.draw()

