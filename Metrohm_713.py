# -*- coding: cp1252 -*-

import time
import datetime
import csv
import os
import serial

print ("Sisesta katse pikkus (sekundites):")
test_time = round(int(input()), 1)
print ("Sisesta mõõtmisintervall (sekundites, miinimumaeg 5 sek):")
sampling_rate = round(int(input()), 1)

today_string = datetime.datetime.today().strftime('%d-%m-%Y-%H-%M')
csvfile = "logi_" + today_string + ".txt"

ser = serial.Serial('/dev/tty.usbserial-1410', baudrate=9600, bytesize=8)

prev_sample_time = 0
test_in_progress = 1
time_between_samples = 0

def ask_log_data(sample_time_for_log):
    try:
        mesg = '&Config.PrintMeasVal $G\n'
        ser.write(mesg.encode('ascii'))
        time.sleep(0.01)
        metrohm_reading = ser.readline()
        metrohm_reading = metrohm_reading.strip().decode('ascii')
    except:
        print ('data error')
    try:
        log_sequence = [sample_time_for_log]
        log_reading = [metrohm_reading]
        log_sequence.extend(log_reading)
        with open(os.path.join(csvfile), 'a') as f:
            w = csv.writer(f)
            w.writerow(log_sequence)
    except:
        print ('logging error')

while test_in_progress == 1:
    print ('test in progress...')
    current_time = int(time.perf_counter())
    time_between_samples = current_time - prev_sample_time
    if int(time_between_samples) == sampling_rate:
        prev_sample_time = current_time
        current_time = int(time.perf_counter()) + sampling_rate
        sample_time_for_log = prev_sample_time
        ask_log_data(sample_time_for_log)
    if int(time.perf_counter()) >= test_time:
        print ('ending test...')
        test_in_progress = 0

