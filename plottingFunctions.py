### Plotting Function Definitions

import numpy as np
import librosa
from scipy import signal

def plot_spectrogram(y, sr, fig, ax, n_fft_ms, hop_length_ms, y_scale, 
                    amplitude, vmin, vmax, cmap = 'viridis', title=None):
    """Plot a spectrogram with specified frequency and amplitude scaling.

    Parameters:
    -----------
    y : np.ndarray
        Audio signal
    sr : int
        Sample rate in Hz
    fig : matplotlib.figure.Figure
        Figure object for the plot
    ax : matplotlib.axes.Axes
        Axes object to plot on
    n_fft_ms : int
        FFT window size in milliseconds
    hop_length_ms : int
        Number of milliseconds between successive frames
    y_scale : {'linear', 'log'}
        Frequency axis scaling:
        - 'linear': Shows 0-2000 Hz with linear spacing, ticks every 100 Hz
        - 'log': Shows 20-min(20000, sr/2) Hz with logarithmic spacing
    amplitude : {'db', 'linear'}
        Amplitude scaling:
        - 'db': Shows amplitude in decibels, normalized to max
        - 'linear': Shows amplitude normalized to range 0-1
    vmin : float
        Minimum value for color scaling
    vmax : float
        Maximum value for color scaling
    cmap : str, optional
        Matplotlib colormap name (default: 'viridis')
    title : str, optional
        Plot title (default: None). If not provided, describes the scale types.
    """

    
    # Convert ms to samples
    n_fft = int(n_fft_ms * sr / 1000)
    hop_length = int(hop_length_ms * sr / 1000)
    
    # Compute STFT
    D = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))
    
    # Apply amplitude scaling
    if amplitude == 'db':
        D = librosa.amplitude_to_db(D, ref=np.max)  # Reference to max for consistent scaling
        colorbar_format = '%+2.f dB'
    else:
        # Normalize linear amplitude to 0-1 range
        D = D / np.max(np.abs(D))
        colorbar_format = '%.2f'
    
    # Plot spectrogram
    img = librosa.display.specshow(D, y_axis=y_scale, x_axis='time', 
                                 hop_length=hop_length, sr=sr, ax=ax,
                                 cmap=cmap, vmin=vmin, vmax=vmax)
    
    # Configure frequency axis
    ax.tick_params(axis='y', which='minor', left=False)
    nyquist = sr/2
    
    if y_scale == 'linear':
        ax.set_ylim(0, 5000)
        ax.set_yticks(range(0, 5100, 200))
    else:  # log scale
        if nyquist > 20000:
            ax.set_ylim(20, 20000)
            ax.set_yticks([20, 50, 100, 200, 300, 500, 1000, 2000, 3000, 5000, 10000, 20000])
        else:
            ax.set_ylim(20, nyquist)
            ax.set_yticks([20, 50, 100, 200, 300, 500, 1000, 2000, 3000, 5000, 7000, nyquist])
    
    # Set title
    plot_type = f"{'Linear' if y_scale=='linear' else 'Log'}-freq, {'dB' if amplitude=='db' else 'Linear'}-amplitude"
    ax.set_title(title if title else f"{plot_type} spectrogram", pad=15)
    
    # Add colorbar
    fig.colorbar(img, ax=ax, format=colorbar_format)
def plot_spectrogram_subtraction(y1, y2, sr, fig, ax, n_fft_ms, hop_length_ms, y_scale, amplitude, vmin, vmax, title1, title2, cmap = 'RdBu_r'):

    """Plot a spectrogram with specified frequency and amplitude scaling.
    
    Parameters:
    -----------
    x : np.ndarray
    audio 2
    y : np.ndarray
        Audio signal
    sr : int
        Sample rate in Hz
    fig : matplotlib.figure.Figure
        Figure object for the plot
    ax : matplotlib.axes.Axes
        Axes object to plot on
    n_fft_ms : int, optional
        FFT window size in milliseconds (default: 100)
    hop_length_ms : int, optional
        Number of milliseconds between successive frames (default: 1)
    y_scale : {'linear', 'log'}, optional
        Frequency axis scaling (default: 'linear')
        - 'linear': Shows 0-2000 Hz with linear spacing
        - 'log': Shows 20-20000 Hz with logarithmic spacing
    amplitude : {'db', 'linear'}, optional
        Amplitude scaling (default: 'db')
        - 'db': Shows amplitude in decibels (-80 to 0 dB)
        - 'linear': Shows normalized linear amplitude (0 to 1)
    title : str, optional
        Plot title (default: None)
    """
    
    
    # Convert ms to samples
    n_fft = int(n_fft_ms * sr / 1000)
    hop_length = int(hop_length_ms * sr / 1000)
    
    # Compute STFT
    D1 = np.abs(librosa.stft(y1, n_fft=n_fft, hop_length=hop_length))
    D2 = np.abs(librosa.stft(y2, n_fft=n_fft, hop_length=hop_length))
        
    
    # Apply amplitude scaling
    if amplitude == 'db':
        D = (librosa.amplitude_to_db(D1, ref=np.max) - librosa.amplitude_to_db(D2, ref=np.max))   # Reference to max for consistent scaling
        colorbar_format = '%+2.f dB'
    else:
        # Normalize linear amplitude to 0-1 range
        # D = D / np.max(np.abs(D))
        D = D1 - D2
        colorbar_format = '%.2f'
    
    # Plot spectrogram
    img = librosa.display.specshow(D, y_axis=y_scale, x_axis='time', 
                                 hop_length=hop_length, sr=sr, ax=ax,
                                 cmap=cmap, vmin=vmin, vmax=vmax)
    
    # Configure frequency axis
    ax.tick_params(axis='y', which='minor', left=False)
    nyquist = sr/2
    
    if y_scale == 'linear':
        ax.set_ylim(0, 5000)
        ax.set_yticks(range(0, 5100, 200))
    else:  # log scale
        if nyquist > 20000:
            ax.set_ylim(20, 20000)
            ax.set_yticks([20, 50, 100, 200, 300, 500, 1000, 2000, 3000, 5000, 10000, 20000])
        else:
            ax.set_ylim(20, nyquist)
            ax.set_yticks([20, 50, 100, 200, 300, 500, 1000, 2000, 3000, 5000, 7000, nyquist])
    
    # Set title
    plot_type = f"{'Linear' if y_scale=='linear' else 'Log'}-freq, {'dB' if amplitude=='db' else 'Linear'}-amplitude"
    ax.set_title(f"Spectral Subtraction: \n {title1} - {title2}", pad=15)
    
    # Add colorbar    
    cbar = fig.colorbar(img, ax=ax, format=colorbar_format)
    
    # Add text at top and bottom of colorbar using the colorbar object
    cbar.ax.text(1.5, 1.1, f'{title1} leads', 
                 ha='left', va='bottom', transform=cbar.ax.transAxes)
    cbar.ax.text(1.5, -0.1, f'{title2} leads', 
                 ha='left', va='top', transform=cbar.ax.transAxes)


def plot_spectrogram_subtraction_onesided(y1, y2, sr, fig, ax, n_fft_ms, hop_length_ms, y_scale, amplitude, vmin, vmax, title1, title2, y1Leads, cmap = 'RdBu_r'):

    """Plot a spectrogram with specified frequency and amplitude scaling.
    
    Parameters:
    -----------
    x : np.ndarray
    audio 2
    y : np.ndarray
        Audio signal
    sr : int
        Sample rate in Hz
    fig : matplotlib.figure.Figure
        Figure object for the plot
    ax : matplotlib.axes.Axes
        Axes object to plot on
    n_fft_ms : int, optional
        FFT window size in milliseconds (default: 100)
    hop_length_ms : int, optional
        Number of milliseconds between successive frames (default: 1)
    y_scale : {'linear', 'log'}, optional
        Frequency axis scaling (default: 'linear')
        - 'linear': Shows 0-2000 Hz with linear spacing
        - 'log': Shows 20-20000 Hz with logarithmic spacing
    amplitude : {'db', 'linear'}, optional
        Amplitude scaling (default: 'db')
        - 'db': Shows amplitude in decibels (-80 to 0 dB)
        - 'linear': Shows normalized linear amplitude (0 to 1)
    title : str, optional
        Plot title (default: None)
    """
    
    
    # Convert ms to samples
    n_fft = int(n_fft_ms * sr / 1000)
    hop_length = int(hop_length_ms * sr / 1000)
    
    # Compute STFT
    D1 = np.abs(librosa.stft(y1, n_fft=n_fft, hop_length=hop_length))
    D2 = np.abs(librosa.stft(y2, n_fft=n_fft, hop_length=hop_length))
        
    
    # Apply amplitude scaling
    if amplitude == 'db':
        D = (librosa.amplitude_to_db(D1, ref=np.max) - librosa.amplitude_to_db(D2, ref=np.max))   # Reference to max for consistent scaling
        colorbar_format = '%+2.f dB'
    else:
        D = D1 - D2
        colorbar_format = '%.2f'
        

    ########################
    # MAKE IT ONE SIDED!!!
    ########################
    if y1Leads:
            D = np.where(D < 0, 0, D)
    else:
            D = np.where(D > 0, 0, D)    
    ########################
    ########################
    ########################
        
        
    # Plot spectrogram
    img = librosa.display.specshow(D, y_axis=y_scale, x_axis='time', 
                                 hop_length=hop_length, sr=sr, ax=ax,
                                 cmap=cmap, vmin=vmin, vmax=vmax)
    
    # Configure frequency axis
    ax.tick_params(axis='y', which='minor', left=False)
    nyquist = sr/2
    
    if y_scale == 'linear':
        ax.set_ylim(0, 5000)
        ax.set_yticks(range(0, 5100, 200))
    else:  # log scale
        if nyquist > 20000:
            ax.set_ylim(20, 20000)
            ax.set_yticks([20, 50, 100, 200, 300, 500, 1000, 2000, 3000, 5000, 10000, 20000])
        else:
            ax.set_ylim(20, nyquist)
            ax.set_yticks([20, 50, 100, 200, 300, 500, 1000, 2000, 3000, 5000, 7000, nyquist])
    
    # Set title
    plot_type = f"{'Linear' if y_scale=='linear' else 'Log'}-freq, {'dB' if amplitude=='db' else 'Linear'}-amplitude"
    if y1Leads:
        ax.set_title(f"Spectral Subtraction: \n {title1} bigger", pad=15)
    else:
        ax.set_title(f"Spectral Subtraction: \n {title2} bigger", pad=15)
    
    # Add colorbar    
    cbar = fig.colorbar(img, ax=ax, format=colorbar_format)
    
    # Add text at top and bottom of colorbar using the colorbar object
    cbar.ax.text(1.5, 1.1, f'{title1} leads', 
                 ha='left', va='bottom', transform=cbar.ax.transAxes)
    cbar.ax.text(1.5, -0.1, f'{title2} leads', 
                 ha='left', va='top', transform=cbar.ax.transAxes)
    
    
    
def plot_spectrum(y, sr, fig, ax, title=None):
    """Plot magnitude spectrum with frequency axis in Hz."""
    
    # Perform FFT and calculate amplitude
    ft = np.fft.rfft(y)  # Already gives just the positive frequencies
    freqs = np.fft.rfftfreq(len(y), 1/sr)  # Frequencies for rfft
    magnitude_spectrum = np.abs(ft)  # No need to slice
    
    # Convert magnitude to decibels
    magnitude_db = librosa.amplitude_to_db(magnitude_spectrum, ref=np.max)
    
    # Plot the spectrum
    img = ax.plot(freqs, magnitude_db)
    
    # Set log scale and ticks
    ax.set_xscale('log')
    ax.tick_params(axis='x', which='minor', bottom=False)
    ax.grid(True, which='major', linestyle='-', alpha=0.3)

    if (20000 < (sr/2)):
        ax.set_xlim(20, 20000)
        ticks = [20, 50, 100, 200, 300, 500, 1000, 2000, 3000, 5000, 10000, 20000]
        ax.set_xticks(ticks)
        ax.set_xticklabels(ticks)    
    else:
        ax.set_xlim(20, sr/2)
        ticks = [20, 50, 100, 200, 300, 500, 1000, 2000, 5000, sr/2]
        ax.set_xticks(ticks)
        ax.set_xticklabels(ticks) 

    
    ax.set_ylim(-80, 0)  

    
    # Labels
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Amplitude (dB)')
    if title:
        ax.set_title(f"Spectrum: {title}", pad=15) 
    else:
        ax.set_title('Spectrum', pad=15) 
        
        


def plot_time(y, sr, fig, ax, color='#1f77b4', title=None):
    """Plot time-domain signal with improved visualization."""
    # Create time axis in seconds
    times = np.arange(len(y)) / sr
    
    # Plot the waveform
    ax.plot(times, y, color, linewidth=0.75)  # Thinner line for better detail
    
    # Set title and labels 
    if title:
        ax.set_title(f"Waveform: {title}", pad=15)    
    else:
        ax.set_title('Waveform', pad=15)    
        
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    
    # Add grid for better readability
    ax.grid(True, alpha=0.2)
    
    # Set y-axis limits symmetrically based on the signal
    max_amp = np.max(np.abs(y))
    ax.set_ylim(-max_amp, max_amp)
    ax.set_xlim(0, times[-1])

    
def plot_csd(x, y, sr, fig, ax1, ax2, title=None):
    """Plot cross-spectral density magnitude and phase with frequency axis in Hz."""
    
    # Compute CSD using scipy.signal
    f, Pxy = signal.csd(x, y, fs=sr, scaling='density', nperseg=4096)
    
    # Plot magnitude spectrum
    ax1.semilogy(f, np.abs(Pxy))
    ax1.set_xscale('log')
    ax1.tick_params(axis='x', which='minor', bottom=False)
    ax1.grid(True, which='major', linestyle='-', alpha=0.3)
    
    # Plot phase spectrum
    ax2.plot(f, np.angle(Pxy, deg=True))  # deg=True converts to degrees
    ax2.set_xscale('log')
    ax2.tick_params(axis='x', which='minor', bottom=False)
    ax2.grid(True, which='major', linestyle='-', alpha=0.3)
    
    # Set frequency limits and ticks
    for ax in [ax1, ax2]:
        if (20000 < (sr/2)):
            ax.set_xlim(20, 20000)
            ticks = [20, 50, 100, 200, 300, 500, 1000, 2000, 3000, 5000, 10000, 20000]
        else:
            ax.set_xlim(20, sr/2)
            ticks = [20, 50, 100, 200, 300, 500, 1000, 2000, 5000, sr/2]
        ax.set_xticks(ticks)
        ax.set_xticklabels(ticks)

    # Labels
    ax1.set_ylabel('CSD Magnitude')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Phase (degrees)')
    
    if title:
        ax1.set_title(f"CSD: {title}", pad=15)
    else:
        ax1.set_title('Cross-spectral Density', pad=15)