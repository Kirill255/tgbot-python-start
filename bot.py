import os
import random
# import time
# import logging
import telebot
from telebot import types
# from telebot import apihelper

# Logger
# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)

# http -> proxy, что-то в данный момент с простым proxy у этого модуля проблемы
# PROXY = "http://173.192.21.89:8123"
# apihelper.proxy = {"http": PROXY}

# https -> socks proxy, с socks всё работает
# PROXY = "socks5://85.105.213.27:9999"
# PROXY = os.environ.get("PROXY")
# apihelper.proxy = {"https": PROXY}

# TOKEN = "766561573:AAFyg6TptPrXjaDHuBLA-74t9Rc2N6awk7M"
# TOKEN = os.environ["TOKEN"]
TOKEN = os.environ.get("TOKEN")  # using get will return `None` if a key is not present rather than raise a `KeyError`
bot = telebot.TeleBot(TOKEN)


def create_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton("😂")
    btn2 = types.KeyboardButton("😘")
    btn3 = types.KeyboardButton("😍")
    markup.add(btn1, btn2, btn3)
    return markup


smiles = [
    '😂',
    '😘',
    '❤',
    '😍',
    '😊',
    '👍'
]


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Привет, я бот!")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    # bot.reply_to(message, message.text)
    bot.send_message(message.chat.id, random.choice(smiles), reply_markup=create_keyboard())


bot.polling(none_stop=True)
# Polling
# while True:
#     try:
#         bot.polling(none_stop=True)
#     except Exception as e:
#         logger.error(e)
#         time.sleep(15)
