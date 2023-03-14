import redis


class RedisConnector:
    def __init__(self):
        self._redis_connector = redis.Redis()

    def set_lang(self, message, lang):
        self._redis_connector.hset(f'user_{message.from_user.id}', "lang", lang)

    def get_lang(self, message):
        try:
            lang = self._redis_connector.hget(f'user_{message.from_user.id}', "lang").decode()
            return lang or 'en'
        except AttributeError:
            return None

    def del_lang(self, message):
        self._redis_connector.hdel(f'user_{message.from_user.id}', "lang")

    def set_username_status(self, message, status, username="loging"):
        self._redis_connector.hmset(f'user_{message.from_user.id}', {
            "status": status,
            "username": username
        })

    def change_username(self, message, username):
        self._redis_connector.hset(f'user_{message.from_user.id}', "username", username)

    def get_username(self, message):
        try:
            return self._redis_connector.hget(f'user_{message.from_user.id}', "username").decode()
        except AttributeError:
            return None

    def get_status(self, message):
        try:
            return self._redis_connector.hget(f'user_{message.from_user.id}', "status").decode()
        except AttributeError:
            return None

    def del_status(self, message):
        self._redis_connector.hdel(f'user_{message.from_user.id}', "status")

    def del_username(self, message):
        self._redis_connector.hdel(f'user_{message.from_user.id}', "username")

    def set_reg_data(self, message, key, value):
        self._redis_connector.hset(f'registration_{message.from_user.id}', key, value)

    def get_reg_data(self, message, key):
        try:
            return self._redis_connector.hget(f'registration_{message.from_user.id}', key).decode()
        except AttributeError:
            return None

    def del_reg_data(self, message):
        self._redis_connector.delete(f'registration_{message.from_user.id}')

    def set_log(self, message, lang):
        self._redis_connector.set(f'log_status_{message.from_user.id}', lang)

    def get_log(self, message):
        try:
            return self._redis_connector.get(f'log_status_{message.from_user.id}').decode()
        except AttributeError:
            return None

    def del_log(self, message):
        self._redis_connector.delete(f'log_status_{message.from_user.id}')

    def set_log_data(self, message, key):
        self._redis_connector.set(f'login_{message.from_user.id}', key)

    def get_log_data(self, message):
        try:
            return self._redis_connector.get(f'login_{message.from_user.id}').decode()
        except AttributeError:
            return None

    def del_log_data(self, message):
        self._redis_connector.delete(f'login_{message.from_user.id}')

    def set_acc_actions(self, message, status):
        self._redis_connector.set(f'account_{message.from_user.id}', status)

    def get_acc_actions(self, message):
        try:
            return self._redis_connector.get(f'account_{message.from_user.id}').decode()
        except AttributeError:
            return None

    def del_acc_actions(self, message):
        self._redis_connector.delete(f'account_{message.from_user.id}')

    def set_change_pass(self, message, password_hash):
        self._redis_connector.set(f'password_change_{message.from_user.id}', password_hash)

    def get_change_pass(self, message):
        try:
            return self._redis_connector.get(f'password_change_{message.from_user.id}').decode()
        except AttributeError:
            return None

    def del_change_pass(self, message):
        self._redis_connector.delete(f'password_change_{message.from_user.id}')
