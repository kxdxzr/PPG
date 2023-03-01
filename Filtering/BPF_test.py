# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 17:54:15 2022

@author: DELL
"""

import numpy as np
import matplotlib.pylab as plt
from AC_sweep import AC_sweep
from C4 import Filtering_HPF
from C3 import Filtering_LPF
from C5_2 import Filtering_BPF
from C5 import Filtering_BSF

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

BSF = Filtering_BPF(0.5,10,50)

f = 50
w = 2. * np.pi * f
time_interval = 1
samples = 500
t = np.linspace(0, time_interval, samples)
print(len(t))
y = np.sin(w * t)
print(len(y))
filtered_y = BSF.butter_filter(y)
print(len(filtered_y))
Plot(t,y,"y")
Plot(t,filtered_y,"Filtered y")