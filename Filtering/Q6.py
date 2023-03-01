# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 09:53:59 2022

@author: yulep
"""

#inputs with default values
import wfdb
import matplotlib.pyplot as plt
import numpy as np

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

def Plot(x,y,title,xlabel,ylabel): 
    #Plot ECG data #setup figure 
    fig = plt.figure(1) 
    #plot line graph with blue line and o marker 
    #plt.plot(x,y,color='b',marker='o') 
    plt.plot(x,y) 
    #set labels and title 
    plt.xlabel(xlabel) 
    plt.ylabel(ylabel) 
    plt.title(title) 
    #show graph 
    plt.show()


example='Person_01/rec_1'
ampto=1000
ECG_data,ECG_data_filtered,Sampling_rate = Read_signals_from_file(example,ampto)
x = np.linspace(0, len(ECG_data_filtered)/Sampling_rate, len(ECG_data_filtered), True)
Plot(x,ECG_data,"Filtered ECG data",'time (s)','Volt (mV)')

