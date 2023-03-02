import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import Table
from telebot.util import quick_markup
import telebot
import redis
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from message_text import translator
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]

bot = telebot.TeleBot(BOT_TOKEN)
redis_connector = redis.Redis()


def get_start_keyboard():
    info_button = KeyboardButton('Info')
    login_button = KeyboardButton('Login')
    register_button = KeyboardButton('Register')
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.add(login_button)
    keyboard.add(register_button)
    keyboard.add(info_button)
    return keyboard


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, translator['welcome_message']['en'], reply_markup=get_start_keyboard())


@bot.message_handler(func=lambda message: message.text == 'Login')
def reg_start(message):
    redis_connector.set({f'user_status_{message.from_user.id}': 'name_wait'})
    bot.reply_to(message, translator['enter_name']['en'], reply_markup=None)


bot.infinity_polling()
