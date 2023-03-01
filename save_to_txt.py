# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 16:37:05 2022

@author: Steve Yu
"""
import numpy as np

def save_to_txt(data,title):
    f=open(title,'w')
    np.savetxt(f,data,delimiter=',',fmt='%s') 
    f.close() 
    

data = [1,2,3,4,5]
save_to_txt(data,"test_txt.txt")