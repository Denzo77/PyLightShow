"""
Handle details of audio input stream.

Could use numpy.fft.rfft and include the hamming window in here to save on importing scipy
"""
import sounddevice as sd
from queue import Queue
import numpy as np
# from scipy import fftpack, signal


DEVICE = None
CHANNELS = 1
SAMPLERATE = 44100.0
BLOCKSIZE = 1024  # gives us a minimum frequency of ~43 Hz
DTYPE = None  # this defaults to float32

queue = Queue()  # For passing audio between files

window = np.hamming(BLOCKSIZE)  # Hamming window for the FFT to give us a sane plot.


def audio_callback(indata, frames, time, status):
    """
    Callback for passing stream to main loop. This runs in a separate thread.

    Additionally calculates an FFT and bins it into octaves.

    :param indata: Audio stream in.
    :type indata: Numpy array of type DTYPE and size BLOCKSIZE
    :param frames: Not used.
    :param time:   Not Used.
    :param status:
    """
    if status:
        print(status, flush=True)
    if any(indata):  # not sure if this is needed.
        temp = np.abs(np.fft.rfft((indata[:, 0] * window)))  # window data, get FFT find absolute.
        temp = np.power(temp, 2)  # We are interested in signal power so we square it.
        outdata = np.zeros(10)
        for i in range(10):  # Binning happens here.
            start_index = 2**i
            stop_index = 2**(i+1)
            outdata[i] = np.sum(temp[start_index:stop_index]) * 1.0e-4
        queue.put(outdata)  # Put in queue for inter thread comms.

# Set up the audio stream
stream = sd.InputStream(device=DEVICE,
                        channels=CHANNELS,
                        samplerate=SAMPLERATE,
                        callback=audio_callback,
                        blocksize=BLOCKSIZE)




