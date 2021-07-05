from sqlalchemy import (
    create_engine,
    String,
    Integer,
    Column,
)

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from sqlalchemy.ext.declarative import declarative_base

from decouple import config

DATABASE_URL = config("DATABASE_URL")


ENGINE = create_engine(DATABASE_URL, echo=False)
session_factory = sessionmaker(bind=ENGINE)
SESSION = scoped_session(session_factory)
BASE = declarative_base()


class UpdaterData(BASE):
    __tablename__ = "updater_data"
    updater_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)

    def __init__(self, updater_id, username):
        self.updater_id = updater_id
        self.user_id = user_id


class UserData(BASE):
    __tablename__ = "user_data"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(100))
    type = Column(String(10))

    def __init__(user_id, username, type=None):
        self.user_id = user_id
        self.username = username
        self.type = type


BASE.metadata.create_all(ENGINE)


def fetch_usernames(updater_id):
    return (
        SESSION.query(
            UserData.user_id,
            UserData.username,
        )
        .filter(UserData.user_id == UpdaterData.user_id)
        .filter(UpdaterData.updater_id == updater_id)
        .all()
    )
