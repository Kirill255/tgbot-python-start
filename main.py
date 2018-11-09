import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import SQLite, DBRequest

TOKEN = os.environ.get("TOKEN")  # Telegram токен
PATH_DB = 'db.sqlite'  # Путь к базе данных

bot = telebot.TeleBot(TOKEN)
db = DBRequest(SQLite(PATH_DB))


def post_markup(like_yes='', like_not=''):
    markup = InlineKeyboardMarkup()
    item1 = InlineKeyboardButton('👍 {0}'.format(like_yes), callback_data=f'yes')
    item2 = InlineKeyboardButton('👎 {0}'.format(like_not), callback_data=f'not')
    markup.add(item1, item2)

    return markup


@bot.channel_post_handler()
def channel_post(message):
    db.new_post([None, message.chat.id, message.message_id, 0, 0])
    bot.edit_message_reply_markup(message.chat.id, message.message_id, reply_markup=post_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = db.select_post([call.message.chat.id, call.message.message_id])

    if call.data == 'yes':
        num = data[0][3] + 1
        db.new_like_yes([num, call.message.chat.id, call.message.message_id])
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                      reply_markup=post_markup(num, data[0][4]))
        bot.answer_callback_query(call.id, 'Нравится')
    elif call.data == 'not':
        num = data[0][4] + 1
        db.new_like_not([num, call.message.chat.id, call.message.message_id])
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                      reply_markup=post_markup(data[0][3], num))
        bot.answer_callback_query(call.id, 'Не нравится')


if __name__ == '__main__':
    db.create()
    bot.polling()
