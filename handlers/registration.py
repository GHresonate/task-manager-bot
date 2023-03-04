from util.message_text import translator
from util.keyboard_manager import KeyboardManager
from util.redis_connector import RedisConnector
from hashlib import sha256


class Registration:
    def __init__(self):
        self.kb = KeyboardManager()
        self.redis = RedisConnector()

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
        self.redis.set_status(message,  'wait_for_username')
        bot.reply_to(message, translator['enter_username'][self.redis.get_lang(message)])

    def enter_username(self, message, bot):
        username = message.text
        if len(username) > 16 or username.isspace():
            bot.reply_to(message, translator['username_error'][self.redis.get_lang(message)])
            return
        self.redis.set_status(message,  'wait_for_password')
        self.redis.set_reg_data(message, 'username', username)
        bot.reply_to(message, translator['reaction_for_username'][self.redis.get_lang(message)].format(username))
        bot.send_message(message.chat.id, translator['enter_password'][self.redis.get_lang(message)])

    def enter_password(self, message, bot):
        password = message.text
        if len(password) < 5 or password.isspace() or len(password) > 20:
            bot.reply_to(message, translator['password_error'][self.redis.get_lang(message)])
            return
        self.redis.set_status(message, 'repeat_password')
        self.redis.set_reg_data(message, 'password_hash', sha256(password.encode()).hexdigest())
        bot.send_message(message.chat.id, translator['repeat_password'][self.redis.get_lang(message)])

    def repeat_password(self, message, bot):
        password = message.text
        p_hash = self.redis.get_reg_data(message, 'password_hash')
        if p_hash == sha256(password.encode()).hexdigest():
            ins = insert(Users).values(username=self.redis.get_reg_data(message, 'username'),
                                       password_hash=self.redis.get_reg_data(message, 'password_hash'))
            session.execute(ins)
            redis_connector.delete(f'registration_{message.from_user.id}')
            session.commit()
            self.redis.set_status(message, 'logged')
            return get_main_menu(message)
        else:
            self.redis.set_status(message,  'wait_for_password')
            bot.reply_to(message, translator['repeat_password_error'][self.redis.get_lang(message)])
            bot.send_message(message.chat.id, translator['enter_password'][self.redis.get_lang(message)])
