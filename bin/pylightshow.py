#!/usr/bin/env python3

import numpy as np
import sounddevice as sd
from queue import Queue, Empty


# Global Variables:
queue = Queue()


# This is called from another thread once audio buffer is filled
def audio_callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    queue.put(indata)

# Audio in object
audio_stream = sd.InputStream(channels=1, samplerate=44100.0, callback=audio_callback)


# All calculations are performed here
def update():
    audio_buf = queue


# Setup is done in here
def setup():
    audio_stream.start()


# Stuff to do when exiting
def end_program():
    audio_stream.close()


# Main loop
def main():
    while True:
        update()


if __name__ == "__main__":
    main()
