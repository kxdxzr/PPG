# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 13:25:43 2022

@author: yulep
"""

from C3 import Filtering_LPF
import wfdb
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter, freqz
from Q6 import Read_signals_from_file, Plot

def save_to_csv(x,y): 
    f=open('ECG_DATA_butterworth.csv','w') 
    np.savetxt(f,np.transpose([x,y]),delimiter=',',fmt='%.4f') 
    f.close() 
    print("Saved!")
    
######################## data #################################################
example='Person_01/rec_1'
ampto=1000
cut_off_frequency = 30
######################## data #################################################

ECG_data,ECG_data_filtered,Sampling_rate = Read_signals_from_file(example,ampto)

LPF = Filtering_LPF(cut_off_frequency,Sampling_rate)
y = LPF.butter_filter(ECG_data)
x = np.linspace(0, len(ECG_data_filtered)/Sampling_rate, len(ECG_data_filtered), True)
Plot(x,y,"LPF filtered ECG data",'time (s)','Volt (mV)')
LPF.butter_example()
save_to_csv(x,y)

