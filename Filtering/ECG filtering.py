# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 14:48:33 2022

@author: Steve Yu
"""

from Q6 import Plot, Read_signals_from_file
import numpy as np
import matplotlib.pylab as plt
from AC_sweep import AC_sweep
from C4 import Filtering_HPF
from C3 import Filtering_LPF
from C5_2 import Filtering_BPF
from C5 import Filtering_BSF

def save_to_csv(x,y): 
    f=open('ECG_DATA_Challenge_6.csv','w') 
    np.savetxt(f,np.transpose([x,y]),delimiter=',',fmt='%.4f') 
    f.close() 
    print("Saved!")

example='Person_01/rec_1'
ampto=1000
ECG_data,ECG_data_filtered,Sampling_rate = Read_signals_from_file(example,ampto)

BPF = Filtering_BPF(0.1,40,Sampling_rate)
BSF = Filtering_BSF(60,40,Sampling_rate)

ECG_data1 = BSF.butter_filter(ECG_data)
ECG_data2 = BPF.butter_filter(ECG_data1)

x = np.linspace(0, len(ECG_data_filtered)/Sampling_rate, len(ECG_data_filtered), True)
Plot(x,ECG_data2,"Challenge 6 filtered ECG data",'time (s)','Volt (mV)')
save_to_csv(x,ECG_data2)