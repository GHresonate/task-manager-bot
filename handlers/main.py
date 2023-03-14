from utilits.message_text import translator
from utilits.keyboard_manager import KeyboardManager
from connectors.redis_connector import RedisConnector


class Main:
    def __init__(self):
        self._kb = KeyboardManager()
        self._redis = RedisConnector()

    def start(self, message, bot):
        if not self._redis.get_lang(message) or self._redis.get_lang(message) == 'choosing':
            self._redis.set_lang(message, 'choosing')
            bot.send_message(message.chat.id, translator['chose_language']['en'],
                             reply_markup=self._kb.get_lang_kb())
        elif self._redis.get_status(message) != 'logged':
            bot.send_message(message.chat.id, translator['welcome_message'][
                self._redis.get_lang(message)], reply_markup=self._kb.get_main_kb())
        else:
            self.get_main_menu(message, bot)

    def get_main_menu(self, message, bot):
        bot.send_message(message.chat.id, translator['welcome_for_register'][self._redis.get_lang(message)],
                         reply_markup=self._kb.get_main_kb())

    def filter_anonim(self, message, bot):
        bot.send_message(message.chat.id, translator['unknown_user'][self._redis.get_lang(message)],
                         reply_markup=self._kb.get_start_kb())
    def info(self, message, bot):
        bot.send_message(message.chat.id, translator['info'][self._redis.get_lang(message)],
                         reply_markup=self._kb.get_start_kb())
