import sounddevice as sd
from queue import Queue
import numpy as np
from scipy import fftpack


"""
Handle details of audio input stream.
"""
DEVICE = None
CHANNELS = 1
SAMPLERATE = 44100.0
BLOCKSIZE = 1024
DTYPE = None

queue = Queue()  # For passing audio between files


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
        outdata = np.abs(fftpack.fft(indata))
    # outdata = np.power(fftpack.rfft(indata), 2)
    # outdata = np.zeros(10)
    # for i in range(10):
    #     index1 = 2**i
    #     index2 = 2**(i+1)
    #     outdata[i] = np.sum(indata[index1:index2]) / (index2-index1)
    #     # outdata[i] = np.sum(indata[2**i:2**(i+1)])
    # queue.put(outdata)
        queue.put(indata)

stream = sd.InputStream(device=DEVICE,
                        channels=CHANNELS,               # Set up the audio stream
                        samplerate=SAMPLERATE,
                        callback=audio_callback,
                        blocksize=BLOCKSIZE)




# import numpy as np
# import matplotlib.pyplot as plt
# import scipy.fftpack
#
# # Number of samplepoints
# N = 600
# # sample spacing
# T = 1.0 / 800.0
# x = np.linspace(0.0, N*T, N)
# y = np.sin(50.0 * 2.0*np.pi*x)
# plt.plot(x, y)
# yf = scipy.fftpack.rfft(y)
# xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
#
# fig, ax = plt.subplots()
# ax.plot(xf, 2.0/N * np.abs(yf[:N/2]))
# plt.show()