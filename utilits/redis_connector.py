import redis


class RedisConnector:
    def __init__(self):
        self.redis_connector = redis.Redis()

    def set_lang(self, message, lang):
        return self.redis_connector.set(f'user_language_{message.from_user.id}', lang)

    def get_lang(self, message):
        try:
            return self.redis_connector.get(f'user_language_{message.from_user.id}').decode()
        except AttributeError:
            return None

    def del_lang(self, message):
        return self.redis_connector.delete(f'user_language_{message.from_user.id}')

    def set_status(self, message, status):
        return self.redis_connector.set(f'user_status_{message.from_user.id}', status)

    def get_status(self, message):
        try:
            return self.redis_connector.get(f'user_status_{message.from_user.id}').decode()
        except AttributeError:
            return None

    def del_status(self, message):
        return self.redis_connector.delete(f'user_status_{message.from_user.id}')

    def set_reg_data(self, message, key, value):
        return self.redis_connector.hset(f'registration_{message.from_user.id}', key, value)

    def get_reg_data(self, message, key):
        try:
            return self.redis_connector.hget(f'registration_{message.from_user.id}', key).decode()
        except AttributeError:
            return None

    def del_reg_data(self, message):
        return self.redis_connector.delete(f'registration_{message.from_user.id}')
