# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 16:31:16 2022

@author: Steve Yu
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
import sys
from datetime import datetime, date

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

def save_to_txt(data,title):
    f=open(title,'w')
    np.savetxt(f,data,delimiter=',',fmt='%s') 
    f.close() 

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

def Log(Info):
    time = datetime.now().strftime("%H:%M:%S")
    date_str = str(date.today())
    date_list = date_str.split("-")
    month_num = date_list[1]
    day = date_list[2]
    year = date_list[0]
    month_str = Months[month_num]
    weekday_int = datetime.today().weekday()
    weekday_str = weekdays[weekday_int]
    log_list.append("{} {} {} {} {}: {}".format(weekday_str, 
                                                   month_str, 
                                                   day, 
                                                   time, 
                                                   year, 
                                                   Info))
    log_window.update(values = log_list)
    #print(log_list)


log_list = []
raw_y_list = []
processed_y_list = []
pulse_x  = []
heart_rate_list = []
heart_rate_x = []

weekdays = {
  0: "Mon",
  1: "Tue",
  2: "Wed",
  3: "Thu",
  4: "Fri",
  5: "Sat",
  6: "Sun"
}

Months = {
  "01": "Jan",
  "02": "Feb",
  "03": "Mar",
  "04": "Apr",
  "05": "May",
  "06": "Jun",
  "07": "Jul",
  "08": "Jul",
  "09": "Aug",
  "10": "Oct",
  "11": "Nov",
  "12": "Dec",
}

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
        ])
    
    Column2 = sg.Column([
        [sg.Text("Heart Rate: {}".format(0),key = "Rate_number",
                 font = ("Times New Roman",text_size))], 
        [sg.Canvas(size = (1280,800),key = "Rate Canvas")],
        ])
    
    layout = [
        [Column1,Column2],
        [sg.Button('Exit', key='EXIT_BUTTON',size = (5,2)),
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
    ############## text windows ##############
    global log_window
    
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
            try:
                updatePlot([x_pulse],
                           [y_pulse],
                           ax_pulse,figAgg_pulse,
                           "Pulse Reading",
                           "Pulse Reading",
                           ["Pulse Reading"])
            except:
                for e in sys.exc_info():
                    print("  ",e)
                print("close")
                window.close()
            try:
                updatePlot([x_rate],
                           [y_rate],
                           ax_rate,figAgg_rate,
                           "Heart Rate(beats/min)",
                           "Heart Rate",
                           ["Heart Rate","Average"])
                rate_number_window.update(value = "Heart Rate: {}".format(heart_rate_value))
            except:
                for e in sys.exc_info():
                    print("  ",e)
                print("close")
                window.close()
            ran = ran + 1
            
        event, values = window.read(timeout=0.1)
        if event in ['EXIT_BUTTON', sg.WIN_CLOSED]:
            print("close")
            window.close()
            return
        elif event == 'Save_Button':
            Log("Data Saved")
            save_to_csv(pulse_x, raw_y_list, "Raw Data from sensor.csv")
            save_to_csv(pulse_x, processed_y_list, "Processed Data from sensor.csv")
            save_to_csv(heart_rate_x, heart_rate_list, "Heart Rate.csv")
            save_to_txt(log_list,"log.log")
        else:
            pass

Main_GUI()