# -*- coding: utf-8 -*-

# This script initializes Fluxteq's Compaq DAQ,
# reads data from serial port and saves to temporary file

# Developed by Akram Ali
# Updated on: 02/25/2020

import time
import serial
import os

number_of_sensors = '4'
sensitivities = ['1.39', '1.31', '1.29', '1.32']
temp_data_dir = '/var/tmp/temp_heatflux'

# initialize serial port
try:
    serialport = serial.Serial('/dev/ttyUSB0', 9600, timeout=2) # make sure baud rate is the same
except serial.SerialException:
    print('Serial Port Failed.')
    while True:     # loop forever
        pass

time.sleep(3)  # wait few seconds till serial port initialized

# send initial configuration to the DAQ to begin logging
try:
    serialport.write(number_of_sensors)
    time.sleep(1.5)
    for n in range(int(number_of_sensors)):
        serialport.write(sensitivities[n])
        time.sleep(1.5)
except:
    print('Failed to write data')
    pass

time.sleep(1)

# loop forever
while True:
    data = serialport.read(1)   # get first byte from serial port
    n = serialport.in_waiting   # check remaining number of bytes
    if n:    # wait till data arrives and then read it
        data = data + serialport.readline()    # read one line and merge with first byte
        try:
            file = open('%s.csv' % temp_data_dir,'w')
            file.write(data)     # save data in a temp csv file
            file.close()
        except:
            pass
    else:
        continue    # ignore bad packets or no data received

    time.sleep(0.01)    # wait a bit so CPU doesn't choke to def