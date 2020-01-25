from flask import Flask

app = Flask(__name__)


@app.route("/test/<int:printer_id>")
def run_test(printer_id):
    return "Hello World"


@app.route("/disable/<int:printer_id>")
def disable_printer(printer_id):
    return "disable %i" % (printer_id)


@app.route("/enable/<int:printer_id>")
def enable_printer(printer_id):
    return "enable %i" % (printer_id)


@app.route("/get-status/<int:printer_id>")
def get_status(printer_id):
    return "check on %i" % (printer_id)
