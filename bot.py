import sqlalchemy
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import Table, insert, values
from telebot.util import quick_markup
import telebot
import redis
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from message_text import translator
import os
import hashlib

BOT_TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(BOT_TOKEN)
redis_connector = redis.Redis()

engine = sqlalchemy.create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
Base = declarative_base()
session = Session(engine)


class Users(Base):
    __table__ = Table('Users', Base.metadata, autoload_with=engine)


def get_start_keyboard():
    info_button = KeyboardButton('Info')
    login_button = KeyboardButton('Login')
    register_button = KeyboardButton('Register')
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.add(login_button)
    keyboard.add(register_button)
    keyboard.add(info_button)
    return keyboard


def get_chose_language_keyboard():
    eng_button = KeyboardButton('English')
    ukr_button = KeyboardButton('Українська')
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.add(eng_button)
    keyboard.add(ukr_button)
    return keyboard


def get_main_keyboard():
    quit_button = KeyboardButton('Quit')
    account_button = KeyboardButton('Account')
    tasks_button = KeyboardButton('Tasks')
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.add(tasks_button)
    keyboard.add(account_button)
    keyboard.add(quit_button)
    return keyboard


@bot.message_handler(commands=['start'])
def start(message):
    if not redis_connector.get(f'user_language_{message.from_user.id}') or redis_connector.get(
            f'user_language_{message.from_user.id}').decode() == 'choosing':
        redis_connector.set(f'user_language_{message.from_user.id}', 'choosing')
        bot.reply_to(message, translator['chose_language']['en'], reply_markup=get_chose_language_keyboard())
    elif redis_connector.get(f'user_status_{message.from_user.id}') != 'logged':
        get_main_menu(message)
    else:
        redis_connector.delete(f'user_status_{message.from_user.id}')
        bot.reply_to(message, translator['welcome_message'][
            redis_connector.get(f'user_language_{message.from_user.id}').decode()], reply_markup=get_start_keyboard())


@bot.message_handler(
    func=lambda message: redis_connector.get(f'user_language_{message.from_user.id}') == b'choosing')
def chose_language(message):
    if message.text == 'Українська':
        redis_connector.set(f'user_language_{message.from_user.id}', 'uk')
    elif message.text == 'English':
        redis_connector.set(f'user_language_{message.from_user.id}', 'en')
    else:
        bot.send_message(message.chat.id, translator['language_error']['en'],
                         reply_markup=get_chose_language_keyboard())
        return
    bot.send_message(message.chat.id, translator['welcome_message'][
        redis_connector.get(f'user_language_{message.from_user.id}').decode()], reply_markup=get_start_keyboard())


@bot.message_handler(func=lambda message: message.text == 'Register')
def reg_start(message):
    redis_connector.set(f'user_status_{message.from_user.id}', 'wait_for_username')
    bot.reply_to(message,
                 translator['enter_username'][redis_connector.get(f'user_language_{message.from_user.id}').decode()])


@bot.message_handler(
    func=lambda message: redis_connector.get(f'user_status_{message.from_user.id}') == b'wait_for_username')
def enter_username(message):
    username = message.text
    if len(username) > 16 or username.isspace():
        bot.reply_to(message, translator['username_error'][
            redis_connector.get(f'user_language_{message.from_user.id}').decode()])
        return
    redis_connector.set(f'user_status_{message.from_user.id}', 'wait_for_password')
    redis_connector.hset(f'registration_{message.from_user.id}', 'username', username)
    bot.reply_to(message, translator['reaction_for_username'][
        redis_connector.get(f'user_language_{message.from_user.id}').decode()].format(username))
    bot.send_message(message.chat.id, translator['enter_password'][
        redis_connector.get(f'user_language_{message.from_user.id}').decode()])


@bot.message_handler(
    func=lambda message: redis_connector.get(f'user_status_{message.from_user.id}') == b'wait_for_password')
def enter_password(message):
    password = message.text
    if len(password) < 5 or password.isspace() or len(password) > 20:
        bot.reply_to(message, translator['password_error'][
            redis_connector.get(f'user_language_{message.from_user.id}').decode()])
        return
    redis_connector.set(f'user_status_{message.from_user.id}', 'repeat_password')
    redis_connector.hset(f'registration_{message.from_user.id}', 'password_hash',
                         hashlib.sha256(password.encode()).hexdigest())
    bot.send_message(message.chat.id, translator['repeat_password'][
        redis_connector.get(f'user_language_{message.from_user.id}').decode()])


@bot.message_handler(
    func=lambda message: redis_connector.get(f'user_status_{message.from_user.id}') == b'repeat_password')
def repeat_password(message):
    password = message.text
    p_hash = redis_connector.hget(f'registration_{message.from_user.id}', 'password_hash')
    if p_hash == hashlib.sha256(password.encode()).hexdigest().encode():
        ins = insert(Users).values(username=redis_connector.hget(f'registration_{message.from_user.id}',
                                                                 'username').decode(),
                                   password_hash=redis_connector.hget(f'registration_{message.from_user.id}',
                                                                      'password_hash').decode())
        session.execute(ins)
        redis_connector.delete(f'registration_{message.from_user.id}')
        session.commit()
        redis_connector.set(f'user_status_{message.from_user.id}', 'logged')
        return get_main_menu(message)
    else:
        redis_connector.set(f'user_status_{message.from_user.id}', 'wait_for_password')
        bot.reply_to(message, translator['repeat_password_error'][
            redis_connector.get(f'user_language_{message.from_user.id}').decode()])
        bot.send_message(message.chat.id, translator['enter_password'][
            redis_connector.get(f'user_language_{message.from_user.id}').decode()])


def get_main_menu(message):
    keyboard = get_main_keyboard()
    bot.send_message(message.chat.id, translator['welcome_for_register'][
        redis_connector.get(f'user_language_{message.from_user.id}').decode()],
                     reply_markup=keyboard)


bot.infinity_polling()
