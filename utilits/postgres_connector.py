import sqlalchemy
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import Table, insert, select, delete


class PostgresConnector:
    def __init__(self):
        self.engine = sqlalchemy.create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
        self.session = Session(self.engine)
        self.Base = declarative_base()

        class Users(self.Base):
            __table__ = Table('Users', self.Base.metadata, autoload_with=self.engine)

        self.Users = Users

    def execute(self, sql):
        result = self.session.execute(sql)
        self.session.commit()
        return result

    def insert_user(self, username, password_hash):
        ins = insert(self.Users).values(username=username, password_hash=password_hash)
        self.execute(ins)

    def delete_user(self, username):
        del_sql = delete(self.Users).where(self.Users.username == username)
        self.execute(del_sql)

    def check_user(self, username):
        sel = select(self.Users.username).where(self.Users.username == username)
        result = self.execute(sel)
        return bool(result.one_or_none())
