
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

######################### Plotting #########################
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
######################### Plotting #########################
    
  
######################### Saving #########################

def save_to_csv(x,y,title): 
    f=open(title,'w') 
    np.savetxt(f,np.transpose([x,y]),delimiter=',',fmt='%.4f') 
    f.close() 

def save_to_txt(data,title):
    f=open(title,'w')
    np.savetxt(f,data,delimiter=',',fmt='%s') 
    f.close() 

######################### Saving #########################

######################### Testing Data #########################
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

######################### Testing Data #########################

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

######################### Signal Processing #########################
def moving_averages(pulse_rate, samples_per_second):

    i = 0

    #Empty list to store moving averages
    moving_averages = []

    #Find the number of samples in the last 15 seconds and round to 0 decimal places
    number_samples = samples_per_second*15
    number_samples = round(number_samples)
    
    #Create a new list containing only the data from the last 15 seconds
    moving_pulse_rate = pulse_rate[-number_samples:-1]
    
    #Create a loop to go through the array and calculate the moving average of each with each window size being the number of samples in a second
    while i < len(moving_pulse_rate) - samples_per_second + 1:
        window = moving_pulse_rate[i : i + samples_per_second]
        window_average = sum(window)/samples_per_second
        moving_averages.append(window_average)
        i = i + 1

    return moving_averages

######################### Signal Processing #########################


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
    ploting_length = 15;
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
    global log_window
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
                x_rate_average = np.linspace(0, ran * 50, ploting_length * 50)
                y_rate_average = []
                for i in range(ploting_length * 50):
                    y_rate_average.append(0)
            else:
                y_pulse = wave[(ran - ploting_length)*50:ran * 50]
                x_pulse = range((ran - ploting_length) * 50,ran*50)
                y_rate = pulse[(ran - ploting_length)*50:ran * 50]
                x_rate = range((ran - ploting_length) * 50,ran*50)
                heart_rate_value = randint(45, 110)
                x_rate_average = np.linspace((ran - ploting_length + 1) 
                                             * 50, ran * 50, 50 
                                             * (ploting_length - 1))
                y_rate_average = moving_averages(y_rate, 50)
            
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
                updatePlot([x_rate,x_rate_average],
                           [y_rate,y_rate_average],
                           ax_rate,figAgg_rate,
                           "Heart Rate(beats/min)",
                           "Heart Rate",
                           ["Heart Rate","Average"])
                rate_number_window.update(value = "Heart Rate: {}"
                                          .format(heart_rate_value))
            except:
                for e in sys.exc_info():
                    print("  ",e)
                print("close")
                window.close()
                
            
            ##################### Heart Rate Warning #####################
            if heart_rate_value > 100:
                rate_warning_window.update(value = "Warning: Heart Rate Too High",  
                                           text_color = "Red")
                Log("Pulse High")
            elif heart_rate_value < 50:
                rate_warning_window.update(value = "Warning: Heart Rate Too Low",  
                                           text_color = "Red")
                Log("Pulse Low")
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
                Log("Tranmission Unstable")
            ##################### Tranmission Warning #####################
            ran = ran + 1
            
        event, values = window.read(timeout=0.1)
        if event in ['EXIT_BUTTON', sg.WIN_CLOSED]:
            Log("Exiting")
            save_to_txt(log_list,"log.log")
            print("close")
            window.close()
            return
        elif event == 'Save_Button':
            Log("Data Saved")
            save_to_csv(pulse_x, raw_y_list, 
                        "Raw Data from sensor.csv")
            save_to_csv(pulse_x, processed_y_list, 
                        "Processed Data from sensor.csv")
            save_to_csv(heart_rate_x, heart_rate_list, 
                        "Heart Rate.csv")
            save_to_txt(log_list,"log.log")
        else:
            pass

Main_GUI()