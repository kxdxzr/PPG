# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 12:36:56 2022

@author: Steve Yu
"""

def selection(data):
    ls = []
    ls.append(abs(data[0] - data[1]))
    ls.append(abs(data[0] - data[2]))
    ls.append(abs(data[1] - data[2]))
    position = ls.index(min(ls))
    if position == 2:
        return data[1]
    else:
        return data[0]