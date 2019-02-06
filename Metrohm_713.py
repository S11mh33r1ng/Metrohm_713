# -*- coding: cp1252 -*-

import threading
import time
import datetime
import csv
import os
import serial
import sys

print "Insert test duration (in seconds):"
test_time = round(int(raw_input()), 1)
print "Insert sampling interval (in seconds):",
sampling_rate = round(int(raw_input()), 1)

today_string = datetime.datetime.today().strftime('%d-%m-%Y-%H-%M')
csvfile = "data_" + today_string + ".txt"

ser = serial.Serial('COM4', baudrate=9600, bytesize=8)

measurement_start_time = round(time.clock(),1)

prev_sample_time = 0.0
test_in_progress = 1
time_between_samples = 0
test_over = 0

def ask_log_data(sample_time_for_log):
    try:
        mesg = '&Config.PrintMeasVal $G\n'
        ser.write(mesg.encode('ascii'))
        time.sleep(0.01)
        metrohm_reading = ser.readline()
        metrohm_reading = metrohm_reading.strip()
        #print metrohm_reading
    except:
        print 'data error'
    try:
        log_sequence = [sample_time_for_log]
        log_reading = [metrohm_reading]
        log_sequence.extend(log_reading)
        #print log_sequence
        with open(os.path.join(csvfile), 'a') as f:
            w = csv.writer(f)
            w.writerow(log_sequence)
    except:
        print 'logging error'
    
def measuring_test_time():
    global measurement_start_time
    global test_time
    global test_in_progress
    global test_has_lasted
    global test_over
    while test_over == 0:
        try:
            test_has_lasted = round(time.clock(),1) - measurement_start_time
            print 'test in progress...'
            if test_has_lasted == test_time:
                print 'ending test...'
                test_in_progress = 0
                test_over = 1
        except:
            return
        
def measuring_sampling_time():
    global start_measurement
    global sampling_rate
    global test_in_progress
    global test_has_lasted
    global prev_sample_time
    while test_over == 0:
        try:
            if test_in_progress == 1:
                current_time = round(time.clock(), 1)
                time_between_samples = current_time - prev_sample_time
                if time_between_samples == sampling_rate:
                    prev_sample_time = current_time
                    current_time = round(time.clock(),1) + sampling_rate
                    sample_time_for_log = prev_sample_time
                    ask_log_data(sample_time_for_log)
        except:
            print 'sample measuring error'

def main():
    ask_log_data(prev_sample_time)
    proc1 = threading.Thread(target = measuring_test_time)
    proc2 = threading.Thread(target = measuring_sampling_time)
    
    proc2.start()
    proc1.start()

    proc2.join()
    proc1.join()

if __name__ == '__main__':
    main()
