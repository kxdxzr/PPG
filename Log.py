# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 14:38:22 2022

@author: Steve Yu
"""

from datetime import datetime, date

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
    #log_window.update(values = log_list)
    print(log_list)

log_list = []

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

Log("Test1")
Log("Test2")
Log("Test3")