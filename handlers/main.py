from utilits.message_text import translator
from utilits.keyboard_manager import KeyboardManager
from utilits.redis_connector import RedisConnector


class Main:
    def __init__(self):
        self.kb = KeyboardManager()
        self.redis = RedisConnector()

    def start(self, message, bot):
        if not self.redis.get_lang(message) or self.redis.get_lang(message) == 'choosing':
            self.redis.set_lang(message, 'choosing')
            bot.reply_to(message, translator['chose_language']['en'],
                         reply_markup=self.kb.get_lang_kb())
        elif self.redis.get_status(message) != 'logged':
            self.get_main_menu(message, bot)
        else:
            self.redis.del_status(message)
            bot.reply_to(message, translator['welcome_message'][self.redis.get_lang(message)])
            self.get_main_menu(message, bot)

    def get_main_menu(self, message, bot):
        bot.send_message(message.chat.id, translator['welcome_for_register'][self.redis.get_lang(message)],
                         reply_markup=self.kb.get_main_kb())
