# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 13:44:36 2022

@author: DELL
"""

import numpy as np
import matplotlib.pylab as plt
from Transient import transient
from C4 import Filtering_HPF
from C3 import Filtering_LPF
from C5_2 import Filtering_BPF
from C5 import Filtering_BSF


current_filter = Filtering_BPF(0.1,40,5000)

frequency = 30
amplitude = 1
test_filter = current_filter
transient(frequency,amplitude,test_filter)