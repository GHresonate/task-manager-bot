import telebot
from handlers.main import Main
from handlers.registration import Registration
from handlers.login import Login
from handlers.account import Account
from utilits.filters import Filter
import os


BOT_TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(BOT_TOKEN)

register_bot = Registration()
main_bot = Main()
message_filter = Filter()
log_bot = Login()
account_bot = Account()


@bot.message_handler(commands=['start'])
def start(message):
    main_bot.start(message, bot)


@bot.message_handler(func=message_filter.chose_language)
def chose_language(message):
    register_bot.chose_language(message, bot)


@bot.message_handler(commands=['Register'])
def reg_start(message):
    register_bot.reg_start(message, bot)


@bot.message_handler(commands=['Info'])
def info(message):
    main_bot.info(message, bot)


@bot.message_handler(commands=['Login'])
def log_start(message):
    log_bot.log_start(message, bot)


@bot.message_handler(func=message_filter.enter_username)
def enter_username(message):
    register_bot.enter_username(message, bot)


@bot.message_handler(func=message_filter.enter_password)
def enter_password(message):
    register_bot.enter_password(message, bot)


@bot.message_handler(func=message_filter.repeat_password)
def repeat_password(message):
    if register_bot.repeat_password(message, bot):
        main_bot.get_main_menu(message, bot)


@bot.message_handler(func=message_filter.log_username)
def log_username(message):
    log_bot.enter_username(message, bot)


@bot.message_handler(func=message_filter.log_password)
def log_password(message):
    log_bot.get_password(message, bot)
    main_bot.start(message, bot)


@bot.message_handler(commands=['Account'])
def account(message):
    account_bot.main_account(message, bot)


@bot.message_handler(func=message_filter.change_username_start)
def change_username_start(message):
    account_bot.change_username_start(message, bot)


@bot.message_handler(func=message_filter.change_username_result)
def change_username_result(message):
    account_bot.change_username_result(message, bot)


@bot.message_handler(func=message_filter.change_password_start)
def change_password_start(message):
    account_bot.change_password_start(message, bot)


@bot.message_handler(func=message_filter.change_password_first)
def change_password_first(message):
    account_bot.change_password_first(message, bot)


@bot.message_handler(func=message_filter.change_password_result)
def change_password_result(message):
    account_bot.change_password_result(message, bot)


@bot.message_handler(func=message_filter.delete_password_start)
def delete_account_start(message):
    account_bot.delete_account_start(message, bot)


@bot.message_handler(func=message_filter.delete_password_result)
def delete_account_result(message):
    account_bot.delete_account_result(message, bot)


bot.infinity_polling()
