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
from threading import Thread
from trello import TrelloClient
import json
import requests

from googleServer import getUserById


def getCardTypes():
    r = requests.get(
        "https://api.trello.com/1/boards/{}/customFields?key={}&token={}".format(
            BOARD_ID, API_KEY, API_TOKEN
        )
    )
    options = dict()
    card_types = list(filter(lambda x: x.get("id") == CARD_TYPE_FIELD_ID, r.json()))[
        0
    ].get("options")
    for c in card_types:
        options[c.get("id")] = c.get("value").get("text")
        return options


printerURL = "http://d576482d.ngrok.io"

app = Flask(__name__)
app.config["ENV"] = "development"

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/check", methods=["POST"])
def checkOn():
    if request.method == "POST":
        form = request.form
        printer_of_interest = form.get("text")
        callback_URL = form.get("response_url")

        def do_work():
            # do something that takes a long time
            try:
                r = requests.get(printerURL + "/status", timeout=5)
                print(r.text)
                r = requests.post(callback_URL, json={"text": r.text})
            except:
                pass

        thread = Thread(target=do_work)
        thread.start()
        return "Checking on {}!".format(printer_of_interest)


@app.route("/updateTrello", methods=["POST"])
def updateTrello():
    if request.method == "POST":
        data = request.json
        options = getCardTypes()
        r = requests.get(
            "https://api.trello.com/1/boards/{}/cards/?&key={}&token={}".format(
                BOARD_ID, API_KEY, API_TOKEN
            )
        )
        target_card = list(
            filter(lambda x: x.get("name") == data.get("printer"), r.json())
        )[0]
        target_card_id = target_card.get("id")
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

        name = data.get("user_name")
        if name != "No Current User":
            user = getUserById(name)
            name = user[0]

        print(name)
        updatedName = {"text": name}
        r = requests.put(
            "https://api.trello.com/1/card/{}/customField/{}/item".format(
                target_card_id, USER_FIELD_ID
            ),
            json={"value": updatedName, "key": API_KEY, "token": API_TOKEN},
        )
        if name == "Off Limits":
            print("Changing Labels")
            r = requests.delete(
                "https://api.trello.com/1/cards/{}/idLabels/{}?key={}&token={}".format(
                    target_card_id, GOOD_LABEL_ID, API_KEY, API_TOKEN
                )
            )

            r = requests.post(
                "https://api.trello.com/1/cards/{}/idLabels?value={}&key={}&token={}".format(
                    target_card_id, BAD_LABEL_ID, API_KEY, API_TOKEN
                )
            )
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
                r = requests.get(printerURL + "/disable")
                print(r)
            elif change_label.get("text") == "Functioning Normally":
                print(change_card.get("text") + " is back up and running!")
                r = requests.get(printerURL + "/enable")
                print(r)
    return "CallingBack"
