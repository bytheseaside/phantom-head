from open_bci_v3 import OpenBCIBoard
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.fft import rfft, rfftfreq
from scipy.signal import butter, lfilter, iirnotch, filtfilt
from Fps import Fps
from datetime import datetime
import sys
import argparse

import random
import threading

def beep(n):
    if n == 0:
      print("done")
      file.close()
      return
    handle_sample({'channel_data': [random.randint(-20000,20000)]})
    threading.Timer(0.5, beep, args=(n-1,)).start()

def plot_spectrum(N, series, fs):
  yf = rfft(series)
  xf = rfftfreq(N, 1/fs)

  plt.figure(figsize=(14,7))
  plt.title('Frequency Spectrum')
  plt.plot(xf, np.abs(yf), color='green')
  plt.ylabel('Amplitude')
  plt.xlabel('Freq Hz')
  plt.show()


def notch_filter(series, fs):
  f0 = 50.0
  Q = 30.0
  b, a = iirnotch(f0, Q, fs)
  series = filtfilt( b, a, series)
  return series

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
   # b,a = butter_bandpass(lowcut, highcut, fs, order=order)
   b,a = butter(lowcut, highcut, fs, order=order)
   y = lfilter(b,a,data)
   return y


ffps = Fps()
ffps.tic()
fs = 250.0
data = []
ani = None
file = open(f"output_{datetime.now().strftime('%H:%M:%S')}.txt", "a")  # append mode
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
start_time = None

def handle_sample(sample):
  ffps.steptoc()

  time_difference = datetime.now() - start_time
  total_seconds = int(time_difference.total_seconds())
  hours, remainder = divmod(total_seconds, 3600)
  minutes, seconds = divmod(remainder, 60)

  sample_data = {
    'timestamp': f"{hours:02}:{minutes:02}:{seconds:02}",
    'channel_data': sample['channel_data'][0],
    'fps': ffps.fps
  }

  data.append(sample_data)
  write_to_file(sample_data)

def write_to_file(sample_data):
  file.write(f"{sample_data['timestamp']};{sample_data['fps']};{sample_data['channel_data']}\n")

def update_plot(i, xs, ys):
  last_sample = data[-1]
  xs.append(last_sample['timestamp'])
  ys.append(last_sample['channel_data'])
  xs = xs[-20:]
  ys = ys[-20:]
  ax.clear()
  plt.ylabel('Channel Data')
  plt.xlabel('Time')
  plt.xticks(rotation=45, ha='right')
  ax.set_title('OpenBCI Channel Data')
  ax.plot(xs, ys)


if __name__ == '__main__':
  try:
    parser = argparse.ArgumentParser("test_openbci")
    parser.add_argument("--test", action="store_true", help="Simulate OpenBCI stream.")
    args = parser.parse_args()
    
    file.write("timestamp;fps;channel_data\n")

    if args.test:
      start_time = datetime.now()
      beep(30)
    else:
      board = OpenBCIBoard()
      board.print_register_settings()
      board.get_radio_channel_number()
      print(f'OpenBCI connected to radio channel {board.radio_channel_number}')


    if not args.test:
      board.start()
      start_time = datetime.now()
      board.start_streaming(handle_sample)
    
    ani = animation.FuncAnimation(fig, update_plot, fargs=(xs, ys), interval=1000)
    plt.show()
    
    if not args.test:
      ani.save(f"output_{datetime.now().strftime('%H:%M:%S')}.gif", writer='imagemagick', fps=30)
      board.checktimer.cancel()
      board.disconnect()
      
  except KeyboardInterrupt:
    file.close()