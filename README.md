# PyLightShow
Porting lightshow over to python.

## Project Milestones:
1. [x] Set up sound input.
2. [ ] Set up GUI in PyGame.
3. [ ] Port basic beat onset detection algorithm.
4. [ ] Extend beat detection with FFT.
5. [ ] Port lighting control.
6. [ ] Optimise with Cython/Numba to run fast enough on Raspberry Pi 2.

## Possible future goals:
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

## External Python module Dependencies:
- PyGame
- SoundDevice
- numpy
- cython/numba?
- fftw for python (find out what module this was)
- pyserial?
- RPi?