from flask import Flask
from send_gcode_file import send_file
from setGPIO import set_pin

app = Flask(__name__)


@app.route("/test/<int:printer_id>")
def run_test(printer_id):
    send_file("test.gcode", "/dev/ttyUSB0")
    return "Sending"


@app.route("/disable/<int:printer_id>")
def disable_printer(printer_id):
    set_pin(2, 0)
    return "disable %i" % (printer_id)


@app.route("/enable/<int:printer_id>")
def enable_printer(printer_id):
    set_pin(2, 0)
    return "enable %i" % (printer_id)


@app.route("/get-status/<int:printer_id>")
def get_status(printer_id):
    return "check on %i" % (printer_id)
