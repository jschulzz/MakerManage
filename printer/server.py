from flask import Flask, request
import requests
import serial
import time
import json
from threading import Thread

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
    def do_work():
        send_file("test.gcode", "/dev/ttyACM0")

    thread = Thread(target=do_work)
    thread.start()
    return "Sending Test Print"


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
        print("Pulling Current USB Stream!")
        ser.flushInput()
        while time.time() - ts < 3:
            print(time.time() - ts)
            print("In time range")
            if ser.in_waiting > 0:
                print("Something was in Serial")
                serialString1 = ser.readline()
                decoded1 = serialString1.decode("Ascii")
                print(decoded1)
                serialString2 = ser.readline()
                decoded2 = serialString2.decode("Ascii")
                serialString3 = ser.readline()
                decoded3 = serialString3.decode("Ascii")
                result_string = decoded1 + "\n" + decoded2 + "\n" + decoded3
                print(result_string)
                return result_string
        print("Thank you")
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
    ser = serial.Serial("/dev/ttyACM0", 115200)
    time.sleep(10)
    app.run(debug=True, port=8080)
    
ser.close()
