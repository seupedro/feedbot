from telegram import User, Chat, Message, Bot, Update

from database import save_user_id
from updates_dispatcher import dispatch_message

INTRO_TEXT = 'Olá {}, como vai? 😁 \n' \
             'Pronto para receber novas notícias do *JW.org*? \n\n' \
             'Todo dia eu vou buscar automaticamente por novas ' \
             'noticias no site JW. Assim que tiver uma nova notícia ' \
             'eu mando na hora pra você. 📨 \n\n'

HELP_TEXT = '😥 Desculpe {} \n' \
            'Não consegui te entender. \n\n' \
            'Todo dia eu procuro por novas notícias no site JW.org. Assim ' \
            'que sai uma nova, eu imediatamente mando pra você. \n\n' \
            'Se você tem alguma dúvida, crítica ou sugestão, fique a vontade ' \
            'para entrar em contato usando o botão abaixo. \n\n' \
            'Credits: Icons made by Roundicons from www.flaticon.com is licensed by CC 3.0'


def start(bot, update):
    usr: User = update.effective_user
    chat: Chat = update.effective_chat
    msg: Message = update.effective_message

    save_user_id(usr.id)

    data = {
        'text': INTRO_TEXT.format(usr.first_name),
        'chat_id': chat.id,
        'parse_mode': 'Markdown'
    }

    dispatch_message(data)


def callback_404(bot: Bot, update: Update):
    usr: User = update.effective_user
    chat: Chat = update.effective_chat
    msg: Message = update.effective_message

    data = {
        'text': HELP_TEXT.format(usr.first_name),
        'chat_id': chat.id,
        'parse_mode': 'Markdown',
        'reply_markup': 'contact'
    }

    dispatch_message(data)
