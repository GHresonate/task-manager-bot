from utilits.keyboard_manager import KeyboardManager
from connectors.redis_connector import RedisConnector
from connectors.postgres_connector import PostgresConnector
from utilits.message_text import translator
from sqlalchemy.exc import IntegrityError
from hashlib import sha256


class Account:
    def __init__(self):
        self._kb = KeyboardManager()
        self._redis = RedisConnector()
        self._postgres = PostgresConnector()

    def main_account(self, message, bot):
        bot.send_message(message.chat.id, translator["account_message"][self._redis.get_lang(message)],
                         reply_markup=self._kb.get_account_kb())

    def change_username_start(self, message, bot):
        self._redis.set_acc_actions(message, "chose_name")
        old_username = self._redis.get_username(message)
        bot.send_message(message.chat.id, translator["change_name"][self._redis.get_lang(message)].format(old_username),
                         reply_markup=self._kb.get_account_kb())

    def change_username_result(self, message, bot):
        print(1)
        self._redis.del_acc_actions(message)
        new_username = message.text
        if len(new_username) > 16 or new_username.isspace():
            bot.reply_to(message, translator['username_error'][self._redis.get_lang(message)])
            return
        if self._postgres.check_user_exist(new_username):
            bot.reply_to(message, translator['username_already_used'][self._redis.get_lang(message)])
            return
        old_username = self._redis.get_username(message)
        try:
            self._postgres.change_username(old_username, new_username)
            self._redis.del_acc_actions(message)
            self._redis.change_username(message, new_username)
            bot.send_message(message.chat.id, translator['success_username_change'][self._redis.get_lang(message)],
                             reply_markup=self._kb.get_account_kb())
        except IntegrityError:
            self._redis.del_acc_actions(message)
            bot.send_message(message.chat.id, translator['username_error'][self._redis.get_lang(message)],
                             reply_markup=self._kb.get_account_kb())

    def change_password_start(self, message, bot):
        self._redis.set_acc_actions(message, "chose_password")
        bot.send_message(message.chat.id, translator["change_password"][self._redis.get_lang(message)],
                         reply_markup=self._kb.get_account_kb())

    def change_password_first(self, message, bot):
        password = message.text
        bot.delete_message(message.chat.id, message.message_id)
        if len(password) < 5 or password.isspace() or len(password) > 20:
            bot.reply_to(message, translator['password_error'][self._redis.get_lang(message)])
            return
        self._redis.set_change_pass(message, sha256(password.encode()).hexdigest())
        self._redis.set_acc_actions(message, "repeat_password")
        bot.send_message(message.chat.id, translator["repeat_password"][self._redis.get_lang(message)],
                         reply_markup=self._kb.get_account_kb())

    def change_password_result(self, message, bot):
        password = message.text
        bot.delete_message(message.chat.id, message.message_id)
        p_hash = self._redis.get_change_pass(message)
        self._redis.del_change_pass(message)
        self._redis.del_acc_actions(message)
        if p_hash == sha256(password.encode()).hexdigest():
            username = self._redis.get_username(message)
            try:
                self._postgres.change_password(username, p_hash)
            except IntegrityError:
                bot.send_message(message.chat.id, translator['change_error'][self._redis.get_lang(message)],
                                 reply_markup=self._kb.get_account_kb())
            self._redis.change_username(message, username)
            bot.send_message(message.chat.id, translator['success_password_change'][self._redis.get_lang(message)],
                             reply_markup=self._kb.get_account_kb())
        else:
            bot.reply_to(message, translator['repeat_password_error'][self._redis.get_lang(message)],
                         reply_markup=self._kb.get_account_kb())

    def delete_account_start(self, message, bot):
        self._redis.set_acc_actions(message, "del_account")
        bot.send_message(message.chat.id, translator["del_account"][self._redis.get_lang(message)],
                         reply_markup=self._kb.get_account_kb())

    def delete_account_result(self, message, bot):
        username = self._redis.get_username(message)
        self._postgres.delete_user(username)
        self._redis.del_acc_actions(message)
        self._redis.del_log(message)
        self._redis.del_username(message)
        bot.send_message(message.chat.id, translator["account_deleted"][self._redis.get_lang(message)],
                         reply_markup=self._kb.get_start_kb())

    def user_quit(self, message, bot):
        self._redis.del_acc_actions(message)
        self._redis.del_log(message)
        self._redis.del_username(message)
        bot.send_message(message.chat.id, translator["quit_done"][self._redis.get_lang(message)],
                         reply_markup=self._kb.get_start_kb())

    def change_lang_start(self, message, bot):
        self._redis.set_acc_actions(message, "change_lang")
        bot.send_message(message.chat.id, translator['chose_language']['en'],
                         reply_markup=self._kb.get_lang_kb_for_change())

    def change_lang_result(self, message, bot):
        if message.text == 'Українська':
            self._redis.set_lang(message, 'uk')
        elif message.text == 'English':
            self._redis.set_lang(message, 'en')
        else:
            bot.send_message(message.chat.id, translator['language_error']['en'],
                             reply_markup=self._kb.get_lang_kb_for_change())
            return
        self._redis.del_acc_actions(message)
        bot.send_message(message.chat.id, translator['username_changed'][
            self._redis.get_lang(message)], reply_markup=self._kb.get_account_kb())
