# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.fft import fft
# from scipy.signal import windows, savgol_filter, medfilt

# # Parameters for filters
# window_length = 5  # Window length must be odd and greater than polyorder
# polyorder = 1       # Polynomial order to fit over the window
# kernel_size = 99     # For median filter
# sample_rate = 44100  # Sampling rate for all datasets
# resolution = 500    # Number of frequency bins for downsampling

# # Function to process data, apply filters, FFT, and downsample
# def process_fft(csv_path, label):
#     # Read csv file
#     df = pd.read_csv(csv_path)
    
#     # Process data, connect every message together
#     data_columns = [col for col in df.columns if 'data_' in col]
#     data = df[data_columns].values.flatten()

#     # Apply Savitzky-Golay filter or Median filter (optional)
#     # data = savgol_filter(data, window_length, polyorder)
#     # data = medfilt(data, kernel_size=kernel_size)

#     # Apply Hann window (optional)
#     # window = windows.hann(len(data))  # Ensure window length matches data length
#     # data = data * window

#     # Run FFT
#     fft_result = fft(data)

#     # Calculate frequency
#     freq = np.fft.fftfreq(data.size, d=1/sample_rate)

#     # Select positive frequency part
#     positive_freq_indices = freq > 0
#     positive_freqs = freq[positive_freq_indices]
#     positive_fft_result = fft_result[positive_freq_indices]

#     # Downsample the FFT result
#     if len(positive_freqs) > resolution:
#         step = max(len(positive_freqs) // resolution, 1)  # Ensure step is at least 1
#         downsampled_freqs = positive_freqs[::step]
#         downsampled_fft_result = positive_fft_result[::step]
#     else:
#         downsampled_freqs = positive_freqs
#         downsampled_fft_result = positive_fft_result

#     return downsampled_freqs, np.abs(downsampled_fft_result), label

# # Process and plot FFTs for three files
# # csv_files = ['/home/do-gon/vibecheck_ws/datas/10.19 - test/After changing tape/Wood/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.19 - test/After changing tape/Aluminum/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.19 - test/After changing tape/Aluminum_thick_hollow/output_1.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.19 - test/After changing tape/Aluminum_thin_hollow/output_1.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.19 - test/After changing tape/Brass/output_1.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.19 - test/After changing tape/Brass_thin_hollow/output_1.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.19 - test/After changing tape/Plastic/output_1.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.19 - test/After changing tape/Printed_resin/output_1.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.19 - test/After changing tape/Printed_PLA/output_1.csv'] 

# # csv_files = ['/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/contact test/alu_full_contact/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/contact test/alu_stand_contact/output_2.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/contact test/alu_bottom_edge_contact/output_3.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/contact test/alu_point_contact/output_4.csv', 
# #              ]

# # csv_files = ['/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/liquid test/water_center_contact_100ml_speed_60/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/liquid test/water_center_contact_100ml_speed_60/output_2.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/liquid test/water_center_contact_100ml_speed_60/output_3.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/liquid test/water_center_contact_100ml_speed_60/output_4.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/liquid test/water_center_contact_100ml_speed_60/output_5.csv'
# #              ]

# # csv_files = ['/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p1/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p2/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p3/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p4/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p5/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p6/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p7/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p8/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p9/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p10/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p11/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p12/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p13/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p14/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p15/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p16/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p17/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p18/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p19/output_1.csv', 
# #              ]

# # csv_files = ['/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/internal structure/position1/output_2.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/internal structure/position2/output_5.csv', 
#             #  ]


# # csv_files = ['/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/internal structure/position3/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/internal structure/position4/output_4.csv', 
#             #  ]

# # csv_files = ['/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/liquid test/water_edge_100ml_speed_20/output_5.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/liquid test/water_edge_100ml_speed_40/output_5.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/liquid test/water_edge_100ml_speed_60/output_5.csv',
# #              ] 

# # csv_files = ['/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/liquid test/water_center_contact_100ml_speed_20/output_5.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/liquid test/honey_center_100ml_speed_20/output_5.csv', 
# #              ] 

# # csv_files = ['/home/do-gon/vibecheck_ws/datas/10.21 - egg/raw egg/output_72.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.21 - egg/soft boiled egg/output_51.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.21 - egg/hard boiled egg/output_1.csv', 
# #              ]
# # csv_files = ['/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/output_2.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/output_3.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/output_4.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/output_5.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/output_6.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/output_7.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/output_8.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/output_9.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/output_10.csv', 
# #              ]

# csv_files = ['/home/do-gon/vibecheck_ws/datas/10.14 - with UR5/Liquid_tests/Level_tests/baseline(no_liquid)/output_4.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.14 - with UR5/Liquid_tests/Level_tests/60ml/output_3.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.14 - with UR5/Liquid_tests/different liquids/milk 60 ml/output_6.csv',
#              '/home/do-gon/vibecheck_ws/datas/10.14 - with UR5/Liquid_tests/different liquids/oil 60 ml/output_6.csv',
#              '/home/do-gon/vibecheck_ws/datas/10.14 - with UR5/Liquid_tests/different liquids/honey 60 ml/output_8.csv',
#              ]

# # csv_files = ['/home/do-gon/vibecheck_ws/datas/10.14 - with UR5/Liquid_tests/Level_tests/baseline(no_liquid)/output_4.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.14 - with UR5/Liquid_tests/Level_tests/20ml/output_6.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.14 - with UR5/Liquid_tests/Level_tests/40ml/output_6.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.14 - with UR5/Liquid_tests/Level_tests/60ml/output_6.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.14 - with UR5/Liquid_tests/Level_tests/80ml/output_6.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.14 - with UR5/Liquid_tests/Level_tests/100ml/output_6.csv',
# #              ]

# # labels = ['0 ml (Baseline)', '20 ml', '40 ml', '60 ml', '80 ml', '100 ml'] 

# labels = ['0 ml (Baseline)', 'Water', 'Milk', 'Oil', 'Honey'] 



# # labels = ['Full contact', 'Stand contact', 'Bottom edge contact', 'Point contact'] 

# # labels = ['0 degree', '10 degree', '20 degree', '30 degree', '40 degree', 
# #           '50 degree', '60 degree', '70 degree', '80 degree', '90 degree', 
# #           '100 degree', '110 degree', '120 degree', '130 degree', '140 degree', 
# #           '150 degree', '160 degree', '170 degree', '180 degree', ] 

# # labels = ['position1', 'position2'] 

# # labels = ['Wood', 'Aluminum', 'Aluminum Thick Hollow', 'Aluminum Thin Hollow', 'Brass', 'Brass Thin Hollow', 'Plastic', 'Printed Resin', 'Printed PLA'] 

# # labels = ['1 s', '2 s', '3 s', '4 s', '5 s'] 

# # labels = ['Raw', 'Soft boiled', 'Hard boiled', 'Soft boiled', 'Hard boiled', 'Soft boiled', 'Hard boiled', 'Soft boiled', 'Hard boiled', 'Soft boiled', 'Hard boiled'] 

# plt.figure(figsize=(16, 8))  # Create a single plot

# # Loop over the CSV files and plot the FFT for each one
# for csv_file, label in zip(csv_files, labels):
#     freqs, fft_result, label = process_fft(csv_file, label)
#     plt.plot(freqs, fft_result, label=label)  # Plot each FFT

# # Plot configuration
# plt.title('FFT Comparison between 4 different liquids', fontsize=24)
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Amplitude')
# plt.xlim(0, 20500)  # Set x-axis limits
# plt.ylim(0, 200000)   # Set y-axis limits (adjust as needed)
# plt.grid(True)
# plt.legend(fontsize=20)  # Show legend
# plt.tight_layout()  # Adjust layout
# plt.show()

###############################################################################################################################

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.fft import fft
# from scipy.signal import windows, savgol_filter, medfilt

# # Parameters for filters
# window_length = 5  # Window length must be odd and greater than polyorder
# polyorder = 1      # Polynomial order to fit over the window
# kernel_size = 99   # For median filter
# sample_rate = 44100  # Sampling rate for all datasets
# resolution = 500    # Number of frequency bins for downsampling

# # Function to process data, apply filters, FFT, and downsample
# def process_fft(csv_path, label):
#     # Read csv file
#     df = pd.read_csv(csv_path)
    
#     # Process data, connect every message together
#     data_columns = [col for col in df.columns if 'data_' in col]
#     data = df[data_columns].values.flatten()

#     # Apply Savitzky-Golay filter or Median filter (optional)
#     # data = savgol_filter(data, window_length, polyorder)
#     # data = medfilt(data, kernel_size=kernel_size)

#     # Apply Hann window (optional)
#     # window = windows.hann(len(data))  # Ensure window length matches data length
#     # data = data * window

#     # Run FFT
#     fft_result = fft(data)

#     # Calculate frequency
#     freq = np.fft.fftfreq(data.size, d=1/sample_rate)

#     # Select positive frequency part
#     positive_freq_indices = freq > 0
#     positive_freqs = freq[positive_freq_indices]
#     positive_fft_result = fft_result[positive_freq_indices]

#     # Downsample the FFT result
#     if len(positive_freqs) > resolution:
#         step = max(len(positive_freqs) // resolution, 1)  # Ensure step is at least 1
#         downsampled_freqs = positive_freqs[::step]
#         downsampled_fft_result = positive_fft_result[::step]
#     else:
#         downsampled_freqs = positive_freqs
#         downsampled_fft_result = positive_fft_result

#     return downsampled_freqs, np.abs(downsampled_fft_result), label

# # Define CSV files and labels
# csv_files = ['/home/do-gon/vibecheck_ws/datas/10.30/contact_type/alu_thick_hollow_full_contact/output_2.csv',  
#              '/home/do-gon/vibecheck_ws/datas/10.30/contact_type/alu_thick_hollow_stand_contact/output_5.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.30/contact_type/alu_thick_hollow_bottom_edge_contact/output_7.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.30/contact_type/alu_thick_hollow_point_contact/output_4.csv'
#              ]

# labels = ['Full contact', 
#           'Stand contact', 
#           'Bottom edge contact', 
#           'Point contact'] 

# # Assign colors to each contact type
# color_map = {
#     'Full contact': 'blue',
#     'Stand contact': 'green',
#     'Bottom edge contact': 'red',
#     'Point contact': 'orange'
# }

# plt.figure(figsize=(16, 8))  # Create a single plot

# # Loop over the CSV files and plot the FFT for each one
# for csv_file, label in zip(csv_files, labels):
#     freqs, fft_result, label = process_fft(csv_file, label)
    
#     # Determine color based on the type of contact
#     if 'Full contact' in label:
#         color = color_map['Full contact']
#     elif 'Stand contact' in label:
#         color = color_map['Stand contact']
#     elif 'Bottom edge contact' in label:
#         color = color_map['Bottom edge contact']
#     elif 'Point contact' in label:
#         color = color_map['Point contact']
    
#     plt.plot(freqs, fft_result, label=label, color=color)  # Plot each FFT with specific color

# # Plot configuration
# plt.title('FFT Comparison between 4 different contacts (Aluminum Thick Hollow)', fontsize=24)
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Amplitude')
# plt.xlim(0, 20500)  # Set x-axis limits
# plt.ylim(0, 900000)   # Set y-axis limits (adjust as needed)
# plt.grid(True)
# plt.legend(fontsize=20)  # Show legend
# plt.tight_layout()  # Adjust layout
# plt.show()

###############################################################################################################################

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.fft import fft
# from scipy.signal import windows, savgol_filter, medfilt

# # Parameters for filters
# window_length = 5  # Window length must be odd and greater than polyorder
# polyorder = 1      # Polynomial order to fit over the window
# kernel_size = 99   # For median filter
# sample_rate = 44100  # Sampling rate for all datasets
# resolution = 500    # Number of frequency bins for downsampling

# # Function to process data, apply filters, FFT, and downsample
# def process_fft(csv_path, label):
#     # Read csv file
#     df = pd.read_csv(csv_path)
    
#     # Process data, connect every message together
#     data_columns = [col for col in df.columns if 'data_' in col]
#     data = df[data_columns].values.flatten()

#     # Apply Savitzky-Golay filter or Median filter (optional)
#     # data = savgol_filter(data, window_length, polyorder)
#     # data = medfilt(data, kernel_size=kernel_size)

#     # Apply Hann window (optional)
#     # window = windows.hann(len(data))  # Ensure window length matches data length
#     # data = data * window

#     # Run FFT
#     fft_result = fft(data)

#     # Calculate frequency
#     freq = np.fft.fftfreq(data.size, d=1/sample_rate)

#     # Select positive frequency part
#     positive_freq_indices = freq > 0
#     positive_freqs = freq[positive_freq_indices]
#     positive_fft_result = fft_result[positive_freq_indices]

#     # Downsample the FFT result
#     if len(positive_freqs) > resolution:
#         step = max(len(positive_freqs) // resolution, 1)  # Ensure step is at least 1
#         downsampled_freqs = positive_freqs[::step]
#         downsampled_fft_result = positive_fft_result[::step]
#     else:
#         downsampled_freqs = positive_freqs
#         downsampled_fft_result = positive_fft_result

#     return downsampled_freqs, np.abs(downsampled_fft_result), label

# # Define CSV files and labels
# csv_files = ['/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p1/output_1.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p1/output_36.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p1/output_71.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p1/output_56.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p1/output_81.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p5/output_1.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p5/output_36.csv',
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p5/output_71.csv',
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p5/output_56.csv',
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p5/output_81.csv',
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p10/output_1.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p10/output_36.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p10/output_71.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p10/output_56.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p10/output_81.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p15/output_1.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p15/output_36.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p15/output_71.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p15/output_56.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p15/output_81.csv',
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p19/output_1.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p19/output_36.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p19/output_71.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p19/output_56.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_2/p19/output_81.csv',
#              ]

# labels = ['0 degree1', '0 degree2', '0 degree3', '0 degree4', '0 degree5',
#           '40 degree1', '40 degree2', '40 degree3', '40 degree4', '40 degree5', 
#           '90 degree1', '90 degree2', '90 degree3', '90 degree4', '90 degree5', 
#           '140 degree1', '140 degree2', '140 degree3', '140 degree4', '140 degree5',
#           '180 degree1', '180 degree2', '180 degree3', '180 degree4', '180 degree5'
#           ] 

# # Assign colors to each contact type
# color_map = {
#     '0 degree': 'blue',
#     '40 degree': 'green',
#     '90 degree': 'red',
#     '140 degree': 'orange',
#     '180 degree': 'purple'
# }

# plt.figure(figsize=(20, 10))  # Create a single plot

# # Loop over the CSV files and plot the FFT for each one
# for csv_file, label in zip(csv_files, labels):
#     freqs, fft_result, label = process_fft(csv_file, label)
    
#     # Determine color based on the type of contact
#     if '40 degree' in label:
#         color = color_map['40 degree']
#     elif '90 degree' in label:
#         color = color_map['90 degree']
#     elif '140 degree' in label:
#         color = color_map['140 degree']
#     elif '180 degree' in label:
#         color = color_map['180 degree']
#     elif '0 degree' in label:
#         color = color_map['0 degree']
    
#     plt.plot(freqs, fft_result, label=label, color=color)  # Plot each FFT with specific color

# # Plot configuration
# plt.title('FFT Comparison between 5 different angles (Cylinder 2)', fontsize=24)
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Amplitude')
# plt.xlim(0, 20500)  # Set x-axis limits
# plt.ylim(0, 200000)   # Set y-axis limits (adjust as needed)
# plt.grid(True)
# plt.legend(fontsize=12, loc='upper left', bbox_to_anchor=(1, 1))  # Show legend
# plt.tight_layout()  # Adjust layout
# plt.show()

###############################################################################################################################

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.fft import fft
# from scipy.signal import windows, savgol_filter, medfilt

# # Parameters for filters
# window_length = 5  # Window length must be odd and greater than polyorder
# polyorder = 1      # Polynomial order to fit over the window
# kernel_size = 99   # For median filter
# sample_rate = 44100  # Sampling rate for all datasets
# resolution = 500    # Number of frequency bins for downsampling

# # Function to process data, apply filters, FFT, and downsample
# def process_fft(csv_path, label):
#     # Read csv file
#     df = pd.read_csv(csv_path)
    
#     # Process data, connect every message together
#     data_columns = [col for col in df.columns if 'data_' in col]
#     data = df[data_columns].values.flatten()

#     # Apply Savitzky-Golay filter or Median filter (optional)
#     # data = savgol_filter(data, window_length, polyorder)
#     # data = medfilt(data, kernel_size=kernel_size)

#     # Apply Hann window (optional)
#     # window = windows.hann(len(data))  # Ensure window length matches data length
#     # data = data * window

#     # Run FFT
#     fft_result = fft(data)

#     # Calculate frequency
#     freq = np.fft.fftfreq(data.size, d=1/sample_rate)

#     # Select positive frequency part
#     positive_freq_indices = freq > 0
#     positive_freqs = freq[positive_freq_indices]
#     positive_fft_result = fft_result[positive_freq_indices]

#     # Downsample the FFT result
#     if len(positive_freqs) > resolution:
#         step = max(len(positive_freqs) // resolution, 1)  # Ensure step is at least 1
#         downsampled_freqs = positive_freqs[::step]
#         downsampled_fft_result = positive_fft_result[::step]
#     else:
#         downsampled_freqs = positive_freqs
#         downsampled_fft_result = positive_fft_result

#     return downsampled_freqs, np.abs(downsampled_fft_result), label

# # Define CSV files and labels
# csv_files = ['/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_1/p1/output_71.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_1/p5/output_71.csv',
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_1/p10/output_71.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_1/p15/output_71.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.23/internal_structure_cylinders/cylinder_1/p19/output_71.csv', 
#              ]

# labels = ['0 degree',
#           '40 degree',
#           '90 degree',
#           '140 degree',
#           '180 degree'
#           ] 

# # Assign colors to each contact type
# color_map = {
#     '0 degree': 'blue',
#     '40 degree': 'green',
#     '90 degree': 'red',
#     '140 degree': 'orange',
#     '180 degree': 'purple'
# }

# plt.figure(figsize=(20, 10))  # Create a single plot

# # Loop over the CSV files and plot the FFT for each one
# for csv_file, label in zip(csv_files, labels):
#     freqs, fft_result, label = process_fft(csv_file, label)
    
#     # Determine color based on the type of contact
#     if '40 degree' in label:
#         color = color_map['40 degree']
#     elif '90 degree' in label:
#         color = color_map['90 degree']
#     elif '140 degree' in label:
#         color = color_map['140 degree']
#     elif '180 degree' in label:
#         color = color_map['180 degree']
#     elif '0 degree' in label:
#         color = color_map['0 degree']
    
#     plt.plot(freqs, fft_result, label=label, color=color)  # Plot each FFT with specific color

# # Plot configuration
# plt.title('FFT Comparison between 5 different angles (Cylinder 1)', fontsize=24)
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Amplitude')
# plt.xlim(0, 20500)  # Set x-axis limits
# plt.ylim(0, 200000)   # Set y-axis limits (adjust as needed)
# plt.grid(True)
# plt.legend(fontsize=12, loc='upper left', bbox_to_anchor=(1, 1))  # Show legend
# plt.tight_layout()  # Adjust layout
# plt.show()

###############################################################################################################################

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.fft import fft
# from scipy.signal import windows, savgol_filter, medfilt

# # Parameters for filters
# window_length = 5  # Window length must be odd and greater than polyorder
# polyorder = 1      # Polynomial order to fit over the window
# kernel_size = 99   # For median filter
# sample_rate = 44100  # Sampling rate for all datasets
# resolution = 500    # Number of frequency bins for downsampling

# # Function to process data, apply filters, FFT, and downsample
# def process_fft(csv_path, label):
#     # Read csv file
#     df = pd.read_csv(csv_path)
    
#     # Process data, connect every message together
#     data_columns = [col for col in df.columns if 'data_' in col]
#     data = df[data_columns].values.flatten()

#     # Apply Savitzky-Golay filter or Median filter (optional)
#     # data = savgol_filter(data, window_length, polyorder)
#     # data = medfilt(data, kernel_size=kernel_size)

#     # Apply Hann window (optional)
#     # window = windows.hann(len(data))  # Ensure window length matches data length
#     # data = data * window

#     # Run FFT
#     fft_result = fft(data)

#     # Calculate frequency
#     freq = np.fft.fftfreq(data.size, d=1/sample_rate)

#     # Select positive frequency part
#     positive_freq_indices = freq > 0
#     positive_freqs = freq[positive_freq_indices]
#     positive_fft_result = fft_result[positive_freq_indices]

#     # Downsample the FFT result
#     if len(positive_freqs) > resolution:
#         step = max(len(positive_freqs) // resolution, 1)  # Ensure step is at least 1
#         downsampled_freqs = positive_freqs[::step]
#         downsampled_fft_result = positive_fft_result[::step]
#     else:
#         downsampled_freqs = positive_freqs
#         downsampled_fft_result = positive_fft_result

#     return downsampled_freqs, np.abs(downsampled_fft_result), label

# # Define CSV files and labels
# csv_files = ['/home/do-gon/vibecheck_ws/datas/10.30/material_classification/alu/output_3.csv', 

#              '/home/do-gon/vibecheck_ws/datas/10.30/material_classification/alu_hollow_thick/output_3.csv', 

#              '/home/do-gon/vibecheck_ws/datas/10.30/material_classification/alu_hollow_thin/output_2.csv', 

#              '/home/do-gon/vibecheck_ws/datas/10.30/material_classification/bra/output_3.csv', 

#              '/home/do-gon/vibecheck_ws/datas/10.30/material_classification/bra_hollow_thin/output_2.csv', 

#              '/home/do-gon/vibecheck_ws/datas/10.30/material_classification/pla/output_6.csv', 

#              '/home/do-gon/vibecheck_ws/datas/10.30/material_classification/printed_pla/output_5.csv', 

#              '/home/do-gon/vibecheck_ws/datas/10.30/material_classification/printed_resin/output_3.csv', 

#              '/home/do-gon/vibecheck_ws/datas/10.30/material_classification/woo/output_3.csv'
#              ]

# labels = ['Aluminum', 
#           'Aluminum Thick Hollow', 
#           'Aluminum Thin Hollow', 
#           'Brass', 
#           'Brass Thin Hollow', 
#           'Plastic', 
#           'PLA', 
#           'Resin', 
#           'Wood', 
#          ]


# # Assign colors to each contact type
# color_map = {
#     'Aluminum': 'pink',
#     'Aluminum Thick Hollow': 'brown',
#     'Aluminum Thin Hollow': 'olive',
#     'Brass': 'red',
#     'Brass Thin Hollow': 'orange',
#     'Plastic': 'green',
#     'PLA': 'cyan',
#     'Resin': 'blue',
#     'Wood': 'purple'
# }

# plt.figure(figsize=(16, 8))  # Create a single plot

# # Loop over the CSV files and plot the FFT for each one
# for csv_file, label in zip(csv_files, labels):
#     freqs, fft_result, label = process_fft(csv_file, label)
    
#     # Determine color based on the type of contact
#     if 'Aluminum Thick Hollow' in label:
#         color = color_map['Aluminum Thick Hollow']
#     elif 'Aluminum Thin Hollow' in label:
#         color = color_map['Aluminum Thin Hollow']
#     elif 'Aluminum' in label:
#         color = color_map['Aluminum']
#     elif 'Brass Thin Hollow' in label:
#         color = color_map['Brass Thin Hollow']
#     elif 'Brass' in label:
#         color = color_map['Brass']
#     elif 'Plastic' in label:
#         color = color_map['Plastic']
#     elif 'PLA' in label:
#         color = color_map['PLA']
#     elif 'Resin' in label:
#         color = color_map['Resin']
#     elif 'Wood' in label:
#         color = color_map['Wood']
#     plt.plot(freqs, fft_result, label=label, color=color)  # Plot each FFT with specific color

# # # Plot configuration
# # plt.title('FFT Comparison between 9 different objects', fontsize=24)
# # plt.xlabel('Frequency (Hz)')
# # plt.ylabel('Amplitude')
# # plt.xlim(0, 20500)  # Set x-axis limits
# # plt.ylim(0, 900000)   # Set y-axis limits (adjust as needed)
# # plt.grid(True)
# # plt.legend(fontsize=8, loc='upper left', bbox_to_anchor=(1, 1))  # Place legend outside the plot
# # plt.tight_layout()  # Adjust layout
# # plt.show()

# # Plot configuration
# plt.title('FFT Comparison between 9 different objects', fontsize=24)
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Amplitude')
# plt.xlim(0, 20500)  # Set x-axis limits
# plt.ylim(0, 900000)   # Set y-axis limits (adjust as needed)
# plt.grid(True)
# plt.legend(fontsize=20)  # Show legend
# plt.tight_layout()  # Adjust layout
# plt.show()

###############################################################################################################################

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.fft import fft
# from scipy.signal import windows, savgol_filter, medfilt

# # Parameters for filters
# window_length = 5  # Window length must be odd and greater than polyorder
# polyorder = 1      # Polynomial order to fit over the window
# kernel_size = 99   # For median filter
# sample_rate = 44100  # Sampling rate for all datasets
# resolution = 500    # Number of frequency bins for downsampling

# # Function to process data, apply filters, FFT, and downsample
# def process_fft(csv_path, label):
#     # Read csv file
#     df = pd.read_csv(csv_path)
    
#     # Process data, connect every message together
#     data_columns = [col for col in df.columns if 'data_' in col]
#     data = df[data_columns].values.flatten()

#     # Apply Savitzky-Golay filter or Median filter (optional)
#     # data = savgol_filter(data, window_length, polyorder)
#     # data = medfilt(data, kernel_size=kernel_size)

#     # Apply Hann window (optional)
#     # window = windows.hann(len(data))  # Ensure window length matches data length
#     # data = data * window

#     # Run FFT
#     fft_result = fft(data)

#     # Calculate frequency
#     freq = np.fft.fftfreq(data.size, d=1/sample_rate)

#     # Select positive frequency part
#     positive_freq_indices = freq > 0
#     positive_freqs = freq[positive_freq_indices]
#     positive_fft_result = fft_result[positive_freq_indices]

#     # Downsample the FFT result
#     if len(positive_freqs) > resolution:
#         step = max(len(positive_freqs) // resolution, 1)  # Ensure step is at least 1
#         downsampled_freqs = positive_freqs[::step]
#         downsampled_fft_result = positive_fft_result[::step]
#     else:
#         downsampled_freqs = positive_freqs
#         downsampled_fft_result = positive_fft_result

#     return downsampled_freqs, np.abs(downsampled_fft_result), label

# # Define CSV files and labels
# csv_files = ['/home/do-gon/vibecheck_ws/datas/10.19 - solid v.s. liquid (ice v.s. water)/water 60 ml/output_80.csv', 

#              '/home/do-gon/vibecheck_ws/datas/10.19 - solid v.s. liquid (ice v.s. water)/ice 60 ml/output_80.csv', 
#              ]

# labels = ['Water', 
#           'Ice', 
#         ] 

# # csv_files = ['/home/do-gon/vibecheck_ws/datas/10.21 - egg/raw egg/output_80.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.21 - egg/soft boiled egg/output_80.csv',
# #              '/home/do-gon/vibecheck_ws/datas/10.21 - egg/hard boiled egg/output_80.csv', 
# #              ]

# # labels = ['Raw egg', 
# #           'Soft boiled egg', 
# #           'Hard boiled egg'
# #         ] 

# # csv_files = ['/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/internal structure/position1/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/internal structure/position1/output_2.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/internal structure/position1/output_3.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/internal structure/position1/output_4.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/internal structure/position1/output_5.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/internal structure/position2/output_1.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/internal structure/position2/output_2.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/internal structure/position2/output_3.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/internal structure/position2/output_4.csv', 
# #              '/home/do-gon/vibecheck_ws/datas/10.18 - contact & liquid test/internal structure/position2/output_5.csv', 
# #              ]

# # labels = ['Position1', 'Position1', 'Position1', 'Position1', 'Position1',
# #           'Position2', 'Position2', 'Position2', 'Position2', 'Position2', 
# #         ] 

# # Assign colors to each contact type
# # color_map = {
# #     'Raw egg': 'blue',
# #     'Soft boiled egg': 'red',
# #     'Hard boiled egg': 'green'
# # }

# color_map = {
#     'Water': 'blue',
#     'Ice': 'red',
# }

# plt.figure(figsize=(16, 8))  # Create a single plot

# # Loop over the CSV files and plot the FFT for each one
# for csv_file, label in zip(csv_files, labels):
#     freqs, fft_result, label = process_fft(csv_file, label)
    
#     # Determine color based on the type of contact
#     if 'Water' in label:
#         color = color_map['Water']
#     elif 'Ice' in label:
#         color = color_map['Ice']

    
#     plt.plot(freqs, fft_result, label=label, color=color)  # Plot each FFT with specific color

# # Plot configuration
# plt.title('FFT Comparison between 2 different states (H2O)', fontsize=24)
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Amplitude')
# plt.xlim(0, 20500)  # Set x-axis limits
# plt.ylim(0, 200000)   # Set y-axis limits (adjust as needed)
# plt.grid(True)
# plt.legend(fontsize=20)  # Show legend
# plt.tight_layout()  # Adjust layout
# plt.show()

###############################################################################################

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.fft import fft
# from scipy.signal import windows, savgol_filter, medfilt

# # Parameters for filters
# window_length = 5  # Window length must be odd and greater than polyorder
# polyorder = 1      # Polynomial order to fit over the window
# kernel_size = 99   # For median filter
# sample_rate = 44100  # Sampling rate for all datasets
# resolution = 500    # Number of frequency bins for downsampling

# # Function to process data, apply filters, FFT, and downsample
# def process_fft(csv_path, label):
#     # Read csv file
#     df = pd.read_csv(csv_path)
    
#     # Process data, connect every message together
#     data_columns = [col for col in df.columns if 'data_' in col]
#     data = df[data_columns].values.flatten()

#     # Apply Savitzky-Golay filter or Median filter (optional)
#     # data = savgol_filter(data, window_length, polyorder)
#     # data = medfilt(data, kernel_size=kernel_size)

#     # Apply Hann window (optional)
#     # window = windows.hann(len(data))  # Ensure window length matches data length
#     # data = data * window

#     # Run FFT
#     fft_result = fft(data)

#     # Calculate frequency
#     freq = np.fft.fftfreq(data.size, d=1/sample_rate)

#     # Select positive frequency part
#     positive_freq_indices = freq > 0
#     positive_freqs = freq[positive_freq_indices]
#     positive_fft_result = fft_result[positive_freq_indices]

#     # Downsample the FFT result
#     if len(positive_freqs) > resolution:
#         step = max(len(positive_freqs) // resolution, 1)  # Ensure step is at least 1
#         downsampled_freqs = positive_freqs[::step]
#         downsampled_fft_result = positive_fft_result[::step]
#     else:
#         downsampled_freqs = positive_freqs
#         downsampled_fft_result = positive_fft_result

#     return downsampled_freqs, np.abs(downsampled_fft_result), label

# # Define CSV files and labels
# csv_files = ['/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_1.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_2.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_3.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_4.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_5.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_6.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_7.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_8.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_9.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_10.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_11.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_12.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_13.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_14.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_15.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_16.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_17.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_18.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_19.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_20.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_21.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_22.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_23.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_24.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_25.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_26.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_27.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_28.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_29.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_30.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_31.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_32.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_33.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_34.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_35.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_36.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_37.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_38.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_39.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_40.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_41.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_42.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_43.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_44.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_45.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_46.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_47.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_48.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_49.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.19 - test/Before changing tape/Nothing between two fingers (they are 2 cm away from each other)/output_50.csv', 
#              ]

# labels = ['Nothing1', 'Nothing2', 'Nothing3', 'Nothing4', 'Nothing5',
#           'Nothing6', 'Nothing7', 'Nothing8', 'Nothing9', 'Nothing10',
#           'Nothing11', 'Nothing12', 'Nothing13', 'Nothing14', 'Nothing15',
#           'Nothing16', 'Nothing17', 'Nothing18', 'Nothing19', 'Nothing20',
#           'Nothing21', 'Nothing22', 'Nothing23', 'Nothing24', 'Nothing25',
#           'Nothing26', 'Nothing27', 'Nothing28', 'Nothing29', 'Nothing30',
#           'Nothing31', 'Nothing32', 'Nothing33', 'Nothing34', 'Nothing35',
#           'Nothing36', 'Nothing37', 'Nothing38', 'Nothing39', 'Nothing40',
#           'Nothing41', 'Nothing42', 'Nothing43', 'Nothing44', 'Nothing45',
#           'Nothing46', 'Nothing47', 'Nothing48', 'Nothing49', 'Nothing50',
#         ] 

# # Assign colors to each contact type
# color_map = {
#     'Nothing': 'blue'
# }

# plt.figure(figsize=(20, 10))  # Create a single plot

# # Loop over the CSV files and plot the FFT for each one
# for csv_file, label in zip(csv_files, labels):
#     freqs, fft_result, label = process_fft(csv_file, label)
    
#     # Determine color based on the type of contact
#     if 'Nothing' in label:
#         color = color_map['Nothing']

    
#     plt.plot(freqs, fft_result, label=label, color=color)  # Plot each FFT with specific color

# # Plot configuration
# plt.title('FFT plot when there is nothing between two fingers (2cm far away)', fontsize=24)
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Amplitude')
# plt.xlim(0, 20500)  # Set x-axis limits
# plt.ylim(0, 100000)   # Set y-axis limits (adjust as needed)
# plt.grid(True)
# plt.legend(fontsize=18)  # Show legend
# plt.tight_layout()  # Adjust layout
# plt.show()

###############################################################################################
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.fft import fft
# from scipy.signal import windows, savgol_filter, medfilt

# # Parameters for filters
# window_length = 5  # Window length must be odd and greater than polyorder
# polyorder = 1      # Polynomial order to fit over the window
# kernel_size = 99   # For median filter
# sample_rate = 44100  # Sampling rate for all datasets
# resolution = 500    # Number of frequency bins for downsampling

# # Function to process data, apply filters, FFT, and downsample
# def process_fft(csv_path, label):
#     # Read csv file
#     df = pd.read_csv(csv_path)
    
#     # Process data, connect every message together
#     data_columns = [col for col in df.columns if 'data_' in col]
#     data = df[data_columns].values.flatten()

#     # Apply Savitzky-Golay filter or Median filter (optional)
#     # data = savgol_filter(data, window_length, polyorder)
#     # data = medfilt(data, kernel_size=kernel_size)

#     # Apply Hann window (optional)
#     # window = windows.hann(len(data))  # Ensure window length matches data length
#     # data = data * window

#     # Run FFT
#     fft_result = fft(data)

#     # Calculate frequency
#     freq = np.fft.fftfreq(data.size, d=1/sample_rate)

#     # Select positive frequency part
#     positive_freq_indices = freq > 0
#     positive_freqs = freq[positive_freq_indices]
#     positive_fft_result = fft_result[positive_freq_indices]

#     # Downsample the FFT result
#     if len(positive_freqs) > resolution:
#         step = max(len(positive_freqs) // resolution, 1)  # Ensure step is at least 1
#         downsampled_freqs = positive_freqs[::step]
#         downsampled_fft_result = positive_fft_result[::step]
#     else:
#         downsampled_freqs = positive_freqs
#         downsampled_fft_result = positive_fft_result

#     return downsampled_freqs, np.abs(downsampled_fft_result), label

# # Define CSV files for each egg type
# raw_egg_files = [f'/home/do-gon/vibecheck_ws/datas/10.21 - egg/raw egg/output_{i}.csv' for i in range(1, 101)]
# soft_boiled_egg_files = [f'/home/do-gon/vibecheck_ws/datas/10.21 - egg/soft boiled egg/output_{i}.csv' for i in range(1, 101)]
# hard_boiled_egg_files = [f'/home/do-gon/vibecheck_ws/datas/10.21 - egg/hard boiled egg/output_{i}.csv' for i in range(1, 101)]

# # Combine all file paths
# csv_files = raw_egg_files + soft_boiled_egg_files + hard_boiled_egg_files

# # Define corresponding labels
# labels = [f'Raw Egg {i}' for i in range(1, 101)] + \
#          [f'Soft Boiled Egg {i}' for i in range(1, 101)] + \
#          [f'Hard Boiled Egg {i}' for i in range(1, 101)]

# # Assign colors to each egg type
# color_map = {
#     'Raw Egg': 'red',
#     'Soft Boiled Egg': 'green',
#     'Hard Boiled Egg': 'blue'
# }

# plt.figure(figsize=(20, 10))  # Create a single plot

# # Loop over the CSV files and plot the FFT for each one
# for csv_file, label in zip(csv_files, labels):
#     freqs, fft_result, label = process_fft(csv_file, label)
    
#     # Determine color based on the egg type
#     if 'Raw Egg' in label:
#         color = color_map['Raw Egg']
#     elif 'Soft Boiled Egg' in label:
#         color = color_map['Soft Boiled Egg']
#     elif 'Hard Boiled Egg' in label:
#         color = color_map['Hard Boiled Egg']
    
#     plt.plot(freqs, fft_result, label=label, color=color, alpha=0.5)  # Plot each FFT with specific color

# # Plot configuration
# plt.title('FFT plot for Raw, Soft Boiled, and Hard Boiled Eggs', fontsize=24)
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Amplitude')
# plt.xlim(0, 20500)  # Set x-axis limits
# plt.ylim(0, 300000)   # Set y-axis limits (adjust as needed)
# plt.grid(True)
# plt.legend(fontsize=10, loc='upper right')  # Show legend
# plt.tight_layout()  # Adjust layout
# plt.show()

#######################################################################################################################################


# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.fft import fft
# from scipy.signal import windows, savgol_filter, medfilt

# # Parameters for filters
# window_length = 5  # Window length must be odd and greater than polyorder
# polyorder = 1      # Polynomial order to fit over the window
# kernel_size = 99   # For median filter
# sample_rate = 44100  # Sampling rate for all datasets
# resolution = 500    # Number of frequency bins for downsampling

# # Function to process data, apply filters, FFT, and downsample
# def process_fft(csv_path, label):
#     # Read csv file
#     df = pd.read_csv(csv_path)
    
#     # Process data, connect every message together
#     data_columns = [col for col in df.columns if 'data_' in col]
#     data = df[data_columns].values.flatten()

#     # Run FFT
#     fft_result = fft(data)

#     # Calculate frequency
#     freq = np.fft.fftfreq(data.size, d=1/sample_rate)

#     # Select positive frequency part
#     positive_freq_indices = freq > 0
#     positive_freqs = freq[positive_freq_indices]
#     positive_fft_result = fft_result[positive_freq_indices]

#     # Downsample the FFT result
#     if len(positive_freqs) > resolution:
#         step = max(len(positive_freqs) // resolution, 1)  # Ensure step is at least 1
#         downsampled_freqs = positive_freqs[::step]
#         downsampled_fft_result = positive_fft_result[::step]
#     else:
#         downsampled_freqs = positive_freqs
#         downsampled_fft_result = positive_fft_result

#     return downsampled_freqs, np.abs(downsampled_fft_result), label

# # Define CSV files and labels
# csv_files = ['/home/do-gon/vibecheck_ws/datas/10.30/grasping_point/woo_center/output_3.csv',  
#              '/home/do-gon/vibecheck_ws/datas/10.30/grasping_point/woo_middle/output_4.csv', 
#              '/home/do-gon/vibecheck_ws/datas/10.30/grasping_point/woo_edge/output_4.csv', 
#              ]

# labels = ['Center', 
#           'Middle', 
#           'Edge', 
#           ] 

# # Assign colors to each contact type
# color_map = {
#     'Center': 'blue',
#     'Middle': 'green',
#     'Edge': 'red',
# }

# plt.figure(figsize=(16, 8))  # Create a single plot

# # Loop over the CSV files and plot the FFT for each one
# for csv_file, label in zip(csv_files, labels):
#     freqs, fft_result, label = process_fft(csv_file, label)
    
#     # Determine color based on the type of contact
#     if 'Center' in label:
#         color = color_map['Center']
#     elif 'Middle' in label:
#         color = color_map['Middle']
#     elif 'Edge' in label:
#         color = color_map['Edge']
    
#     plt.plot(freqs, fft_result, label=label, color=color)  # Plot each FFT with specific color

# # Plot configuration
# plt.title('FFT Comparison between 3 different grasping points (Wood)', fontsize=24)
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Amplitude')
# plt.xlim(0, 20500)  # Set x-axis limits
# plt.ylim(0, 900000)   # Set y-axis limits (adjust as needed)
# plt.grid(True)
# plt.legend(fontsize=20)  # Show legend
# plt.tight_layout()  # Adjust layout
# plt.show()

###############################################################################

import os
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

# Define directory path
base_dir = "/home/do-gon/acoustic_docker/vibecheck_ws/classification/data/contact_type/2025-2-23/demo_expanded_workspace/test_set"

# List of contact type directories
contact_types = [f"one_line_{i}" for i in range(1, 11)]

# Randomly select one CSV file from each contact type
selected_files = []
for contact_type in contact_types:
    contact_dir = os.path.join(base_dir, contact_type)
    csv_files = [f for f in os.listdir(contact_dir) if f.endswith(".csv") and f != "all_result.csv"]
    
    if csv_files:
        selected_file = random.choice(csv_files)
        selected_files.append((os.path.join(contact_dir, selected_file), contact_type))

# Parameters
sample_rate = 44100  # Sampling rate
resolution = 500  # Frequency bins for downsampling

# Function to process FFT
def process_fft(csv_path):
    df = pd.read_csv(csv_path)
    data_columns = [col for col in df.columns if 'data_' in col]
    data = df[data_columns].values.flatten()
    
    fft_result = fft(data)
    freq = np.fft.fftfreq(data.size, d=1/sample_rate)

    positive_freq_indices = freq > 0
    positive_freqs = freq[positive_freq_indices]
    positive_fft_result = np.abs(fft_result[positive_freq_indices])

    if len(positive_freqs) > resolution:
        step = max(len(positive_freqs) // resolution, 1)
        downsampled_freqs = positive_freqs[::step]
        downsampled_fft_result = positive_fft_result[::step]
    else:
        downsampled_freqs = positive_freqs
        downsampled_fft_result = positive_fft_result

    return downsampled_freqs, downsampled_fft_result

# Plot
plt.figure(figsize=(16, 8))

for csv_path, label in selected_files:
    freqs, fft_result = process_fft(csv_path)
    plt.plot(freqs, fft_result, label=label)

plt.title('FFT Comparison between Randomly Selected Contact Types', fontsize=16)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.xlim(0, 20500)
plt.ylim(0, 130000)   # Set y-axis limits (adjust as needed)
plt.grid(True)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()
