import sounddevice as sd
from queue import Queue


"""
Handle details of audio input stream.
"""

CHANNELS = 1
SAMPLERATE = 44100.0
BLOCKSIZE = 1024

queue = Queue()  # For passing audio between files


def audio_callback(indata, frames, time, status):
    """
    Callback for passing stream to main loop
    :param indata: Audio stream in np arrays of size blocksize.
    :param frames: Not used.
    :param time:   Not Used.
    :param status:
    :return:
    """
    if status:
        print(status, flush=True)
    queue.put(indata)

stream = sd.InputStream(channels=CHANNELS,               # Set up the audio stream
                        samplerate=SAMPLERATE,
                        callback=audio_callback,
                        blocksize=BLOCKSIZE)
