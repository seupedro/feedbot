import os

import httpx as httpx
import telegram
from flask import Flask, request
from httpx import Response

from feedbot import init
from updates_handler import process_updates

app = Flask(__name__)
dispatcher = init()
TOKEN = os.getenv('FEEDBOT_TELEGRAM_TOKEN')
FEEDBOT_SERVICE_URL = os.getenv('FEEDBOT_SERVICE_URL')


@app.route("/ping")
def ping():
    return "pong"


@app.route("/set_webhook")
def set_webhook():
    response: Response = httpx.get(url=f'https://api.telegram.org/bot{TOKEN}/setWebhook?url={FEEDBOT_SERVICE_URL}/{TOKEN}/webhook')
    return response.json()


@app.route(f'/{TOKEN}/webhook', methods=['POST'])
def webhook_handler():
    bot = telegram.Bot(TOKEN)

    if request.method == "POST":

        update = telegram.Update.de_json(request.get_json(force=True), bot)
        # update_queue.put(update)
        dispatcher.process_update(update)

    return 'ok'


@app.route(f'/{TOKEN}/updates', methods=['POST'])
def updates():

    if request.method == "POST":
        json: dict = request.get_json(force=True)
        process_updates(
            title=json.get('title'),
            link=json.get('link'),
            photo_html=json.get('photo_html')
        )

    return 'ok'

