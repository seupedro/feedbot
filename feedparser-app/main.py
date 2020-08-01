from flask import Flask

from feed import fetch_updates

app = Flask(__name__)


@app.route("/ping")
def ping():
    return "pong"


@app.route("/fetch")
def fetch():
    fetch_updates()
    return "fetch"


