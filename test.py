import datetime

from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from typing import Dict

Base = declarative_base()

engine = create_engine(f'sqlite:///db/{os.getenv("DB_NAME")}')

Session = sessionmaker(bind=engine)

session = Session()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    surname = Column(String)
    age = Column(Integer)
    subject = Column(String)
    language = Column(String)
    grade = Column(Integer)
    creation_date = Column(Date)


class BanList(Base):
    __tablename__ = "ban_list"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)


async def add_user(dictionary: Dict):
    user = User()
    user.name = dictionary["name"]
    # user.surname = dictionary["surname"]
    user.age = dictionary["age"]
    # user.subject = dictionary["subject"]
    # user.language = dictionary["language"]
    # user.grade = dictionary["grade"]
    user.creation_date = datetime.datetime.now()
    session.add(user)
    session.commit()


async def get_all_users():
    return session.query(User).all()


async def add_to_ban_list(user_id):
    user = BanList(user_id=user_id)
    session.add(user)
    session.commit()


async def get_ban_list():
    ban_list_users = session.query(BanList).all()
    return list(map(lambda banned_user: banned_user.user_id, ban_list_users))


Base.metadata.create_all(engine)