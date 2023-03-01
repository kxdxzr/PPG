##
## Read from a serial port and print received data.
## Set portName to be the name of teh serial port to be used.
##
## Author:  Greg Watkins
## Date:    10 Sep 2021
##

import serial
import time
import sys

serialString = ""  # Used to hold data coming over UART
portName = "COM5"          # PC format
#portName = "/dev/tty..."    # Mac format


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

    while 1:
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()
            data = serialString.decode("Ascii")
            data = data.replace("\r\n","")
            x = data.split(" ")
            #print(serialString)
            #print(data)
            print(x)
else:
    print("Exiting")
