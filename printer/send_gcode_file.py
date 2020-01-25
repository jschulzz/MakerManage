

def send_file(filename, port):

    import serial
    import time
    
    ser = serial.Serial(port, 250000)
    time.sleep(10)
    with open(filename) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            print("Line {}: {}".format(cnt, line.strip()))
            ser.write(str.encode(line))
            line = fp.readline()
            cnt += 1

    ser.close()
