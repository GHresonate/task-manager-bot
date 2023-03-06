from utilits.message_text import translator
from utilits.keyboard_manager import KeyboardManager
from utilits.redis_connector import RedisConnector
from utilits.postgres_connector import PostgresConnector


class Account:
    def __init__(self):
        self.kb = KeyboardManager()
        self.redis = RedisConnector()
        self.postgres = PostgresConnector()

    def change_name(self, message, bot):
        pass

    def change_password(self, message, bot):
        pass

    def delete_account(self, message, bot):
        pass

