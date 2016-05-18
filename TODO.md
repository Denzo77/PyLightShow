## Project Milestones:
1. [x] Set up sound input.
2. [ ] Set up visuals in PyGame.
    - [x] Beat detection GUI.
    - [x] Lighting GUI.
    - [ ] Sound card selection etc (low priority).
3. [ ] Set up GUI in PyGame.
    - [ ] Beat detection GUI.
    - [ ] Lighting GUI.
    - [ ] Sound card selection etc (low priority).
4. [x] Port basic beat onset detection algorithm.
5. [x] Extend beat detection with FFT.
6. [ ] Port lighting control.
    - [x] Light objects
    - [ ] Method of saving state (JSON?).
    - [ ] Scene Manager.
    - [ ] Serial connections.
7. [ ] Optimise with Cython/Numba to run fast enough on Raspberry Pi 2 (low priority).
8. [ ] Move to using OpenGL/OpenGLES (low priority).
9. [ ] Write tests.
10. [ ] Fill in setup.py

## Bugs:
1. [x] Issues with drawing at 60 Hz - Make update return None when queue is empty + reduced framerate to 30.
2. [ ] ~~Find alternative to queue for getting data from callback~~
3. [x] Random level changes on spectrogram - related to (2) - See (1)
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
- More GUI stuff:
    - Move each type to it's own surface and switch to update way instead of redrawing everything.