from utilits.keyboard_manager import KeyboardManager
from utilits.redis_connector import RedisConnector
from utilits.postgres_connector import PostgresConnector
from utilits.message_text import translator
from sqlalchemy.exc import IntegrityError
from hashlib import sha256


class Account:
    def __init__(self):
        self.kb = KeyboardManager()
        self.redis = RedisConnector()
        self.postgres = PostgresConnector()

    def main_account(self, message, bot):
        bot.send_message(message.chat.id, translator["account_message"][self.redis.get_lang(message)],
                         reply_markup=self.kb.get_account_kb())

    def change_username_start(self, message, bot):
        self.redis.set_acc_actions(message, "chose_name")
        old_username = self.redis.get_username(message)
        bot.send_message(message.chat.id, translator["change_name"][self.redis.get_lang(message)].format(old_username),
                         reply_markup=self.kb.get_account_kb())

    def change_username_result(self, message, bot):
        print(1)
        self.redis.del_acc_actions(message)
        new_username = message.text
        if len(new_username) > 16 or new_username.isspace():
            bot.reply_to(message, translator['username_error'][self.redis.get_lang(message)])
            return
        if self.postgres.check_user_exist(new_username):
            bot.reply_to(message, translator['username_already_used'][self.redis.get_lang(message)])
            return
        old_username = self.redis.get_username(message)
        try:
            self.postgres.change_username(old_username, new_username)
            self.redis.del_acc_actions(message)
            self.redis.change_username(message, new_username)
            bot.send_message(message.chat.id, translator['success_username_change'][self.redis.get_lang(message)],
                             reply_markup=self.kb.get_account_kb())
        except IntegrityError:
            bot.send_message(message.chat.id, translator['username_error'][self.redis.get_lang(message)],
                             reply_markup=self.kb.get_account_kb())

    def change_password_start(self, message, bot):
        self.redis.set_acc_actions(message, "chose_password")
        bot.send_message(message.chat.id, translator["change_password"][self.redis.get_lang(message)],
                         reply_markup=self.kb.get_account_kb())

    def change_password_first(self, message, bot):
        password = message.text
        bot.delete_message(message.chat.id, message.message_id)
        if len(password) < 5 or password.isspace() or len(password) > 20:
            bot.reply_to(message, translator['password_error'][self.redis.get_lang(message)])
            return
        self.redis.set_change_pass(message, sha256(password.encode()).hexdigest())
        self.redis.set_acc_actions(message, "repeat_password")
        bot.send_message(message.chat.id, translator["repeat_password"][self.redis.get_lang(message)],
                         reply_markup=self.kb.get_account_kb())

    def change_password_result(self, message, bot):
        password = message.text
        bot.delete_message(message.chat.id, message.message_id)
        p_hash = self.redis.get_change_pass(message)
        self.redis.del_change_pass(message)
        self.redis.del_acc_actions(message)
        if p_hash == sha256(password.encode()).hexdigest():
            username = self.redis.get_username(message)
            try:
                self.postgres.change_password(username, p_hash)
            except IntegrityError:
                bot.send_message(message.chat.id, translator['change_error'][self.redis.get_lang(message)],
                                 reply_markup=self.kb.get_account_kb())
            self.redis.change_username(message, username)
            bot.send_message(message.chat.id, translator['success_password_change'][self.redis.get_lang(message)],
                             reply_markup=self.kb.get_account_kb())
        else:
            bot.reply_to(message, translator['repeat_password_error'][self.redis.get_lang(message)],
                         reply_markup=self.kb.get_account_kb())

    def delete_account_start(self, message, bot):
        pass

    def delete_account_result(self, message, bot):
        pass
