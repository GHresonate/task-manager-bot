from utilits.message_text import translator
from hashlib import sha256
from handlers.base_handler import BaseHandler


class Login(BaseHandler):
    def log_start(self, message, bot):
        if self._redis.get_status(message) == 'logged':
            bot.reply_to(message, translator['already_logged_error'][
                self._redis.get_lang(message)])
            return
        self._redis.set_log(message, 'wait_for_username')
        bot.reply_to(message, translator['enter_username'][self._redis.get_lang(message)])

    def enter_username(self, message, bot):
        username = message.text
        if len(username) > 16 or username.isspace():
            bot.reply_to(message, translator['username_error'][self._redis.get_lang(message)])
            return
        self._redis.set_log(message, 'wait_for_password')
        self._redis.set_log_data(message, username)
        bot.send_message(message.chat.id, translator['enter_password_log'][self._redis.get_lang(message)])

    def get_password(self, message, bot):
        password = message.text
        bot.delete_message(message.chat.id, message.message_id)
        p_hash = sha256(password.encode()).hexdigest()
        username = self._redis.get_log_data(message)
        if self._postgres.check_user_password(username, p_hash):
            self._redis.del_log(message)
            self._redis.del_log_data(message)
            self._redis.set_username_status(message, 'logged', username)
            return 1
        else:
            self._redis.del_log_data(message)
            return 0
