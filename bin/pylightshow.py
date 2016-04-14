#!/usr/bin/env python3
import sound_input as sound
import numpy as np
from queue import Empty


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
    ms = np.mean(audio_buf)
    if ms > 0.1:
        print("1")
    else:
        print("o")


def main():  # This is the main loop
    while True:
        update()


if __name__ == "__main__":
    sound.stream.start()
    main()
    sound.stream.stop()
