from utilits.message_text import translator
from utilits.keyboard_manager import KeyboardManager
from utilits.redis_connector import RedisConnector
from utilits.postgres_connector import PostgresConnector
from utilits.message_text import translator
from sqlalchemy.exc import IntegrityError

class Account:
    def __init__(self):
        self.kb = KeyboardManager()
        self.redis = RedisConnector()
        self.postgres = PostgresConnector()

    def main_account(self, message, bot):
        bot.send_message(message.chat.id, translator["account_message"][self.redis.get_lang(message)],
                         reply_markup=self.kb.get_account_kb())

    def change_name_start(self, message, bot):
        self.redis.set_acc_actions(message, "chose_name")
        bot.send_message(message.chat.id, translator["change_name"][self.redis.get_lang(message)].format(),
                         reply_markup=self.kb.get_account_kb())

    def change_name_result(self, message, bot):
        self.redis.del_acc_actions(message)
        old_username = self.redis.get_username(message)
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
        except IntegrityError:
            bot.send_message(message.chat.id, translator['registration_error'][self.redis.get_lang(message)],
                             reply_markup=self.kb.get_start_kb())
    def change_password_start(self, message, bot):
        pass

    def change_password_result(self, message, bot):
        pass

    def delete_account_start(self, message, bot):
        pass

    def delete_account_result(self, message, bot):
        pass
