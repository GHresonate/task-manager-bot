from utilits.message_text import translator
from utilits.keyboard_manager import KeyboardManager
from utilits.redis_connector import RedisConnector
from utilits.postgres_connector import PostgresConnector
from sqlalchemy.exc import IntegrityError
from hashlib import sha256


class Login:
    def __init__(self):
        self.kb = KeyboardManager()
        self.redis = RedisConnector()
        self.postgres = PostgresConnector()

    def log_start(self, message, bot):
        if self.redis.get_status(message) == 'logged':
            bot.reply_to(message, translator['already_logged_error'][
                self.redis.get_lang(message)])
            return
        self.redis.set_log(message, 'wait_for_username')
        bot.reply_to(message, translator['enter_username'][self.redis.get_lang(message)])

    def enter_username(self, message, bot):
        username = message.text
        if len(username) > 16 or username.isspace():
            bot.reply_to(message, translator['username_error'][self.redis.get_lang(message)])
            return
        self.redis.set_log(message, 'wait_for_password')
        self.redis.set_log_data(message, username)
        bot.send_message(message.chat.id, translator['enter_password_log'][self.redis.get_lang(message)])

    def get_password(self, message, bot):
        password = message.text
        bot.delete_message(message.chat.id, message.message_id)
        p_hash = sha256(password.encode()).hexdigest()
        username = self.redis.get_log_data(message)
        self.redis.del_log_data(message)
        if self.postgres.check_user_password(username, p_hash):
            self.redis.del_log_data(message)
            self.redis.set_user_status(message, 'logged', username)
            return 1
        else:
            self.redis.del_log_data(message)
            return 0
