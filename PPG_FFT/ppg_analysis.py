import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft, ifft

# import data
filename = input("Enter data file name:  ")
data_df = pd.read_csv(filename)

# remove DC offset from PPG data
data_df['PPG'] = data_df['PPG'] - data_df['PPG'].mean()
print(data_df['PPG'].mean())

# plot raw data
fig = plt.figure(figsize=[20,20])
ax_1 = fig.add_subplot(211)
ax_1.set_title('Raw Data (DC offset removed)')
ax_1.set_ylabel('PPG Data (amplitude)')
ax_1.plot(data_df['PPG'])
ax_2 = ax_1.twinx()
ax_2.set_ylabel('sample_freq (Hz)', color='red')
ax_2.set_ylim(0, max(data_df['sample_freq'])*1.1)
ax_2.plot(data_df['sample_freq'], color='red')

# calculate FFT
fft_PPG = fft(data_df['PPG'])
fft_y = np.abs(fft_PPG)
sample_rate = 50
N = len(fft_PPG)
n = np.arange(N)
T = N/sample_rate
freq = n/T 

# clunky bandpass filter using FFT data
min_freq = 0.5
max_freq = 10
x_data, y_data = np.array([]), np.array([])
for i in range(len(freq)):
    if min_freq <= freq[i] <= max_freq:
        x_data = np.append(x_data, freq[i])
        y_data = np.append(y_data, fft_y[i])

# Get BPM
bpm_freq = x_data[y_data.argmax()]
bpm_point = np.array([bpm_freq, max(y_data)])

# plot fft
ax_3 = fig.add_subplot(212)
ax_3.set_title('FFT')
ax_3.set_xlabel('freq')
ax_3.plot(x_data, y_data)
ax_3.scatter(*bpm_point, facecolor='limegreen', edgecolor='black', s=100, zorder=3)
ax_3.annotate("BPM: %.1f" % (60*bpm_freq), bpm_point, xytext=[bpm_point[0]*1.07, bpm_point[1]*0.95], fontsize=13)

plt.show()
