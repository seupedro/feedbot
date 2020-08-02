from flask import Flask

from feed import fetch_updates

app = Flask(__name__)


@app.route("/ping")
def ping():
    return "pong"


@app.route("/fetch")
def fetch():
    feed_status: int = fetch_updates()
    return '/fetch', feed_status


