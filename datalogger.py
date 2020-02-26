# -*- coding: utf-8 -*-

# realtime data logger script by AKstudios
# Updated on 02/25/2020

from datetime import datetime
import time
from pathlib import Path

now = datetime.now()   # get current date/time
logging_start_time = now.strftime('%Y-%m-%d_%H%M%S')    # format datetime to use in filename
temp_data_dir = '/var/tmp'
data_dir = '/home/pi/heatflux/data'

time.sleep(10) # sleep 10 seconds to let data come in first

# function to find, parse, log data files
def logdata(_dt):
    try:
        file = open('%s/%s.csv' % (temp_data_dir, 'temp_heatflux'),'r')        # get data from file
        dataline = file.readline()
        file.close()
    except:
        pass

    # # parse data
    # data = []
    # try:
    #     for p in dataline.strip().split(","): #strip() removes trailing \n
    #         data.append(p)
    # except:
    #     pass

    # save data to file
    filename = '%s/%s_%s.csv' % (data_dir, 'heatflux', logging_start_time)
    my_file = Path(filename)
    if my_file.is_file():   # if file already exists, i.e., logging started
        try:
            file = open(filename,'a')   # open file in append mode
            file.write(str(_dt) + ',')   # write formatted datetime
            file.write(dataline)
            # file.write('\n')
            file.close()
        except:
            print ('Error: Failed to open file %s' % filename)
            pass

    else:   # file does not exist, write headers to it, followed by data. This should happen first time when creating file only
        try:
            file = open(filename,'w')   # open file in write mode
            file.write('Date/Time')
            for n in range(1,9):
                file.write(',')
                if n % 2 == 0:
                    file.write('Temperature (C) (Ch %d)' % int(n/2))
                else:
                    file.write('Heat Flux (W/m2) (Ch %d)' % round(n-n/2))
            file.write('\n')
            file.close()
        except:
            pass


# loop forever
while True:
     # this will log data every second
    for i in range(0,60):

        flag = None
        while flag is None:     # keep trying to match seconds with real time
            dt = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            second = datetime.now().strftime("%S")

            if int(second) == i:
                flag = 1
                break
            else:
                time.sleep(0.5)
                pass

        if int(second) == 0 and flag == 1:
            logdata(dt)
        else:
            pass

        time.sleep(0.1) # sleep script so the CPU is not bogged down
