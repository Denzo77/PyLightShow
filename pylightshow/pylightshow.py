#!/usr/bin/env python3
import sound_input as sound
from pybeatdetect import BasicBeatDetect
import numpy as np
from queue import Empty
import pygame

# GUI
pygame.init()
clock = pygame.time.Clock()
size = width, height = 1024, 768
screen = pygame.display.set_mode(size)
COLOUR_BACKGROUND = (40, 40, 40)
COLOUR_VOL_INSTANT = (150, 150, 150)
COLOUR_VOL_AVERAGE = (0, 0, 0)

bar_width = 40
bar_vol_instant = pygame.Rect((width-bar_width)/2, height-38, bar_width, 1)
bar_vol_average = pygame.Rect((width-bar_width)/2 + 2, height-40, bar_width-4, 1)


def update():
    """
    Calculations are done in this. Intended for future abstraction.
    Currently has a test function.
    :return:
    """
    # get audio out of queue
    try:
        audio_buf = sound.queue.get(block=True)
    except Empty:
        pass
    # process (temporarily calculating RMS)
    audio_buf = np.power(audio_buf, 2)
    audio_buf = np.mean(audio_buf)
    ms = np.sqrt(audio_buf)
    return ms


def display(vol_instant, vol_average):
    height_instant = int(vol_instant * 2000)
    height_average = int(vol_average * 2000)
    bar_vol_instant.height = -height_instant
    bar_vol_average.height = -height_average
    pygame.draw.rect(screen, COLOUR_VOL_INSTANT, bar_vol_instant)
    pygame.draw.rect(screen, COLOUR_VOL_AVERAGE, bar_vol_average)


def main():  # This is the main loop
    b = BasicBeatDetect(sensitivity_grad=-2.0e-8, sensitivity_offset=1.01, cutoff=0.001)
    while True:
        val = update()
        if val is not None:
            b.update(val)
        screen.fill(COLOUR_BACKGROUND)
        display(b.vol_instant, b.vol_average)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    sound.stream.start()
    main()
    sound.stream.stop()
