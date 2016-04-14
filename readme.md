Porting lightshow over to python.

Project Milestones:
    - Set up sound input.
    - Set up GUI in PyGame.
    - Port basic beat onset detection algorithm.
    - Extend beat detection with FFT.
    - Port lighting control.
    - Optimise with Cython/Numba to run fast enough on Raspberry Pi 2.

Possible future goals:
    - Extend for MIDI IO.
    - Extend for DMX IO.
    - Extend for nRF24L01.
    - Allow for multiple channels.
    - Add BPM detection.
    - Control from mobile app.
    - More intelligent beat detection.
    - Detection of more large scale features e.g.:
        - Song change.
        - Break downs.
        - Phrases.
        - Drops.

External Python module Dependencies:
    - PyGame
    - SoundDevice
    - numpy
    - cython/numba?
    - fftw for python (find out what module this was)
    - pyserial?
    - RPi?