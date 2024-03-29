from flask import Flask, render_template, request
import os
import json
import subprocess
import webbrowser

app = Flask(__name__, template_folder="templates", static_folder="static")

subprocess_instance = None

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/bot-credentials/set", methods=["POST"])
def bot_credentials_set():
    payload = request.get_json()
    with open("token.txt", "w+") as file:
        file.write(payload["token"])
    global subprocess_instance
    if subprocess_instance is not None:
        subprocess_instance.terminate()
        subprocess_instance.wait()
        subprocess_instance = subprocess.Popen(["python3", "bot.py"])
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

@app.route("/servers", methods=["GET"])
def servers():
    servers = None
    with open("bot_storage_cache.json", "r") as file:
        servers = json.loads(file.read())
    
    servers_only = json.dumps(servers["servers"])

    return servers_only

@app.route("/register-slash-commands", methods=["GET"])
def register_slash_commands():
    with open("dashboard_req_to_bot", "a") as file:
        file.write("regcmd\n")

    return "Success"

subprocess_instance = subprocess.Popen(["python3", "bot.py"])

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run()