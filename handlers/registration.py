from utilits.message_text import translator
from utilits.keyboard_manager import KeyboardManager
from utilits.redis_connector import RedisConnector
from utilits.postgres_connector import PostgresConnector
from sqlalchemy.exc import IntegrityError
from hashlib import sha256


class Registration:
    def __init__(self):
        self.kb = KeyboardManager()
        self.redis = RedisConnector()
        self.postgres = PostgresConnector()

    def chose_language(self, message, bot):
        if message.text == 'Українська':
            self.redis.set_lang(message, 'uk')
        elif message.text == 'English':
            self.redis.set_lang(message, 'en')
        else:
            bot.send_message(message.chat.id, translator['language_error']['en'],
                             reply_markup=self.kb.get_lang_kb())
            return
        bot.send_message(message.chat.id, translator['welcome_message'][
            self.redis.get_lang(message)], reply_markup=self.kb.get_start_kb())

    def reg_start(self, message, bot):
        if self.redis.get_status(message) == 'logged':
            bot.reply_to(message, translator['already_logged_error'][
                self.redis.get_lang(message)])
            return
        self.redis.set_user_status(message, 'wait_for_username')
        bot.reply_to(message, translator['enter_username'][self.redis.get_lang(message)])

    def enter_username(self, message, bot):
        username = message.text
        if len(username) > 16 or username.isspace():
            bot.reply_to(message, translator['username_error'][self.redis.get_lang(message)])
            return
        if self.postgres.check_user_exist(username):
            bot.reply_to(message, translator['username_already_used'][self.redis.get_lang(message)])
            return
        self.redis.set_user_status(message, 'wait_for_password')
        self.redis.set_reg_data(message, 'username', username)
        bot.reply_to(message, translator['reaction_for_username'][self.redis.get_lang(message)].format(username))
        bot.send_message(message.chat.id, translator['enter_password'][self.redis.get_lang(message)])

    def enter_password(self, message, bot):
        password = message.text
        bot.delete_message(message.chat.id, message.message_id)
        if len(password) < 5 or password.isspace() or len(password) > 20:
            bot.reply_to(message, translator['password_error'][self.redis.get_lang(message)])
            return
        self.redis.set_reg_data(message, 'password_hash', sha256(password.encode()).hexdigest())
        self.redis.set_user_status(message, 'repeat_password')
        bot.send_message(message.chat.id, translator['repeat_password'][self.redis.get_lang(message)])

    def repeat_password(self, message, bot):
        password = message.text
        bot.delete_message(message.chat.id, message.message_id)
        p_hash = self.redis.get_reg_data(message, 'password_hash')
        if p_hash == sha256(password.encode()).hexdigest():
            username = self.redis.get_reg_data(message, 'username')
            try:
                self.postgres.insert_user(username,
                                          password_hash=self.redis.get_reg_data(message, 'password_hash'))
            except IntegrityError:
                bot.send_message(message.chat.id, translator['registration_error'][self.redis.get_lang(message)],
                                 reply_markup=self.kb.get_start_kb())
            self.redis.del_reg_data(message)
            self.redis.set_user_status(message, 'logged', username)
            return True
        else:
            self.redis.set_user_status(message, 'wait_for_password')
            bot.reply_to(message, translator['repeat_password_error'][self.redis.get_lang(message)])
            bot.send_message(message.chat.id, translator['enter_password'][self.redis.get_lang(message)])
            return False
