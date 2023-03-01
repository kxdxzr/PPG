# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 14:25:19 2022

@author: yulep
"""

from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
import numpy as np

class Filtering_HPF: 
    "Create High-pass filters" 
    #Class variables 
    order = 3 #Butterworth filter order 
    fs = 30.0 #Sampling rate       
    cutoff = 3.667 #cutoff frequency  
     
    #Will be executed on new instance initialisation 
    def __init__(self,frequency,sampling_rate): 
        print('new HPF Created') 
        self.cutoff = frequency 
        self.fs = sampling_rate 
         
    #Will be executed on instance delete     
    def __del__(self): 
        print("HPF deleted") 
 
    #Butterworth filter functions#====================================================================== 
    def butter_highpass(self): 
        #get nyquist frequency 
        nyq = 0.5 * self.fs  
        #normalise cutoff frequency 
        normal_cutoff = self.cutoff / nyq 
        #get butterworth filter parameters using spicy.signal 
        b, a = butter(self.order, normal_cutoff, btype='high', analog=False) 
        return b, a 
    
    def butter_filter(self,data):
        #butterworth filtering function, output is the filtered data 
        b, a = self.butter_highpass() 
        #get filter 
        y = lfilter(b, a, data) 
        return y
    
    def butter_example(self): 
        #plot butterworth filter frequency response and filtering example 
         
        #get butterworth filter parameters 
        b, a = self.butter_highpass() 
     
        #Plotting the frequency response 
        w, h = freqz(b, a, worN=8000) 
        plt.subplot(2, 1, 1) 
        plt.plot(0.5*self.fs*w/np.pi, np.abs(h), 'b') 
        plt.plot(self.cutoff, 0.5*np.sqrt(2), 'ko') 
        plt.axvline(self.cutoff, color='k') 
        plt.xlim(0, 0.5*self.fs) 
        plt.title("Highpass Filter Frequency Response") 
        plt.xlabel('Frequency [Hz]') 
        plt.grid() 
     
        #Example 
        #Creating the data for filteration 
        T = 0.5         #value taken in seconds 
        n = int(T * self.fs) #indicates total samples 
        t = np.linspace(0, T, n, endpoint=False) 
         
        data = np.sin(2*2*np.pi*t) + 1.5*np.cos((self.fs/2-50)*2*np.pi*t) 
         
        #Filtering and plotting 
        y = self.butter_filter(data) 
         
        plt.subplot(2, 1, 2) 
        plt.plot(t, data, 'b-', label='data') 
        plt.plot(t, y, 'g-', linewidth=2, label='filtered data') 
        plt.xlabel('Time [sec]') 
        plt.grid() 
        plt.legend() 
         
        plt.subplots_adjust(hspace=0.35) 
        plt.show() 