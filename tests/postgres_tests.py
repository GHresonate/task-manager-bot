import unittest

from utilits.postgres_connector import PostgresConnector


class PostgresTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.postgres = PostgresConnector()
        super().__init__(*args, **kwargs)

    def test_check_user(self):
        self.assertFalse(self.postgres.check_user("test_username"))
        self.postgres.insert_user("test_username", "test12345")
        self.assertTrue(self.postgres.check_user("test_username"))
        self.postgres.delete_user("test_username")


if __name__ == '__main__':
    unittest.main()
