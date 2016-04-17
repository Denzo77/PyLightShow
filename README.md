# PyLightShow
Porting lightshow over to python.

## Project Milestones:
1. [x] Set up sound input.
2. [ ] Set up GUI in PyGame.
    - [x] Beat detection GUI.
    - [ ] Lighting GUI.
    - [ ] Sound card selection etc (low priority).
3. [x] Port basic beat onset detection algorithm.
4. [x] Extend beat detection with FFT.
5. [ ] Port lighting control.
6. [ ] Optimise with Cython/Numba to run fast enough on Raspberry Pi 2 (low priority).
7. [ ] Move to using OpenGL/OpenGLES (whatever the one the RPi 2 can manage was).
8. [ ] Write tests.
9. [ ] Fill in setup.py

## Bugs:
1. [x] Issues with drawing at 60 Hz - Brought it down to 30
2. [ ] Find alternative to queue for getting data from callback (only interested in latest version)
3. [ ] Random level changes on spectrogram - related to (2)?
4. [x] Fix issue with sensitivity becoming a bool. - changed to use np.maximum
5. [x] BaseBeatDetect.beat is not returning an array. - Used np.logical_xxx functions.
6. [ ] Sensitivity does not change adequately.

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
- NumPy
- SciPy

## Possible future dependencies:
- cython/numba?
- pyserial?
- RPi?