#!/usr/bin/env python3
import sound_input as sound
from pybeatdetect import GuiBeatDetect
# from pybeatdetect import SimpleBeatDetect
import numpy as np
from queue import Empty
import pygame
import sys

# GUI
pygame.init()
clock = pygame.time.Clock()
size = width, height = 1600, 768
screen = pygame.display.set_mode(size)
COLOUR_BACKGROUND = (30, 30, 30)

bar_width = 40


def update():
    """
    Calculations are done in this. Intended for future abstraction.
    Currently has a test function.
    :return: RMS value of audio_buf. Doubled to scale to +-1
    """
    # get audio out of queue
    try:
        audio_buf = sound.queue.get(block=True)
    except Empty:
        pass
    # # process (temporarily calculating RMS)
    # audio_buf = np.power(audio_buf, 2)
    # audio_buf = np.mean(audio_buf)
    # rms = 2 * np.sqrt(audio_buf)
    # return rms
    return audio_buf


def draw_val(indata):
    indata[:] = indata[:] * 2.0e1
    x = np.arange(100, 100+len(indata))
    offset = height/2
    for i in range(len(indata)):
        pygame.draw.line(screen, (100, 100, 100), (x[i], offset), (x[i], offset-int(indata[i])), 1)


def main():  # This is the main loop
    sound.stream.start()
    b = GuiBeatDetect(average_weight=0.1, sensitivity_grad=-2.0e-3, sensitivity_offset=1.4, cutoff=0.001,
                        left=(width-bar_width)/2, top=40, width=bar_width, height=700)
    # b = SimpleBeatDetect(average_weight=0.1, sensitivity_grad=-2.0e-2, sensitivity_offset=1.4, cutoff=0.001)
    while True:
        val = update()
        if val is not None:
            b.update(val)
            screen.fill(COLOUR_BACKGROUND)
            # b.draw(screen)
            draw_val(val)
            pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sound.stream.stop()
                pygame.quit()
                sys.exit
        # clock.tick(60)


if __name__ == "__main__":
    main()
