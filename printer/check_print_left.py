import serial
import time

ser = serial.Serial("COM8", 115200)
time.sleep(15)
# print("Sending")
filepath = "check_print_left.gcode"
with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
        print("Line {}: {}".format(cnt, line.strip()))
        ser.write(str.encode(line))
        line = fp.readline()
        cnt += 1

serialString = ""                           # Used to hold data coming over UART


while(1):

    # Wait until there is data waiting in the serial buffer
    if(ser.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        serialString = ser.readline()

        # Print the contents of the serial data
        print(serialString.decode('Ascii'))

		
ser.close()
