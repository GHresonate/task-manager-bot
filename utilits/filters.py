from utilits.redis_connector import RedisConnector


class Filter:
    def __init__(self):
        self.redis = RedisConnector()

    def chose_language(self, message):
        return self.redis.get_lang(message) == 'choosing'

    def enter_username(self, message):
        return self.redis.get_status(message) == 'wait_for_username'

    def enter_password(self, message):
        return self.redis.get_status(message) == 'wait_for_password'

    def repeat_password(self, message):
        return self.redis.get_status(message) == 'repeat_password'

    def log_username(self, message):
        return self.redis.get_log(message) == 'wait_for_username'

    def log_password(self, message):
        return self.redis.get_log(message) == 'wait_for_password'
