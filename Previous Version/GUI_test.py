# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 17:46:03 2022

@author: yulep
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:28:24 2022

@author: yulep
"""

import csv
from tkinter import *
from random import randint
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
import tkinter as Tk
import PySimpleGUI as sg
import time
import numpy as np

def addPlot(canvasElement,fig):
    # create a set of axes on the figure
    ax = fig.add_subplot(1,1,1)
    canvas = canvasElement.TKCanvas
    # place the figure on the canvas
    figAgg = FigureCanvasTkAgg(fig, canvas)
    figAgg.draw()
    figAgg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return ax, figAgg

def updatePlot(x,y,ax,figAgg,ylabel,title,labels):
    ax.cla()
    for i in range(len(x)):
        ax.plot(x[i],y[i],label = labels[i])
    if len(x) > 1:
        ax.legend()
    ax.set_xlabel("time(s)") 
    ax.set_ylabel(ylabel) 
    ax.set_title(title)
    figAgg.draw()
    figAgg.flush_events()
    
def save_to_csv(x,y,title): 
    f=open(title,'w') 
    np.savetxt(f,np.transpose([x,y]),delimiter=',',fmt='%.4f') 
    f.close() 
    print("Saved!")

def open_csv():
    with open('pulse.csv') as csvDataFile: 
    # read file as csv file  
        csvReader = csv.reader(csvDataFile)
        wave = [] 
        pulse = [] 
        # append each row to data 
        for row in csvReader: 
            wave.append(int(row[0])) 
            pulse.append(float(row[1])) 
        return wave, pulse

def log():
    pass

def Main_GUI():
    
    ############# initial value #############
    sg_theme = sg.theme("Default1")
    text_size = 18
    last_time = 0
    ran = 1
    tranmission_stable = True
    total_heart_rate = []
    total_pulse_raw = []
    total_pulse_processed = []
    ploting_length = 5;
    ############# layout #############
    
    ############# initial value #############
    Column1 = sg.Column([
        [sg.Text("",font = ("Times New Roman",text_size))], 
        [sg.Canvas(size = (1280,800),key = "Pulse Canvas")],
        [sg.Text("No Value",key = "Tranmission Warning",
                 font = ("Times New Roman",text_size))],
        ])
    
    Column2 = sg.Column([
        [sg.Text("Heart Rate: {}".format(0),key = "Rate_number",
                 font = ("Times New Roman",text_size))], 
        [sg.Canvas(size = (1280,800),key = "Rate Canvas")],
        [sg.Text("No Value",key = "Heart_rate_warning",
                 font = ("Times New Roman",text_size))],
        ])
    
    layout = [
        [Column1,Column2],
        [sg.Text("Log",font = ("Times New Roman",16))],
        [sg.Listbox([],size = (60, 15),key = "Log"),
        sg.Button('Exit', key='EXIT_BUTTON',size = (5,2)),
         sg.Button('Save', key='Save_Button',size = (5,2))],
        ]
    
    window = sg.Window("Pulse Monitoring", layout, finalize=True,resizable=True)
    ############# layout #############
    
    
    ############# Canvas Windows #############
    fig_pulse = Figure()
    pulse_window = window["Pulse Canvas"]
    ax_pulse, figAgg_pulse = addPlot(pulse_window,fig_pulse)
    
    fig_rate = Figure()
    rate_window = window["Rate Canvas"]
    ax_rate, figAgg_rate = addPlot(rate_window,fig_rate)
    ############# Canvas Windows #############
    
    ############## text windows ##############
    rate_number_window = window["Rate_number"]
    rate_warning_window = window["Heart_rate_warning"]
    tranmission_warning_window = window["Tranmission Warning"]
    ############## text windows ##############
    
    log_window = window["Log"]
    
    while True:
        current_time = time.time()
        
        wave, pulse = open_csv()
        
        if current_time > last_time + 1:
            print(ran)
            last_time = current_time
            
            ##################### testing data #####################
            if ran < ploting_length + 1:
                y_pulse = wave[0:ran * 50]
                y_pulse = y_pulse + [0] * ((ploting_length - ran)*50)
                x_pulse = range(0,50 * ploting_length)
                y_rate = pulse[0:ran * 50]
                y_rate = y_rate + [0] * ((ploting_length - ran)*50)
                x_rate = range(0,50 * ploting_length)
                heart_rate_value = randint(45, 110)
                x_rate_average = np.linspace(0, ran * 50, 250)
                y_rate_average = []
                for i in range(250):
                    y_rate_average.append(randint(11, 12)/10)
            else:
                y_pulse = wave[(ran - ploting_length)*50:ran * 50]
                x_pulse = range((ran - ploting_length) * 50,ran*50)
                y_rate = pulse[(ran - ploting_length)*50:ran * 50]
                x_rate = range((ran - ploting_length) * 50,ran*50)
                heart_rate_value = randint(45, 110)
                x_rate_average = np.linspace((ran - ploting_length) * 50, ran * 50, 250)
                y_rate_average = []
                for i in range(250):
                    y_rate_average.append(randint(11, 12)/10)
            
            ##################### testing data #####################
            
            updatePlot([x_pulse],
                       [y_pulse],
                       ax_pulse,figAgg_pulse,
                       "Pulse Reading",
                       "Pulse Reading",
                       ["Pulse Reading"])
            updatePlot([x_rate,x_rate_average],
                       [y_rate,y_rate_average],
                       ax_rate,figAgg_rate,
                       "Heart Rate(beats/min)",
                       "Heart Rate",
                       ["Heart Rate","Average"])
            rate_number_window.update(value = "Heart Rate: {}".format(heart_rate_value))
            
            ##################### Heart Rate Warning #####################
            if heart_rate_value > 100:
                rate_warning_window.update(value = "Warning: Heart Rate Too High",  
                                           text_color = "Red")
            elif heart_rate_value < 50:
                rate_warning_window.update(value = "Warning: Heart Rate Too Low",  
                                           text_color = "Red")
            else:
                rate_warning_window.update(value = "Normal Heart Rate",  
                                           text_color = "Black")
            ##################### Heart Rate Warning #####################
            
            ##################### Tranmission Warning #####################
            if tranmission_stable:
                tranmission_warning_window.update(value = "Tranmission Stable",  
                                                  text_color = "Black")
            else:
                tranmission_warning_window.update(value = "Tranmission Unstable",  
                                                  text_color = "Red")
            ##################### Tranmission Warning #####################
            ran = ran + 1
            
        event, values = window.read(timeout=0.1)
        if event in ['EXIT_BUTTON', sg.WIN_CLOSED]:
            print("close")
            window.close()
            return
        elif event == 'Save_Button':
            pass
        else:
            pass

Main_GUI()