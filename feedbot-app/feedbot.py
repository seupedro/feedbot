import logging
import os
from asyncio import Queue

from telegram import Bot
from telegram.ext import CommandHandler, RegexHandler, Dispatcher
from telegram.ext import messagequeue as mq

from commands import start, callback_404
from database import redis_db

TOKEN = os.getenv('FEEDBOT_TELEGRAM_TOKEN')


class MQBot(Bot):
    '''A subclass of Bot which delegates send method handling to MQ'''
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
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_message(*args, **kwargs)


def init():

    # Start DB and Bot
    redis_db()
    feedbot = Bot(TOKEN)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    update_queue = Queue()
    dispatcher = Dispatcher(feedbot, None, 0)

    # Handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(RegexHandler(pattern=r'\w+', callback=callback_404))  # Must be last callback

    # Start the thread
    # thread = Thread(target=dispatcher.start, name='dispatcher')
    # thread.start()

    return dispatcher


if __name__ == '__main__':
    init()
