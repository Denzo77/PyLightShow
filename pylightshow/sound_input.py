import sounddevice as sd
from queue import Queue
import numpy as np
from scipy import fftpack, signal


"""
Handle details of audio input stream.
"""
DEVICE = 4
CHANNELS = 1
SAMPLERATE = 44100.0
BLOCKSIZE = 1024
DTYPE = None

queue = Queue()  # For passing audio between files

window = signal.hamming(BLOCKSIZE, False)


def audio_callback(indata, frames, time, status):
    """Callback for passing stream to main loop. This runs in a separate thread.
    :param indata: Audio stream in.
    :type indata: Numpy array of type DTYPE and size BLOCKSIZE
    :param frames: Not used.
    :param time:   Not Used.
    :param status:
    """
    if status:
        print(status, flush=True)
    if any(indata):
        # outdata = np.abs(fftpack.fft(indata)[:512, 0])
        # outdata = np.zeros(BLOCKSIZE/2)
        temp = np.abs(fftpack.rfft((indata[:, 0] * window), overwrite_x=True))
        temp = np.power(temp, 2)

        outdata = np.zeros(10)
        for i in range(10):
            index1 = 2**i
            index2 = 2**(i+1)
            outdata[i] = np.sum(temp[index1:index2]) / (index2-index1)
            # outdata[i] = np.sum(indata[2**i:2**(i+1)])
            queue.put(outdata)

stream = sd.InputStream(device=DEVICE,
                        channels=CHANNELS,               # Set up the audio stream
                        samplerate=SAMPLERATE,
                        callback=audio_callback,
                        blocksize=BLOCKSIZE)




