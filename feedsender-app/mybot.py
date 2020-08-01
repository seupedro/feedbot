import logging
import os

from telegram import Bot
from telegram.ext import messagequeue as mq
from telegram.utils.request import Request

from keyboards import getKeyboard
from models import Message, BulkMessage, BulkPhotoMessage

TOKEN = os.getenv('FEEDBOT_TELEGRAM_TOKEN')


class MQBot(Bot):
    """A subclass of Bot which delegates send method handling to MQ"""

    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass
        super(MQBot, self).__del__()

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        """Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments"""
        return super(MQBot, self).send_message(*args, **kwargs)


def mybot():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    msg_queue = mq.MessageQueue(all_burst_limit=25, all_time_limit_ms=1050)
    request = Request(con_pool_size=8)
    bot = MQBot(TOKEN, request=request, mqueue=msg_queue)
    return bot


def send_message(bot: Bot, msg: Message):
    msg.reply_markup = getKeyboard(msg.reply_markup)

    bot.send_message(
        chat_id=msg.chat_id,
        text=msg.text,
        parse_mode=msg.parse_mode,
        disable_web_page_preview=msg.disable_web_page_preview,
        disable_notification=msg.disable_notification,
        reply_to_message_id=msg.reply_to_message_id,
        reply_markup=msg.reply_markup,
        timeout=msg.timeout
    )


def send_bulk_message(bot: Bot, msg: BulkMessage):
    msg.reply_markup = getKeyboard(msg.reply_markup, msg.link)

    for user in msg.users:
        bot.send_message(
            chat_id=user,
            text=msg.text,
            disable_notification=msg.disable_notification,
            reply_markup=msg.reply_markup
        )


def send_bulk_photo_message(bot: Bot, msg: BulkPhotoMessage):
    msg.reply_markup = getKeyboard(msg.reply_markup, msg.link)

    for user in msg.users:
        bot.send_photo(
            chat_id=user,
            photo=msg.photo,
            caption=msg.caption,
            disable_notification=msg.disable_notification,
            reply_markup=msg.reply_markup
        )
