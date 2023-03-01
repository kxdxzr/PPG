# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 16:12:52 2022

@author: Steve Yu

Note this AC sweep can not sweep over half of the sampling rate because of it 
is discrete.
"""
import numpy as np
import matplotlib.pylab as plt

def AC_sweep(start_frequency,stop_frequency,points,test_filter,sample_rate):
    response = []
    frequency = []
    current_frequency = start_frequency
    freq = 0.000001
    last_freq = start_frequency
    while current_frequency <= stop_frequency:
        while current_frequency > freq:
            last_freq = freq
            freq = 10 * freq # decade
        # calculate the value that needs to be add to the frequency each loop
        gap = (freq - last_freq)/(points - 1)
        f = current_frequency
        frequency.append(f)
        # generate a sine wave of certain frequency
        w = 2. * np.pi * f
        time_interval = 1000
        samples = time_interval * sample_rate
        t = np.linspace(0, time_interval, samples)
        y = np.sin(w * t)
        # filter the data
        filtered_y = test_filter.butter_filter(y)
        # convert the result into dB and record, record the largest value for
        # the second half the wave as the first few cycles are not totally
        # filtered
        response.append(20*np.log10(max(filtered_y[len(filtered_y)//2:])))
        current_frequency += gap
    # plot the result
    plt.plot(frequency,response)
    plt.xlabel('Frequency(Hz)') 
    plt.xscale('log')
    plt.ylabel('dB') 
    plt.title("AC Sweep") 
    plt.show()