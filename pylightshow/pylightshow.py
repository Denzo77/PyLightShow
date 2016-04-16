#!/usr/bin/env python3
import sound_input as sound
from pybeatdetect import BasicBeatDetect
import numpy as np
from queue import Empty
import pygame


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


def main():  # This is the main loop
    b = BasicBeatDetect(sensitivity_grad=0.0, sensitivity_offset=1.0, cutoff=0.001)
    while True:
        val = update()
        b.update(val)
        if b.get():
            print('i')
        else:
            print('o')


if __name__ == "__main__":
    sound.stream.start()
    main()
    sound.stream.stop()
