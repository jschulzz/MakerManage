from flask import Flask
from flask import request
import json

app = Flask(__name__)


@app.route("/trelloCallback", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        res = request.json
        change = res.get("action")
        change_type = change.get("type")
        # print(res.get("action").get("type"))
        if change_type == "addLabelToCard":
            print(json.dumps(change, indent=2))
    return "CallingBack"
