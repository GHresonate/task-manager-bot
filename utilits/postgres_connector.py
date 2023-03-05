import sqlalchemy
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import Table, insert, select


class PostgresConnector:
    def __init__(self):
        self.engine = sqlalchemy.create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
        self.session = Session(self.engine)
        self.Base = declarative_base()

        class Users(self.Base):
            __table__ = Table('Users', self.Base.metadata, autoload_with=self.engine)

        self.Users = Users

    def insert_user(self, username, password_hash):
        ins = insert(self.Users).values(username=username, password_hash=password_hash)
        self.session.execute(ins)
        self.session.commit()

    def check_user(self, username):
        stmt = select(self.Users.username).where(self.Users.username == username)
        return bool(self.session.execute(stmt).one_or_none())
