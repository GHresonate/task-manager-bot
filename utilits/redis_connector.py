import redis


class RedisConnector:
    def __init__(self):
        self.redis_connector = redis.Redis()

    def set_lang(self, message, lang):
        self.redis_connector.hset(f'user_{message.from_user.id}', "lang", lang)

    def get_lang(self, message):
        try:
            return self.redis_connector.hget(f'user_{message.from_user.id}', "lang").decode()
        except AttributeError:
            return None

    def del_lang(self, message):
        self.redis_connector.hdel(f'user_{message.from_user.id}', "lang")

    def set_user_status(self, message, status, username):
        self.redis_connector.hmset(f'user_{message.from_user.id}', {
            "status": status,
            "username": username
        })

    def get_username(self, message):
        try:
            return self.redis_connector.hget(f'user_{message.from_user.id}', "username").decode()
        except AttributeError:
            return None

    def get_status(self, message):
        try:
            return self.redis_connector.hget(f'user_{message.from_user.id}', "status").decode()
        except AttributeError:
            return None

    def del_status(self, message):
        self.redis_connector.hdel(f'user_{message.from_user.id}', "status")

    def set_reg_data(self, message, key, value):
        self.redis_connector.hset(f'registration_{message.from_user.id}', key, value)

    def get_reg_data(self, message, key):
        try:
            return self.redis_connector.hget(f'registration_{message.from_user.id}', key).decode()
        except AttributeError:
            return None

    def del_reg_data(self, message):
        self.redis_connector.delete(f'registration_{message.from_user.id}')

    def set_log(self, message, lang):
        self.redis_connector.set(f'log_status_{message.from_user.id}', lang)

    def get_log(self, message):
        try:
            return self.redis_connector.get(f'log_status_{message.from_user.id}').decode()
        except AttributeError:
            return None

    def del_log(self, message):
        self.redis_connector.delete(f'log_status_{message.from_user.id}')

    def set_log_data(self, message, key):
        self.redis_connector.set(f'login_{message.from_user.id}', key)

    def get_log_data(self, message):
        try:
            return self.redis_connector.get(f'login_{message.from_user.id}').decode()
        except AttributeError:
            return None

    def del_log_data(self, message):
        self.redis_connector.delete(f'login_{message.from_user.id}')

    def set_acc_actions(self, message, status):
        self.redis_connector.set(f'account_{message.from_user.id}', status)

    def get_acc_actions(self, message, status):
        self.redis_connector.get(f'account_{message.from_user.id}')

    def del_acc_actions(self, message, status):
        self.redis_connector.delete(f'account_{message.from_user.id}')
