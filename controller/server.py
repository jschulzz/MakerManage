from flask import Flask
from flask import request
import json

app = Flask(__name__)
app.config["ENV"] = "development"

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/trelloCallback", methods=["GET", "POST"])
def callback():
    if request.method == "POST":
        res = request.json
        change = res.get("action")
        change_type = change.get("type")
        change_label = change.get("display").get("entities").get("label")
        change_card = change.get("display").get("entities").get("card")
        # print(res.get("action").get("type"))
        if change_type == "addLabelToCard":
            print(json.dumps(change, indent=2))
            if change_label.get("text") == "Off Limits":
                print(change_card.get("text") + " is off limits")


    return "CallingBack"
