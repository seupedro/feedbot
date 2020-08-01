from bs4 import BeautifulSoup

from database import get_usr_list
from updates_dispatcher import dispatch_bulk_photo_message, dispatch_bulk_message


def process_updates(title, link, photo_html):

    users: list = get_usr_list()
    photo = get_article_photo(photo_html)

    if users is not None:
        if photo is not None:

            data = {
                'users': users,
                'caption': title[10:],
                'photo': photo,
                'link': link,
                'disable_notification': True,
                'reply_markup': 'read_on_jw'
            }

            dispatch_bulk_photo_message(data)

        else:

            data = {
                'users': users,
                'text': title,
                'link': link,
                'parse_mode': 'Markdown',
                'disable_notification': True,
                'reply_markup': 'read_on_jw'
            }

            dispatch_bulk_message(data)


def get_article_photo(photo_html):

    if photo_html is not None:
        # Get image from html
        # Edit filename to get large photo format
        photo = BeautifulSoup(photo_html, 'html.parser') \
            .contents[0].attrs['src'].replace('_univ_sqs_sm.jpg', '_univ_lsr_lg.jpg')
        print('photo', photo)

    return photo_html
