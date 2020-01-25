import serial
import time

ser = serial.Serial("COM4", 115200)
time.sleep(15)
# print("Sending")
filepath = "test.gcode"
with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
        print("Line {}: {}".format(cnt, line.strip()))
        ser.write(str.encode(line))
        line = fp.readline()
        cnt += 1

ser.close()
