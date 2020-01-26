from readRFID import readRFID
import requests
import time

RFIDManagerURL = "http://localhost:8080/RFID/"

last_read = None;

while(True):
    id = readRFID()
    print(id)
    if last_read != id:
        print(id)
        URL = RFIDManagerURL + str(id)
        try:
            r = requests.get(url = URL, timeout=5)
        except:
            print("Sending RFID to Printer server failed")
            pass
    last_read = id
    time.sleep(1)
    