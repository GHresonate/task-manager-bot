import sqlalchemy
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import Table, insert, select, delete, update


class PostgresConnector:
    def __init__(self):
        self._engine = sqlalchemy.create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
        self._session = Session(self._engine)
        self._Base = declarative_base()

        class Users(self._Base):
            __table__ = Table('Users', self._Base.metadata, autoload_with=self._engine)

        self._Users = Users

    def execute(self, sql):
        result = self._session.execute(sql)
        self._session.commit()
        return result

    def insert_user(self, username, password_hash):
        ins = insert(self._Users).values(username=username, password_hash=password_hash)
        self.execute(ins)

    def delete_user(self, username):
        del_sql = delete(self._Users).where(self._Users.username == username)
        self.execute(del_sql)

    def check_user_exist(self, username):
        sel = select(self._Users.username).where(self._Users.username == username)
        result = self.execute(sel)
        return bool(result.one_or_none())

    def check_user_password(self, username, password_hash):
        sel = select(self._Users.username).where(self._Users.username == username) \
            .where(self._Users.password_hash == password_hash)
        result = self.execute(sel)
        return bool(result.one_or_none())

    def change_username(self, old_username, new_username):
        change = update(self._Users).where(self._Users.username == old_username).values(username=new_username)
        self.execute(change)
