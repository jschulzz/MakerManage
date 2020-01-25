from flask import Flask, jsonify
import serial
import time

app = Flask(__name__)

ser = None


@app.route("/status")
def getStatus():
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


@app.route("/lockout")
def lockout():
    ser.write(str.encode("M22\n"))


if __name__ == "__main__":
    ser = serial.Serial("COM6", 115200)
    time.sleep(10)
    print("Connected")
    app.run(debug=False)

ser.close()
