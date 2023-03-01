# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 14:41:02 2022

@author: yulep
"""

from C4 import Filtering_HPF
from C3 import Filtering_LPF
import wfdb
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter, freqz
import sys

class Filtering_BSF:
    "Create low-pass filters" 
    #Class variables 
    order = 6 #Butterworth filter order 
    fs = 30.0 #Sampling rate       
    frequency_high = 50 #cutoff frequency  
    frequency_low = 40
    high_pass = Filtering_HPF(frequency_high,fs)
    low_pass = Filtering_LPF(frequency_low,fs)
    
    def __init__(self,frequency_high,frequency_low,sampling_rate): 
        print('new BSF Created') 
        self.frequency_high = frequency_high
        self.frequency_low = frequency_low
        self.fs = sampling_rate
        self.high_pass = Filtering_HPF(self.frequency_high,self.fs)
        self.low_pass = Filtering_LPF(self.frequency_low,self.fs)
        #if self.frequency_high < self.frequency_low:
            #print("Error, cut-off frequency for HPF must be higher than LPF for a BSF")
            #sys.exit()
    
    def __del__(self): 
        print("BSF deleted") 
    
    
    def butter_filter(self,data):
        #butterworth filtering function, output is the filtered data 
        #get filter 
        y1 = self.high_pass.butter_filter(data)
        y2 = self.low_pass.butter_filter(data)
        y3 = y1 + y2
        return y3


######################## test #################################################

def Read_signals_from_file(example,sampto): 
    #A function to read ECG signals from Physionet file 
    index = example.find('/') #find index of / 
    length = len(example) #find length of example string 
    #use wfdb library function to extract ECG data from files 
    #readout = wfdb.rdsamp(example, 5000) 
    readout,attribute = wfdb.rdsamp(example[(index+1):length],sampto=sampto
                                    , pn_dir='ecgiddb/'+example[0:index])
    #Extract Raw ECG_data 
    ECG_data = readout[:,0] 
    #Extract Filtered ECG_data 
    ECG_data_filtered = readout[:,1] 
    #Extract Sampling rate 
    Sampling_rate = attribute['fs'] 
    #Return values 
    return ECG_data,ECG_data_filtered,Sampling_rate

def Plot(x,y,title): 
    #Plot ECG data #setup figure 
    fig = plt.figure(1) 
    #plot line graph with blue line and o marker 
    #plt.plot(x,y,color='b',marker='o') 
    plt.plot(x,y) 
    #set labels and title 
    plt.xlabel('time (s)') 
    plt.ylabel('Volt (mV)') 
    plt.title(title) 
    #show graph 
    plt.show()


######################## data #################################################
example='Person_01/rec_1'
ampto=1000
cut_off_frequency = 30
######################## data #################################################

ECG_data,ECG_data_filtered,Sampling_rate = Read_signals_from_file(example,ampto)

BSF = Filtering_BSF(40,60,Sampling_rate)


######################## test #################################################