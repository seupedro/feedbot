import os

import redis
from redis import Redis

USER_SET = 'user_id'
FEED_LAST_MODIFIED = 'feed_last_modified'
FEED_ID_LIST = 'feed_id'
FEED = 'feed'
SILENCE = 'silence'

FROM_ZERO = 0
DATE_MAX_VALUE = 2147483647
ID_PRESERVE_VALUE = 50

SILENCE_OFF = '0'
SILENCE_ON = '1'
db: Redis


def redis_db():
    global db
    db = redis.StrictRedis(host=os.getenv('FEEDBOT_DATABASE_URL'),
                           port=os.getenv('FEEDBOT_DATABASE_PORT'),
                           password=os.getenv('FEEDBOT_DATABASE_PASSWORD'),
                           charset='utf-8',
                           decode_responses=True)
    # TODO: Use a single connection pool, and limit dbs creations
    # TODO: Set authentication


def save_user_id(user_id):
    db.sadd(USER_SET, user_id)


def get_last_modified():
    return db.hget(FEED, FEED_LAST_MODIFIED)


def set_last_modified(last_modified):
    db.hset(FEED, FEED_LAST_MODIFIED, last_modified)


def set_feed_id(entry_id, date_score):
    return db.zadd(FEED_ID_LIST, dict({entry_id: date_score}), nx=True)


def limit_feed_id_size():
    id_count = db.zcount(FEED_ID_LIST, FROM_ZERO, DATE_MAX_VALUE)
    if id_count > ID_PRESERVE_VALUE:
        db.zremrangebyrank(FEED_ID_LIST, FROM_ZERO, (id_count - ID_PRESERVE_VALUE))


def get_usr_list():
    return db.smembers(USER_SET)


def set_silence(user_id, boolean):
    if boolean:
        db.hset(SILENCE, user_id, SILENCE_ON)
    else:
        db.hset(SILENCE, user_id, SILENCE_OFF)


def get_silence(user_id):
    value = db.hget(SILENCE, user_id)
    if value == SILENCE_ON:
        return True
    elif value == SILENCE_OFF:
        return False
    else:
        return False
