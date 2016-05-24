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

import importlib
import sys
# sys.path.append()  # Location of scenes


# class BaseScene:
#     """
#     A generic scene for building the light show.
#     """
#     def __init__(self, name):
#         self.name = name
#         pass
#
#     def update(self):
#         pass
#
#     def draw(self):
#         pass
#
#
# class GuiScene():
#     """
#     A scene that takes beat detection objects and draws to the GUI
#     """
#     def __init__(self, name):
#         super().__init__(name)
#
#     def update(self, lights):
#
#
# def loadScene(sceneName):
#     """
#     Loads a new scene, ensuring any changes to the source files are brought in.
#     - Will import the scene.
#     - Will reload the scene.
#     :param sceneName: scene to load
#     :return: Reference to scene
#     """
#     importlib.invalidate_caches()
#     scene = importlib.import_module(sceneName)
#     importlib.reload(scene)
#     return scene

# import pylights

class MyScene:
    def __init__(self):
        self.name = "MyScene"

    def update(self, lights):
        for i in range(len(lights)):
            if lights[i].value_target < 1.0:
                lights[i].value_target += 0.01
