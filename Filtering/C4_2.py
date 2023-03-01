# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 14:29:20 2022

@author: yulep
"""
from C4 import Filtering_HPF
import wfdb
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter, freqz

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

######################## data #################################################
example='Person_01/rec_1'
ampto=1000
cut_off_frequency = 30
######################## data #################################################

ECG_data,ECG_data_filtered,Sampling_rate = Read_signals_from_file(example,ampto)
high_pass = Filtering_HPF(cut_off_frequency,Sampling_rate)
high_pass.butter_example()