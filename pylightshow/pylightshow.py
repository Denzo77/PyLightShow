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

# GUI
pygame.init()
clock = pygame.time.Clock()
size = width, height = 800, 768
screen = pygame.display.set_mode(size, pygame.HWSURFACE)
COLOUR_BACKGROUND = (30, 30, 30)

bar_width = 40

# beats and lights
b = PlotBeatDetect(average_weight=0.3, sensitivity_grad=-2.0e-4, sensitivity_offset=1.4, cutoff=0.001,
                   position=(100, 40), size=(400, 700))

light_names = ['light ' + str(x) for x in range(4)]
light_pos = [50 + x * 150 for x in range(len(light_names))]  # these expressions can be safely replaced with nicer ones.
light_size = [100 for x in range(len(light_names))]
lights = pylights.SingleLight(light_names, [600 for x in range(len(light_names))], light_pos, light_size, light_size)
[print(lights.name[x] + '\t' + str(lights.top[x])) for x in range(len(lights.name))]  # print names of lights


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
    pass


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
        b.update(sound.queue.get(block=block))
        if b.beat[1]:
            val = np.empty(4)
            val.fill(0.1)
            lights.fade(val)
            val.fill(0.8)
            lights.fade(val)
    except Empty:
        return None


def main():  # This is the main loop
    sound.stream.start()

    block = True
    draw_frame = True
    while True:
        # Only update stuff that depends on audio if buffer in queue.
        update_audio(block)
        # We want these to run independent of sound input (lights carry on fading even if stream is interrupted)
        lights.update()
        if lights.value_current[0] > 0.75:
            lights.fade(np.zeros(4))
        block = False
        # Only draw every other frame (30 Hz) to reduce artifacts.
        draw_frame = not draw_frame
        if draw_frame:
            screen.fill(COLOUR_BACKGROUND)
            b.draw(screen)
            lights.draw(screen)
            pygame.display.flip()
        # Events loop.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sound.stream.stop()
                pygame.quit()
                sys.exit
        clock.tick(60)


if __name__ == "__main__":
    main()
