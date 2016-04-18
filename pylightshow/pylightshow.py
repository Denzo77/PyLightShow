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
# light = pylights.SingleLight('flashy', (600, 50), (100, 100))
# light2 = pylights.SingleLight('bass', (600, 200), (100, 100))
# light3 = pylights.MultiLight('colour', (600, 350), (100, 100))
lights = [pylights.SingleLight('many ' + str(x), (600, 50 + x * 150), (100, 100)) for x in range(4)]
print(lights[0].name, end='\t')
print(lights[0].position)


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
        # temp1 = b.dBFS(b.vol_average[1]) * 0.01 + 1.0
        # temp2 = b.dBFS(b.vol_average[3]) * 0.01 + 1.0
        # temp3 = b.dBFS(b.vol_average[6]) * 0.01 + 1.0
        # light2.set(max(temp1 + 1.0, 0.0))
        # temparray = np.maximum(np.array([temp1, temp2, temp3]), 0.0)
        # light3.set(temparray)
        if b.beat[1]:
            [lights[x].set(1.0, False) for x in range(len(lights))]
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
        # light.update()
        # light2.update()
        # light3.update()
        # light.set(0.0)
        [lights[x].update() for x in range(len(lights))]
        [lights[x].set(0.0) for x in range(len(lights))]
        block = False
        # Only draw every other frame (30 Hz) to reduce artifacts.
        draw_frame = not draw_frame
        if draw_frame:
            screen.fill(COLOUR_BACKGROUND)
            b.draw(screen)
            [lights[x].draw(screen) for x in range(len(lights))]
            # light.draw(screen)
            # light2.draw(screen)
            # light3.draw(screen)
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
