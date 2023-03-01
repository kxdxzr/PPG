import csv
import pandas as pd
import matplotlib.pyplot as plt
import serial

baud_rate = 115200
data_df = pd.DataFrame(columns=['PPG','sample_freq'])

# get input from user
filename = input("\nEnter file name for saved data ('.csv' will be appended): ") + '.csv'
serial_port = input("Enter the serial port name of the device: ")
sample_number = int(input("Enter number of samples to record: "))

# create serial connection, read data
serial_conn = serial.Serial(serial_port, baud_rate)
print('\nRecording...')
for i in range(sample_number):
    sample = serial_conn.readline().decode('ASCII').replace('\r', '').replace('\n', '')
    sample = [float(val) for val in sample.split(',')]
    data_df.loc[len(data_df)] = sample

# save data, re-import saved file and visualise to confirm recording
data_df.to_csv(filename)
input("\nData acquired, file '%s' created. Hit Enter to visualise...\n" % filename)
import_df = pd.read_csv(filename)

fig = plt.figure(figsize=[20,20])
ax_1 = fig.add_subplot(211)
ax_1.set_title('PPG Data')
ax_1.set_ylabel('Amplitude')
ax_1.plot(import_df['PPG'])
ax_2 = fig.add_subplot(212)
ax_2.set_title('Sample Freq')
ax_2.set_ylabel('Hz')
ax_2.set_xlabel('Samples')
ax_2.set_ylim(0, max(import_df['sample_freq'])*1.1)
ax_2.plot(import_df['sample_freq'])
plt.show()
