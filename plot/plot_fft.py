# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.fft import fft
# from scipy.signal import windows
# from scipy.signal import savgol_filter, medfilt

# # Parameters for Savitzky-Golay filter
# window_length = 7  # Window length must be odd and greater than polyorder
# polyorder = 3       # Polynomial order to fit over the window
# kernel_size = 9       # FOr median filter

# # Read csv file
# df1 = pd.read_csv('/home/do-gon/vibecheck_ws/output.csv')

# # Process data, connect every message together
# data_columns1 = [col for col in df1.columns if 'data_' in col]
# data1 = df1[data_columns1].values.flatten()  # flatten data point

# # Apply Savitzky-Golay filter or Median filter (uncomment them if use it)
# # data1 = savgol_filter(data1, window_length, polyorder)
# # data1 = medfilt(data1, kernel_size=kernel_size)

# # # Apply Hann window (uncomment them if use it)
# # window = windows.hann(data1.size)
# # data1 = data1 * window

# # Run FFT
# fft_result1 = fft(data1)

# # Calculate frequency
# sample_rate = 44100
# freq1 = np.fft.fftfreq(data1.size, d=1/sample_rate)

# # Select positive frequency part
# positive_freq_indices1 = freq1 > 0
# positive_freqs1 = freq1[positive_freq_indices1]
# positive_fft_result1 = fft_result1[positive_freq_indices1]

# # Plot
# plt.figure(figsize=(15, 5))  # Create a single plot
# plt.plot(positive_freqs1, np.abs(positive_fft_result1))  # freq vs amplitude
# plt.title('FFT of Signal.csv')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Amplitude')
# # plt.xlim(1000, 15000)  # Set x-axis limits to 1 to 600 Hz
# plt.ylim(0, 2000)

# plt.grid(True)
# plt.tight_layout()  # Adjust layout to prevent overlap
# plt.show()


###################################


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.signal import windows, savgol_filter, medfilt

# Parameters for Savitzky-Golay filter
window_length = 5  # Window length must be odd and greater than polyorder
polyorder = 1       # Polynomial order to fit over the window
kernel_size = 99     # For median filter

# Read csv file
df1 = pd.read_csv('/home/do-gon/vibecheck_ws/datas/11.1/material_classification_train_sets/bra_thin_hollow/output_6.csv')

# Process data, connect every message together
data_columns1 = [col for col in df1.columns if 'data_' in col]
data1 = df1[data_columns1].values.flatten()  # flatten data point

# Apply Savitzky-Golay filter or Median filter (uncomment them if use it)
# data1 = savgol_filter(data1, window_length, polyorder)
# data1 = medfilt(data1, kernel_size=kernel_size)

# Apply Hann window (uncomment them if use it)
# window = windows.hann(len(data1))  # Ensure window length matches data length
# data1 = data1 * window

# Run FFT
fft_result1 = fft(data1)

# Calculate frequency
sample_rate = 44100
freq1 = np.fft.fftfreq(data1.size, d=1/sample_rate)

# Select positive frequency part
positive_freq_indices1 = freq1 > 0
positive_freqs1 = freq1[positive_freq_indices1]
positive_fft_result1 = fft_result1[positive_freq_indices1]

# Downsample the FFT result
resolution = 500  # Number of frequency bins,  default: 220479
if len(positive_freqs1) > resolution:
    step = max(len(positive_freqs1) // resolution, 1)  # Ensure step is at least 1
    print("Number of bins:", resolution)
    print("step:", step)
    downsampled_freqs1 = positive_freqs1[::step]
    downsampled_fft_result1 = positive_fft_result1[::step]
else:
    print(positive_freqs1.size)
    downsampled_freqs1 = positive_freqs1
    downsampled_fft_result1 = positive_fft_result1


# Plot
plt.figure(figsize=(15, 5))  # Create a single plot
plt.plot(downsampled_freqs1, np.abs(downsampled_fft_result1))  # freq vs amplitude
plt.title('FFT of Aluminum stick downsampling to 500 points')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.xlim(0, 20500)  # Set x-axis limits as needed
plt.ylim(0, 300000)  # Adjust y-axis limits as needed

plt.grid(True)
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()
