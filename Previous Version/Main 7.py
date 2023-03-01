
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
from datetime import datetime, date
import serial
import sys
import matplotlib.pylab as plt
from C4 import Filtering_HPF
from C3 import Filtering_LPF
from C5_2 import Filtering_BPF
import pandas as pd
from numpy.fft import fft, ifft
from FFT import FFT

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
    # generate time
    
    log_list.append("{} {} {} {} {}: {}".format(weekday_str, 
                                                   month_str, 
                                                   day, 
                                                   time, 
                                                   year, 
                                                   Info))
    # add new GUI including time and information
    
    log_window.update(values = log_list, scroll_to_index = len(log_list))
    #print(log_list)
    # update the window

######################### Signal Processing #########################
def moving_averages(pulse_rate, samples_per_second):

    i = 0
    window = 0

    #Find the number of samples in the last 15 seconds and round to 0 decimal places
    number_samples = samples_per_second*15
    number_samples = round(number_samples)

    #Find length of the pulse rate array
    len_pulse_rate = len(pulse_rate)
    
    #If there arent enough values for moving average print 0
    if len(pulse_rate) < number_samples:

        #Create a new list containing only the data from the last 15 seconds
        #Calculate length of list
        moving_pulse_rate = pulse_rate[0:len_pulse_rate]
        length_moving_pulse_rate = len(moving_pulse_rate)

        #Loop through the list to find total of the last 15 seconds
        while i < length_moving_pulse_rate:
            current_value = moving_pulse_rate[i]
            window = window + current_value
            i = i + 1
       #Calculate Moving Average
        moving_average = window/length_moving_pulse_rate
        
        
    #If there are enough values for moving average print print it
    elif len(pulse_rate) >= number_samples:

        #Create a new list containing only the data from the last 15 seconds
        #Calculate length of list
        moving_pulse_rate = pulse_rate[(len_pulse_rate-number_samples):len_pulse_rate]
        length_moving_pulse_rate = len(moving_pulse_rate)

        #Loop through the list to find total of the last 15 seconds
        while i < length_moving_pulse_rate:
            current_value = moving_pulse_rate[i]
            window = window + current_value
            i = i + 1
       #Calculate Moving Average
        moving_average = window/number_samples

    return moving_average

######################### Signal Processing #########################


log_list = []
pulse_x  = []
heart_rate_list = []
heart_rate_x = []
moving_average = []
BPF = Filtering_LPF(10,50)

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

serialString = ""  # Used to hold data coming over UART
portName = "COM5"          # PC format

# define the serial port.
# specify parameters as needed
serialPort = serial.Serial()
serialPort.port=portName
serialPort.baudrate=115200
serialPort.bytesize=8
serialPort.timeout=2
serialPort.stopbits=serial.STOPBITS_ONE


# open the port
try:
    serialPort.open()
except:
     print("Port open failed: " + portName)
     for e in sys.exc_info():
         print("  ",e)
    
if serialPort.isOpen():
    print("**************************************")
    print("** Serial port opened: {}".format(portName))
    print("**************************************")

def Main_GUI():
    
    ############# initial value #############
    sg_theme = sg.theme("Default1")
    text_size = 18
    last_time = 0
    ran = 1
    tranmission_stable = True
    raw_y_list = []
    processed_y_list = []
    ploting_length = 5;
    raw_y_list = []
    high_warning = 100
    low_warning = 50
    Pulse_Ploting = "Processed"
    ############# layout #############
    
    ############# initial value #############
    Column1 = sg.Column([
        [sg.Text("",font = ("Times New Roman",text_size))], 
        [sg.Canvas(size = (640,400),key = "Pulse Canvas")],
        [sg.Spin(["Raw & Processed","Processed","Raw"],
                 size = (30,30),
                 enable_events=True,
                 key = "Pulse_Ploting",
                 initial_value = "Processed"),
         sg.Text("No Value",key = "Tranmission Warning",
                 font = ("Times New Roman",text_size))],
        ])
    
    Column2 = sg.Column([
        [sg.Text("Heart Rate: {}".format(0),key = "Rate_number",
                 font = ("Times New Roman",text_size))], 
        [sg.Canvas(size = (640,400),key = "Rate Canvas")],
        [sg.Image(filename = 'green1.png', 
                  size=(30,30), key="Rate_Warning_Light"),
         sg.Text("No Value",key = "Heart_rate_warning",
                 font = ("Times New Roman",text_size))],
        ])
    Column3 = sg.Column([
        [sg.Text("High warning slider",
                 font = ("Times New Roman",16))], 
        [sg.Slider(range = (80,120),default_value = high_warning, 
                   key = "high_warning_slider",enable_events=True,
                   orientation = 'h',size=(70,20))],
        [sg.Text("low warning slider",
                 font = ("Times New Roman",16))], 
        [sg.Slider(range = (30,70),default_value = low_warning, 
                   key = "low_warning_slider",enable_events=True,
                   orientation = 'h',size=(70,20))],
        ])
    Column4 = sg.Column([
        [sg.Button('Exit', key='EXIT_BUTTON',size = (5,2))],
        [sg.Button('Save', key='Save_Button',size = (5,2))],
        ])
    layout = [
        [Column1,Column2],
        [sg.Text("Log",font = ("Times New Roman",16))],
        [sg.Listbox([],size = (60, 15),key = "Log"),
         Column3,Column4],
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
    rate_light_window = window["Rate_Warning_Light"]
    tranmission_warning_window = window["Tranmission Warning"]
    ############## text windows ##############
    global log_window
    log_window = window["Log"]
    
    while True:
        current_time = time.time()
        
        #wave, pulse = open_csv()
        if current_time > last_time + 1:
            if serialPort.in_waiting > 0:
                # Read data out of the buffer until a carraige return / new line is found
                serialString = serialPort.readline()
                data = serialString.decode("Ascii")
                data = data.strip()
                x = data.split(" ")
                #print(x)
                print(data)
                current_rate = float(x[1])
                current_pulse = x[2:]
                rescurrent_pulse = [int(i) for i in current_pulse]
                raw_y_list = raw_y_list + rescurrent_pulse
                BPF_processed_data = BPF.butter_filter(raw_y_list[-100:])
                #processed_y_list = BPF.butter_filter(raw_y_list[-100:]).tolist()
                processed_y_list = processed_y_list + BPF_processed_data.tolist()[-50:]
                heart_rate_list.append(current_rate)
                print(FFT(processed_y_list[-750:],50))
                print(ran)
                last_time = current_time
                
                ##################### Processing data #####################
                if ran < ploting_length:
                    y_test = raw_y_list[0:ran * 50]
                    y_test = y_test + [0] * ((ploting_length - ran)*50)
                    y_pulse = processed_y_list[0:ran * 50]
                    y_pulse = y_pulse + [0] * ((ploting_length - ran)*50)
                    x_pulse = np.arange(0, ploting_length, 0.02)
                    y_rate = heart_rate_list[0:ran]
                    y_rate = y_rate + [0] * ((ploting_length - ran))
                    x_rate = np.arange(0, ploting_length, 1)
                    heart_rate_value = current_rate
                else:
                    y_test = raw_y_list[(ran - ploting_length)*50:ran * 50]
                    y_pulse = processed_y_list[(ran - ploting_length)*50:ran * 50]
                    x_pulse = np.arange(ran - ploting_length, ran, 0.02)
                    y_rate = heart_rate_list[(ran - ploting_length):ran]
                    x_rate = np.arange(ran - ploting_length+1, ran+1, 1)
                    heart_rate_value = current_rate
                if ran < ploting_length:
                    x_rate_average = np.linspace(0, ploting_length-1, ploting_length)
                    moving_average.append(moving_averages(heart_rate_list,1))
                    y_rate_average = moving_average[0:ran]
                    y_rate_average = y_rate_average + [0] * ((ploting_length - ran))
                else:
                    x_rate_average = np.linspace((ran - ploting_length + 1) , 
                                                 ran, 
                                                 ploting_length)
                    result = moving_averages(heart_rate_list, 1)
                    moving_average.append(result)
                    y_rate_average = moving_average[(ran - ploting_length):ran]
                ##################### Processing data #####################
                if Pulse_Ploting == "Processed":
                    updatePlot([x_pulse],
                               [y_pulse],
                               ax_pulse,figAgg_pulse,
                               "Pulse Reading",
                               "Pulse Reading",
                               ["Pulse Reading"])
                elif Pulse_Ploting == "Raw & Processed":
                    updatePlot([x_pulse,x_pulse],
                               [y_test,y_pulse],
                               ax_pulse,figAgg_pulse,
                               "Pulse Reading",
                               "Pulse Reading",
                               ["Raw","Processed Reading"])
                else:
                    updatePlot([x_pulse],
                               [y_test],
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
                rate_number_window.update(value = "Heart Rate: {}"
                                          .format(heart_rate_value))
                    
                
                ##################### Heart Rate Warning #####################
                if heart_rate_value > high_warning:
                    rate_warning_window.update(value = "Warning: Heart Rate Too High",  
                                               text_color = "Red")
                    rate_light_window.update(filename = "Red1.png",size = (30,30))
                    Log("Pulse High")
                elif heart_rate_value < low_warning:
                    rate_warning_window.update(value = "Warning: Heart Rate Too Low",  
                                               text_color = "Red")
                    rate_light_window.update(filename = "Red1.png",size = (30,30))
                    Log("Pulse Low")
                else:
                    rate_warning_window.update(value = "Normal Heart Rate",  
                                               text_color = "Black")
                    rate_light_window.update(filename = "Green1.png",size = (30,30))
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
            
            ##################### GUI Handling #####################
            event, values = window.read(timeout=0.1)
            if event in ['EXIT_BUTTON', sg.WIN_CLOSED]:
                Log("Exiting")
                save_to_txt(log_list,"log.log")
                print("close")
                serialPort.close()
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
            elif event == "high_warning_slider":
                high_warning = values["high_warning_slider"]
                #Log("High Heart Rate Warning set to: {}".format(high_warning))
            elif event == "low_warning_slider":
                low_warning = values["low_warning_slider"]
                #Log("Low Heart Rate Warning set to: {}".format(low_warning))
            elif event == "Pulse_Ploting":
                Pulse_Ploting = values["Pulse_Ploting"]
            else:
                pass
            ##################### GUI Handling #####################

Main_GUI()