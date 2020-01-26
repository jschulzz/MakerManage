from flask import Flask
from flask import request
from secrets import (
    API_KEY,
    API_TOKEN,
    BOARD_ID,
    CARD_TYPE_FIELD_ID,
    USER_FIELD_ID,
    GOOD_LABEL_ID,
    BAD_LABEL_ID,
)
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
        card_types = list(
            filter(lambda x: x.get("id") == CARD_TYPE_FIELD_ID, r.json())
        )[0].get("options")
        for c in card_types:
            options[c.get("id")] = c.get("value").get("text")
        r = requests.get(
            "https://api.trello.com/1/boards/{}/cards/?&key={}&token={}".format(
                BOARD_ID, API_KEY, API_TOKEN
            )
        )
        target_card = list(
            filter(lambda x: x.get("name") == data.get("printer"), r.json())
        )[0]
        r = requests.get(
            "https://api.trello.com/1/cards/{}/?&key={}&token={}&customFieldItems=true".format(
                target_card.get("id"), API_KEY, API_TOKEN
            )
        )
        userField = list(
            filter(
                lambda x: x.get("idCustomField") == USER_FIELD_ID,
                r.json().get("customFieldItems"),
            )
        )[0]
        cardTypeField = list(
            filter(
                lambda x: x.get("idCustomField") == CARD_TYPE_FIELD_ID,
                r.json().get("customFieldItems"),
            )
        )[0]
        cardType = options[cardTypeField.get("idValue")]
        updatedName = {"text": data.get("name")}
        r = requests.put(
            "https://api.trello.com/1/card/{}/customField/{}/item".format(
                target_card.get("id"), USER_FIELD_ID
            ),
            json={"value": updatedName, "key": API_KEY, "token": API_TOKEN},
        )
        if data.get("name") == "Off Limits":
            print("Changing Labels")
            r = requests.delete(
                "https://api.trello.com/1/cards/{}/idLabels/{}?key={}&token={}".format(
                    target_card.get("id"), GOOD_LABEL_ID, API_KEY, API_TOKEN
                )
            )

            r = requests.post(
                "https://api.trello.com/1/cards/{}/idLabels?value={}&key={}&token={}".format(
                    target_card.get("id"), BAD_LABEL_ID, API_KEY, API_TOKEN
                )
            )
            print(r)
    return ""


@app.route("/trelloCallback", methods=["GET", "POST"])
def callback():
    if request.method == "POST":
        res = request.json
        change = res.get("action")
        change_type = change.get("type")
        change_label = change.get("display").get("entities").get("label")
        change_card = change.get("display").get("entities").get("card")
        if change_type == "addLabelToCard":
            if change_label.get("text") == "Off Limits":
                print(change_card.get("text") + " is off limits")
            elif change_label.get("text") == "Functioning Normally":
                print(change_card.get("text") + " is back up and running!")

    return "CallingBack"
