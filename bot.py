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

bot.register_message_handler(callback=main_bot.start, commands=['start'], pass_bot=True)

bot.register_message_handler(callback=main_bot.info, commands=['Info'], pass_bot=True)

bot.register_message_handler(callback=register_bot.chose_language, func=message_filter.chose_language, pass_bot=True)

bot.register_message_handler(callback=register_bot.reg_start, commands=['Register'], pass_bot=True)

bot.register_message_handler(callback=log_bot.log_start, commands=['Login'], pass_bot=True)

bot.register_message_handler(callback=register_bot.enter_username, func=message_filter.enter_username, pass_bot=True)

bot.register_message_handler(callback=register_bot.enter_password, func=message_filter.enter_password, pass_bot=True)


@bot.message_handler(func=message_filter.repeat_password)
def repeat_password(message):
    if register_bot.repeat_password(message, bot):
        main_bot.get_main_menu(message, bot)


bot.register_message_handler(callback=log_bot.enter_username, func=message_filter.log_username, pass_bot=True)


@bot.message_handler(func=message_filter.log_password)
def log_password(message):
    log_bot.get_password(message, bot)
    main_bot.start(message, bot)


bot.register_message_handler(callback=main_bot.filter_anonim, func=message_filter.filter_anonim, pass_bot=True)

bot.register_message_handler(callback=account_bot.user_quit, commands=['Quit'], pass_bot=True)

bot.register_message_handler(callback=main_bot.start, commands=['Main'], pass_bot=True)

bot.register_message_handler(callback=account_bot.main_account, commands=['Account'], pass_bot=True)

bot.register_message_handler(callback=account_bot.change_username_start, func=message_filter.change_username_start,
                             pass_bot=True)

bot.register_message_handler(callback=account_bot.change_username_result, func=message_filter.change_username_result,
                             pass_bot=True)

bot.register_message_handler(callback=account_bot.change_password_start, func=message_filter.change_password_start,
                             pass_bot=True)

bot.register_message_handler(callback=account_bot.change_password_first, func=message_filter.change_password_first,
                             pass_bot=True)

bot.register_message_handler(callback=account_bot.change_password_result, func=message_filter.change_password_result,
                             pass_bot=True)

bot.register_message_handler(callback=account_bot.delete_account_start, func=message_filter.delete_password_start,
                             pass_bot=True)

bot.register_message_handler(callback=account_bot.delete_account_result, func=message_filter.delete_password_result,
                             pass_bot=True)

bot.register_message_handler(callback=account_bot.change_lang_start, func=message_filter.change_lang_start,
                             pass_bot=True)

bot.register_message_handler(callback=account_bot.change_lang_result, func=message_filter.change_lang_result,
                             pass_bot=True)

bot.register_message_handler(callback=main_bot.unknown_message, func=message_filter.handle_everything,
                             pass_bot=True)


bot.infinity_polling()
