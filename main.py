from flask import Flask, render_template, request
import os
import json

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/bot-credentials/set", methods=["POST"])
def bot_credentials_set():
    payload = request.get_json()
    with open("token.txt", "w+") as file:
        file.write(payload["token"])
    return payload["token"]

@app.route("/settings", methods=["GET"])
def bot_credentials_get():
    token = ""
    if os.path.exists("token.txt"):
        with open("token.txt", "r") as file:
            token = file.read()
    data = {
        "token" : token
    }
    data_json = json.dumps(data)

    return data_json


if __name__ == "__main__":
    app.run()