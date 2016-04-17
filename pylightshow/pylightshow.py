#!/usr/bin/env python3
import sound_input as sound
from pybeatdetect import PlotBeatDetect
# from pybeatdetect import SimpleBeatDetect
import numpy as np
from queue import Empty
import pygame
import sys

# GUI
pygame.init()
clock = pygame.time.Clock()
size = width, height = 1600, 768
screen = pygame.display.set_mode(size, pygame.HWSURFACE)
COLOUR_BACKGROUND = (30, 30, 30)

bar_width = 40


def update(block):
    """
    Calculations are done in this. Intended for future abstraction.
    Currently has a test function.
    :return: RMS value of audio_buf. Doubled to scale to +-1
    """
    # get audio out of queue
    audio_buf = np.zeros(10)
    try:
        audio_buf = sound.queue.get(block=block)
    except Empty:
        return None
    # # process (temporarily calculating RMS)
    # audio_buf = np.power(audio_buf, 2)
    # audio_buf = np.mean(audio_buf)
    # rms = 2 * np.sqrt(audio_buf)
    # return rms
    return audio_buf


def main():  # This is the main loop
    sound.stream.start()
    b = PlotBeatDetect(average_weight=0.3, sensitivity_grad=-2.0e-4, sensitivity_offset=1.4, cutoff=0.001,
                       position=(100, 40), size=(400, 700))
    # b = SimpleBeatDetect(average_weight=0.1, sensitivity_grad=-2.0e-2, sensitivity_offset=1.4, cutoff=0.001)
    block = True
    draw_frame = True
    while True:
        draw_frame = not draw_frame
        val = update(block)
        if val is not None:
            block = False
            b.update(val)
        if draw_frame:
            screen.fill(COLOUR_BACKGROUND)
            b.draw(screen)
            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sound.stream.stop()
                pygame.quit()
                sys.exit
        clock.tick(60)


if __name__ == "__main__":
    main()
