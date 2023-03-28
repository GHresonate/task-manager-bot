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

        class Tasks(self._Base):
            __table__ = Table("Tasks", self._Base.metadata, autoload_with=self._engine)

        self._Tasks = Tasks
        self._Users = Users

    def execute(self, sql):
        result = self._session.execute(sql)
        self._session.commit()
        return result

    def insert_task(self, username, title, description):
        state = 'n'
        ins = insert(self._Tasks).values(username=username, title=title, description=description, state=state)
        self.execute(ins)

    def update_task_state(self, task_id, state):
        change = update(self._Tasks).where(self._Tasks.task_id == task_id).values(state=state)
        self.execute(change)

    def delete_task(self, task_id):
        del_sql = delete(self._Users).where(self._Tasks.task_id == task_id)
        self.execute(del_sql)

    def get_users_tasks(self, username):
        sel = select(self._Tasks.task_id, self._Tasks.title, self._Tasks.description, self._Tasks.state). \
            where(self._Tasks.username == username)
        result = self.execute(sel)
        return result.all()

    def delete_users_tasks(self, username):
        del_sql = delete(self._Tasks).where(self._Tasks.username == username)
        self.execute(del_sql)


    # here user part starts

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

    def change_password(self, username, password_hash):
        change = update(self._Users).where(self._Users.username == username).values(password_hash=password_hash)
        self.execute(change)
