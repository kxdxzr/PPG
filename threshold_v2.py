# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 20:03:14 2022

@author: Steve Yu
"""

def get_threshold(pulse_rate):
    threshold = max(pulse_rate) - (max(pulse_rate)-min(pulse_rate))*0.3
    i = 0
    below_threshold = True
    current = 0
    last = 0
    first = True
    while i < len(pulse_rate):
        if  pulse_rate[i] >= threshold and below_threshold:
            below_threshold = False
            last = current
            current = i
        elif pulse_rate[i] < threshold:
            below_threshold = True
        i += 1
    if current - last == 0:
        return 0
    period = (current - last)*0.02
    bpm = 60/period
    return bpm