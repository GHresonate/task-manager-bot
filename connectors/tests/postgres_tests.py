import unittest

from connectors.postgres_connector import PostgresConnector


class PostgresTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self._postgres = PostgresConnector()
        super().__init__(*args, **kwargs)

    def test_check_user(self):
        self._postgres.delete_user("test_username")
        self.assertFalse(self._postgres.check_user_exist("test_username"))
        self._postgres.insert_user("test_username", "test12345")
        self.assertTrue(self._postgres.check_user_exist("test_username"))
        self._postgres.delete_user("test_username")

    def test_user_password(self):
        self._postgres.delete_user("test_username")
        self._postgres.insert_user("test_username", "test12345")
        self.assertTrue(self._postgres.check_user_password("test_username", "test12345"))
        self.assertFalse(self._postgres.check_user_password("test_username", "test123456"))
        self.assertFalse(self._postgres.check_user_password("test_username_2", "test12345"))
        self._postgres.delete_user("test_username")


if __name__ == '__main__':
    unittest.main()
