# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 13:42:39 2022

@author: DELL
"""
import numpy as np
import matplotlib.pylab as plt

def transient(frequency,amplitude,test_filter):
    w = 2. * np.pi * frequency
    time_interval = 10000
    sample_rate = 5000
    samples = time_interval * sample_rate
    t = np.linspace(0, time_interval, int(samples))
    y = amplitude * np.sin(w * t)
    filtered_y = test_filter.butter_filter(y)
    plt.plot(t,filtered_y)
    plt.xlabel('Time(s)') 
    plt.ylabel('Amplitude(V)') 
    plt.title("Transient analysis") 
    plt.show()