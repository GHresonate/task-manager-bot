from utilits.keyboard_manager import KeyboardManager
from connectors.redis_connector import RedisConnector
from connectors.postgres_connector import PostgresConnector


class BaseHandler:
    def __init__(self):
        self._kb = KeyboardManager()
        self._redis = RedisConnector()
        self._postgres = PostgresConnector()