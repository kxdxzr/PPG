# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 16:20:41 2022

@author: DELL
"""
import numpy as np
import matplotlib.pylab as plt
from AC_sweep import AC_sweep
from C4 import Filtering_HPF
from C3 import Filtering_LPF
from C5_2 import Filtering_BPF
from C5 import Filtering_BSF

sample_rate = 50

# generate filter
current_filter = Filtering_BPF(0.5,10,sample_rate)
# input into test
start_frequency = 0.01
stop_frequency = 25
points = 100
AC_sweep(start_frequency,stop_frequency,points,current_filter,sample_rate)
