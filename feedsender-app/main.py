import telegram
from fastapi import FastAPI

from models import Message, BulkPhotoMessage, BulkMessage
from mybot import TOKEN, send_message, mybot, send_bulk_photo_message, send_bulk_message

app = FastAPI()
bot: telegram.Bot = mybot()


@app.get("/ping")
async def read_root():
    return {"Async": "World"}


@app.post(f'/{TOKEN}/send_message')
async def send(message: Message):
    send_message(bot, message)
    return {"message": "send", "status": 200}


@app.post(f'/{TOKEN}/bulk_message')
async def send(message: BulkMessage):
    send_bulk_message(bot, message)
    return {"message": "send", "status": 200}


@app.post(f'/{TOKEN}/bulk_photo_message')
async def send(message: BulkPhotoMessage):
    send_bulk_photo_message(bot, message)
    return {"message": "send", "status": 200}
