# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 20:57:41 2022

@author: DELL
"""

from C4 import Filtering_HPF
from C3 import Filtering_LPF
import wfdb
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter, freqz
import sys

class Filtering_BPF:
    "Create band-pass filters" 
    #Class variables 
    order = 6 #Butterworth filter order 
    fs = 30.0 #Sampling rate       
    frequency_high = 40 #cutoff frequency for HPF
    frequency_low = 50 #cutoff frequency for LPF
    high_pass = Filtering_HPF(frequency_high,fs)
    low_pass = Filtering_LPF(frequency_low,fs)
    
    def __init__(self,frequency_high,frequency_low,sampling_rate): 
        print('new BPF Created') 
        self.frequency_high = frequency_high
        self.frequency_low = frequency_low
        self.fs = sampling_rate 
        self.high_pass = Filtering_HPF(self.frequency_high,self.fs)
        self.low_pass = Filtering_LPF(self.frequency_low,self.fs)
        #if self.frequency_high > self.frequency_low:
            #print("Error, cut-off frequency for HPF must be lower than LPF for a BPF")
            #sys.exit()
        
    def __del__(self): 
        print("BPF deleted") 
    
    
    def butter_filter(self,data):
        #butterworth filtering function, output is the filtered data 
        #get filter 
        y1 = self.high_pass.butter_filter(data)
        y2 = self.low_pass.butter_filter(y1)
        return y2