from flask import Flask, request
import requests
import serial
import time
import json

from send_gcode_file import send_file
from setGPIO import set_pin
from readRFID import readRFID
from LCD_Control import LCD

app = Flask(__name__)

ser = None
red_LED = 20
green_LED = 21

@app.route("/test")
def run_test():
    send_file("test.gcode", "/dev/ttyUSB0")
    return "Sending"


@app.route("/disable")
def disable_printer():
    set_pin(red_LED, 0)
    set_pin(green_LED, 1)
    return "disabled"


@app.route("/enable")
def enable_printer():
    set_pin(red_LED, 1)
    set_pin(green_LED, 0)
    return "enabled"


@app.route("/status", methods=["GET"])
def status():
    if request.method == "GET":
        ser.write(str.encode("M27\n"))
        ts = time.time()
        result_string = ""
        while time.time() - ts < 3000:
            if ser.in_waiting > 0:
                ser.flushInput()
                serialString1 = ser.readline()
                serialString2 = ser.readline()
                serialString3 = ser.readline()
                decoded1 = serialString1.decode("Ascii")
                decoded2 = serialString2.decode("Ascii")
                decoded3 = serialString3.decode("Ascii")
                result_string = decoded1 + "\n" + decoded2 + "\n" + decoded3
                print(result_string)
                return result_string
        return "Thank you!"


@app.route("/RFID/<string:tag_id>")
def RFIDRecieved(tag_id):
    tag_id = "No Current User" if tag_id == "None" else tag_id
    print(tag_id)
    LCD(tag_id)
    r = requests.post("http://makermanage.holepunch.io/updateTrello", json={
        "user_name": tag_id,
        "printer": "Seattle Slew"
        }, timeout=5
    )
    print(r)
    return "Got it!"

if __name__ == "__main__":
    ser = serial.Serial("/dev/ttyUSB0", 250000)
    time.sleep(10)
    app.run(debug=True, port=8080)
    
ser.close()
