from readRFID import readRFID
from flask import Flask

app = Flask(__name__)

@app.route("/RFID/<int:tag_id>")
def RFIDRecieved(tag_id):
    print(tag_id)
    return "Got it!"


if __name__ == "__main__":
    app.run(debug=True, port=8080)