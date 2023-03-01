# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 16:09:21 2022

@author: yulep
"""

import numpy as np
import matplotlib.pylab as plt
from AC_sweep import AC_sweep
from C4 import Filtering_HPF
from C3 import Filtering_LPF
from C5_2 import Filtering_BPF

BPF = Filtering_BPF(0.5,5,50)

ECG_data2 = BPF.butter_filter(ECG_data1)
