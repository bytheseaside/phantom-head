import os
import numpy as np
import scipy.io.wavfile as wvf
from generate_pulse_signal import generate_pulse_signal
from datetime import datetime

MAX_INT16 = 32767

def generate_audio_file(A, f, DC, T, n, save_graph=False):
    """
    Generate a pulse audio file and save it as a WAV file in a specified directory.

    Parameters:
    -----------
    A : float
        Amplitude of the pulse signal (should be between -1 and 1 for audio).
    f : int
        Sampling frequency in Hz (samples per second).
    DC : float
        Duty cycle of the signal as a fraction (0 to 1). Represents the proportion of the signal that is "on".
    T : float
        Unit pulse period.
    n : int
        Number of repetitions of the pulse to add.
    save_graph : bool, optional
        If True, saves the pulse signal graph. Default is False.
    """
    # Define the directory where audio files will be saved
    directory = 'audio_files'
    os.makedirs(directory, exist_ok=True)

    # Generate the pulse signal
    signal, _ = generate_pulse_signal(A, f, DC, T, n, save_graph=save_graph)

    # Scale the signal to the range of int16 for audio
    audio_signal = np.int16(signal / np.max(np.abs(signal)) * MAX_INT16)

    # Create a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(directory, f'pulse_signal_{timestamp}.wav')

    # Save the audio signal to a WAV file
    wvf.write(filename, f, audio_signal)
    
    print(f"Audio file '{filename}' generated successfully.")

# Example of using the function
if __name__ == "__main__":
    A = 1       # Amplitude
    T = 2       # Period of the signal
    f = 1000    # Sampling frequency in Hz
    n = 4       # Number of repetitions of the pulse
    DC = 0.4    # Duty cycle as a fraction (50%)

    # Generate and save the audio file
    generate_audio_file(A, f, DC, T, n, save_graph=True)
