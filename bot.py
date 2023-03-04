import sqlalchemy
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import Table
import telebot
from handlers.main import Main
from handlers.registration import Registration
import os

BOT_TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(BOT_TOKEN)

engine = sqlalchemy.create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
Base = declarative_base()
session = Session(engine)


register_bot = Registration()
main_bot = Main()


class Users(Base):
    __table__ = Table('Users', Base.metadata, autoload_with=engine)


@bot.message_handler(commands=['start'])
def start(message):
    main_bot.start(message, bot)


@bot.message_handler(
    func=lambda message: redis_connector.get(f'user_language_{message.from_user.id}') == b'choosing')
def chose_language(message):
    register_bot.chose_language(message, bot)


@bot.message_handler(func=lambda message: message.text == 'Register')
def reg_start(message):
    register_bot.reg_start(message, bot)


@bot.message_handler(
    func=lambda message: redis_connector.get(f'user_status_{message.from_user.id}') == b'wait_for_username')
def enter_username(message):
    register_bot.enter_username(message, bot)


@bot.message_handler(
    func=lambda message: redis_connector.get(f'user_status_{message.from_user.id}') == b'wait_for_password')
def enter_password(message):
    register_bot.enter_password(message, bot)


@bot.message_handler(
    func=lambda message: redis_connector.get(f'user_status_{message.from_user.id}') == b'repeat_password')
def repeat_password(message):
    register_bot.repeat_password(message, bot)





bot.infinity_polling()
