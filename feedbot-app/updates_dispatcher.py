import os
import httpx

TOKEN = os.getenv('FEEDBOT_TELEGRAM_TOKEN')
FEEDSENDER_SERVICE_URL = os.getenv('FEEDSENDER_SERVICE_URL')


def dispatch_message(data):
    with httpx.Client() as client:
        client.post(f'{FEEDSENDER_SERVICE_URL}/{TOKEN}/send_message', json=data)


def dispatch_bulk_message(data):
    with httpx.Client() as client:
        print('')
        print(data)
        print('')
        client.post(f'{FEEDSENDER_SERVICE_URL}/{TOKEN}/bulk_message', json=data)


def dispatch_bulk_photo_message(data):
    with httpx.Client() as client:
        client.post(f'{FEEDSENDER_SERVICE_URL}/{TOKEN}/bulk_photo_message', json=data)
