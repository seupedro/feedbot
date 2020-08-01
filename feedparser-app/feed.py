import time

import feedparser
import httpx
from feedparser import FeedParserDict

from database import *

DB_ONE_ITEM_ADDED = 1
FEED_URL = 'https://www.jw.org/pt/noticias/jw-noticias/rss/NewsSubsectionRSSFeed/feed.xml'
TOKEN = os.getenv('FEEDBOT_TELEGRAM_TOKEN')
FEEDBOT_SERVICE_URL = os.getenv('FEEDBOT_SERVICE_URL')


def fetch_updates():
    if True:
        httpx.post(url='https://bedf8726b2caa32f4625cd085c88673a.m.pipedream.net',
                   json={'cron': 'runned','biquini': 'de bolinha amarelinha'})

    redis_db()

    # Work based on last_modified http response
    last_modified = get_last_modified()
    print('fetch started ', last_modified)

    is_first_time_running = last_modified is None
    if is_first_time_running:
        initialize_feed()
        return

    start_new_request(last_modified)


def start_new_request(last_modified):

    print('starting a new request...')

    if feed.status == 200:
        print(feed.status)

        set_last_modified(feed.modified)

        entries_to_send: list = []
        for entry in feed.entries:
            # Score sets based on secs in each entry date.
            date_secs = time.mktime(entry.get('published_parsed'))

            # Prevent duplicated messages be sent.
            is_not_duplicated_item = set_feed_id(entry.id, date_secs) == DB_ONE_ITEM_ADDED
            if is_not_duplicated_item:
                entries_to_send.append({'title': entry.title, 'link': entry.link, 'summary': entry.summary})

        print(len(entries_to_send), 'new entries to send')
        has_news_to_send: bool = len(entries_to_send) > 0
        if has_news_to_send:
            httpx.post(f'{FEEDBOT_SERVICE_URL}/{TOKEN}/updates', json=entries_to_send)

        entries_to_send.clear()

    elif feed.status == 304:
        print(feed.status, 'Not modified')
        limit_feed_id_size()
        pass

    else:
        # TODO: Handle any Response Code here
        print(feed.status, 'unhandled error')
        pass


def initialize_feed():

    # First time running, just get feed's data
    feed: FeedParserDict = feedparser.parse(FEED_URL)
    set_last_modified(feed.modified)

    for entry in feed.entries:

        # Score sets based on secs in each entry date.
        date_secs = time.mktime(entry.get('published_parsed'))
        set_feed_id(entry.id, date_secs)


if __name__ == '__main__':
    fetch_updates()
