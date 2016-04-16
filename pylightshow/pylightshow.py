#!/usr/bin/env python3
import sound_input as sound
from pybeatdetect import GuiBeatDetect
import numpy as np
from queue import Empty
import pygame

# GUI
pygame.init()
clock = pygame.time.Clock()
size = width, height = 1024, 768
screen = pygame.display.set_mode(size)
COLOUR_BACKGROUND = (40, 40, 40)

bar_width = 40

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
    b = GuiBeatDetect(average_weight=0.8, sensitivity_grad=-2.0e-8, sensitivity_offset=1.01, cutoff=0.001,
                        x_pos=(width-bar_width)/2, y_pos=height-40, width=bar_width, y_scale=2000)
    while True:
        val = update()
        if val is not None:
            b.update(val)
        screen.fill(COLOUR_BACKGROUND)
        b.draw(screen, b)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    sound.stream.start()
    main()
    sound.stream.stop()
