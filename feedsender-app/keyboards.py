from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def getKeyboard(keyboard: str = None, link: str = None):

    if keyboard is None:
        return None

    if link is None:
        print(' -- WARNING -- Link is None: It can cause the message fail silent')

    keyboards = {
        'contact': InlineKeyboardMarkup([[InlineKeyboardButton("📣 Contato", url='t.me/pedrohartmann')]]),
        'read_on_jw': InlineKeyboardMarkup([[InlineKeyboardButton("📰  Ler notícia no JW.org", url=link)]])
    }

    return keyboards.get(keyboard)
