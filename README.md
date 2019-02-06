The comments are written for Windows. For other operating system, there might be some differences.
It is written in Python 2.7. You need software to run the Python program. The most common is IDLE, but there are lots of others.

Before starting the program, you need to correct the COM port number!. You can find the COM port number under Device Manager. The COM port number goes to the line no. 19
ser = serial.Serial('COM4', baudrate=9600, bytesize=8)
When starting the program, it asks you duration of the test and sampling interval (both in seconds). Minimum sampling interval is 3 s. During test the program shows “test in progress…” and the data cannot be seen, except on instrument display. After the test is finished, the program saves the data in a file named by date and time. File is created in the same folder where the python file is.
