#!/usr/bin/env python3
"""
Main script for light show.
"""
import sound_input as sound
from pybeatdetect import PlotBeatDetect
import pylights
import numpy as np
from queue import Empty
import pygame
import sys
import json
import lightingscene

# GUI
pygame.init()
clock = pygame.time.Clock()
size = width, height = 1680, 1200
screen = pygame.display.set_mode(size, pygame.HWSURFACE)
COLOUR_BACKGROUND = (30, 30, 30)

bar_width = 40

# beats and lights
NUMBER_OF_LIGHTS = 6
# b = PlotBeatDetect(average_weight=0.3, sensitivity_grad=-2.0e-4, sensitivity_offset=1.4, cutoff=0.001,
#                    position=(100, 40), size=(400, 700))
beat_pos = [100 + x * 40 for x in range(10)]
beats = [PlotBeatDetect(average_weight=0.3, sensitivity_grad=-2.0e-4, sensitivity_offset=1.4, cutoff=0.001,
                        position=(x, 40), size=(40, 700)) for x in beat_pos]

# Generate lights
light_names = ['light ' + str(x) for x in range(NUMBER_OF_LIGHTS)]
light_pos = [50 + x * 150 for x in range(NUMBER_OF_LIGHTS)]  # these expressions can be safely replaced with nicer ones.
lights = [pylights.SingleLight(light_names[x], 600, light_pos[x], 100, 100) for x in range(NUMBER_OF_LIGHTS)]
[print(lights[x].name + '\t' + str(lights[x].top)) for x in range(NUMBER_OF_LIGHTS)]  # print names of lights


def save_state():
    """
    Saves state.
    This is going to be a pain in the arse...

    Method:
    - Get data:
        - Beat detectors:
            - average_weight
            - sensitivity_grad
            - sensitivity_offset
            - cutoff
            - colours?
        - Lights?:
            - damping
            - is_enabled
        - Screen size & position?
    - Convert numpy arrays into dicts? (maybe use json tricks, or json.encodejson())
    - Concatenate into a set of dicts:
    - Convert to JSON with json.dumps(save_state) (and any other options I may need)
    - Write to a file
    """
    # [print(lights[x].__dict__) for x in range(NUMBER_OF_LIGHTS)]
    # print(b.__dict__)
    # print({'Lights': lights, "Beat Detect": b}.__dict__)
    # Lights = str({"Lights": [lights[x].__dict__ for x in range(NUMBER_OF_LIGHTS)]})
    # BeatDetects = {"BeatDetects": b.__dict__}
    # print(Lights)
    # with open('/home/denzo/lights.JSON', 'w') as output:
    #     foo = json.dumps(Lights)
    #     output.write(foo)



def load_state():
    """
    Load state.

    Method:
    If save file present:
        - Load savestate json file.
        - Load JSON with json.loads(save_state).
        - Extract relevant entries from dict.
        - Decode np arrays.
        - Set data in relevant places.
    Otherwise, start up with default values.
    """
    pass


def update_audio(block):
    """
    Gets next set of values from the queue.
    :return: Array of sound values or None if queue is empty.
    """
    try:
        sound_in = sound.queue.get(block=block)  # todo fix this bit
        [beats[x].update(sound_in[x]) for x in range(len(beats))]
    except Empty:
        print("empty")
        return None


def main():  # This is the main loop
    sound.stream.start()

    block = True
    draw_frame = True
    current_scene = lightingscene.MyScene()
    while True:
        # Only update stuff that depends on audio if buffer in queue.
        update_audio(block)
        # We want these to run independent of sound input (lights carry on fading even if stream is interrupted)
        current_scene.update(lights)
        [lights[x].update() for x in range(NUMBER_OF_LIGHTS)]
        block = False
        # Only draw every other frame (30 Hz) to reduce artifacts.
        draw_frame = not draw_frame
        if draw_frame:
            screen.fill(COLOUR_BACKGROUND)
            [beats[x].draw(screen) for x in range(len(beats))]
            [lights[x].draw(screen) for x in range(NUMBER_OF_LIGHTS)]
            pygame.display.flip()
        # Events loop.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sound.stream.stop()
                save_state()
                pygame.quit()
                sys.exit
        clock.tick(60)


if __name__ == "__main__":
    main()
