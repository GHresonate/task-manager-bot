from connectors.redis_connector import RedisConnector


class Filter:
    def __init__(self):
        self._redis = RedisConnector()

    def chose_language(self, message):
       # print(self._redis.get_lang(message) == 'choosing')
        return self._redis.get_lang(message) == 'choosing'

    def enter_username(self, message):
        #print(self._redis.get_status(message) == 'wait_for_username')
        return self._redis.get_status(message) == 'wait_for_username'

    def enter_password(self, message):
        #print(self._redis.get_status(message) == 'wait_for_password')
        return self._redis.get_status(message) == 'wait_for_password'

    def repeat_password(self, message):
        #print(self._redis.get_status(message) == 'repeat_password')
        return self._redis.get_status(message) == 'repeat_password'

    def log_username(self, message):
        # print(4)
        # print(self._redis.get_log(message) == 'wait_for_username')
        return self._redis.get_log(message) == 'wait_for_username'

    def log_password(self, message):
        # print(3)
        # print(self._redis.get_log(message) == 'wait_for_password')
        return self._redis.get_log(message) == 'wait_for_password'

    def change_username_start(self, message):
        # print(2)
        # print(message.text == 'Change username')
        return message.text == 'Change username'

    def change_username_result(self, message):
        # print("filter")
        # print(self._redis.get_acc_actions(message))
        # print(self._redis.get_acc_actions(message) == 'chose_name')
        return self._redis.get_acc_actions(message) == 'chose_name'

    def change_password_start(self, message):
        return message.text == 'Change password'

    def change_password_first(self, message):
        return self._redis.get_acc_actions(message) == 'chose_password'

    def change_password_result(self, message):
        return self._redis.get_acc_actions(message) == 'repeat_password'

    def delete_password_start(self, message):
        return message.text == 'Delete account'

    def delete_password_result(self, message):
        return self._redis.get_acc_actions(message) == 'del_account' and message.text == 'Yes'

