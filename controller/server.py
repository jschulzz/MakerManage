from flask import Flask
from flask import request
from secrets import API_KEY, API_TOKEN, BOARD_ID, CARD_TYPE_FIELD_ID, USER_FIELD_ID
from trello import TrelloClient
import json
import requests

app = Flask(__name__)
app.config["ENV"] = "development"

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/updateTrello", methods=["POST"])
def updateTrello():
    if request.method == "POST":
        ###{
        ###     name
        ###     printer
        ###}
        ###
        data = request.json
        r = requests.get(
            "https://api.trello.com/1/boards/{}/customFields?key={}&token={}".format(
                BOARD_ID, API_KEY, API_TOKEN
            )
        )
        options = dict()
        card_types = list(filter(lambda x: x.get("id") == CARD_TYPE_FIELD_ID, r.json()))[0].get("options")
        for c in card_types:
            options[c.get("id")] = c.get("value").get("text")
        print(json.dumps(r.json(), indent=2))
        r = requests.get(
            "https://api.trello.com/1/boards/{}/cards/?&key={}&token={}".format(
                BOARD_ID, API_KEY, API_TOKEN
            )
        )
        target_card = list(filter(lambda x: x.get("name") == data.get("printer"), r.json()))[0]
        r = requests.get(
            "https://api.trello.com/1/cards/{}/?&key={}&token={}&customFieldItems=true".format(
                target_card.get("id"), API_KEY, API_TOKEN
            )
        )
        print(json.dumps(r.json(), indent=2))
        userField = list(filter(lambda x: x.get("idCustomField") == USER_FIELD_ID, r.json().get("customFieldItems")))[0]
        cardTypeField = list(filter(lambda x: x.get("idCustomField") == CARD_TYPE_FIELD_ID, r.json().get("customFieldItems")))[0]
        cardType = options[cardTypeField.get("idValue")]
        print(cardType)
    return ""


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
