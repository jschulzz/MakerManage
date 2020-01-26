from readRFID import readRFID
from flask import Flask
from LCD_Control import LCD

app = Flask(__name__)

@app.route("/RFID/<string:tag_id>")
def RFIDRecieved(tag_id):
    print(tag_id)
    LCD(tag_id)
    return "Got it!"


if __name__ == "__main__":
    app.run(debug=True, port=8080)