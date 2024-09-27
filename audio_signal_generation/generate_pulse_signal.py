import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

def generate_pulse_signal(A, f, DC, T, n, save_graph=False):
    """
    Generate a pulse signal with a specified amplitude, duration, sampling frequency, and duty cycle.

    Parameters:
    -----------
    A : float
        Amplitude of the pulse signal.
    f : int
        Sampling frequency in Hz (samples per second).
    DC : float
        Duty cycle of the signal as a fraction (0 to 1). Represents the proportion of the signal that is "on".
    T : float
        Unit pulse period.
    n : int
        Number of repetitions of the pulse to add.
    save_graph : bool, optional
        If True, displays the pulse signal graph. Default is False.
    
    Returns:
    --------
    signal : numpy.ndarray
        Array containing the pulse signal. The signal has a value of `A` for the duration of the pulse (based on the duty cycle)
        and a value of 0 for the remaining duration.
    
    time : numpy.ndarray
        Array of time values corresponding to each sample point.
    """
    # Total number of samples
    total_samples = int(f * n * T)
    
    # Pulse width in samples (duration for which the pulse is high)
    pulse_width = int(total_samples * DC)
    
    # Create the signal array and set pulse values to amplitude A
    signal = np.zeros(total_samples)
    for i in range(len(signal)):
      signal[ 0 + T*i*f : pulse_width + T*i*f ] = A
    
    # Generate the time array (corresponding to each sample)
    time = np.linspace(0, n*T, total_samples, endpoint=False)
    
    # Plot the signal if show_graph is True
    if save_graph:
        plt.plot(time, signal)
        plt.title(f'Pulse Signal (A={A}, t={T*n}s, f={f}Hz, DC={DC*100}%, T={T}s)')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.grid(True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        directory = 'audio_files'
        filename = os.path.join(directory, f'image_pulse_signal_{timestamp}.png')
        plt.savefig(filename)
    
    return signal, time