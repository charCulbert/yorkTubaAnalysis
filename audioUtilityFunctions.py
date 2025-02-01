
### Utility Function Definitions

import numpy as np


def trim(y, sr, start_seconds, end_seconds):
    # Convert start and end times to samples
    start_sample = int(start_seconds * sr)
    end_sample = int(end_seconds * sr)
    
    # Trim the audio
    y = y[start_sample:end_sample]
    
    return y         


def apply_hann_window_fades(y, sr, FADE_DURATION_SECONDS):
    """
    Apply Hann window to the audio signal
    
    Parameters:
    - y: numpy array of audio samples
    - sr: the samplerate
    - FADE_DURATION_SECONDS: length of the window to apply in s
    
    Returns:
    - windowed audio signal
    """
    
    window_samples = int(FADE_DURATION_SECONDS * sr)


    # Create Hann window
    hann_window = np.hanning(window_samples * 2)
    
    # Split window into fade-in and fade-out
    fade_in = hann_window[:window_samples]
    fade_out = hann_window[window_samples:]
    
    # Apply fade-in to the beginning
    y[:window_samples] *= fade_in
    
    # Apply fade-out to the end
    y[-window_samples:] *= fade_out
    
    return y