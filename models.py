import datetime

from sqlalchemy import Column, Integer, String, Date, create_engine, Boolean, update, DateTime
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
    age = Column(String)
    phone_number = Column(String)
    telegram_id = Column(String)
    username = Column(String)
    is_in_lottery = Column(Boolean)
    is_file_sending = Column(Boolean)
    creation_date = Column(Date)


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(String)
    grade = Column(String)
    creation_date = Column(DateTime)


async def add_user(dictionary: Dict):
    user = User()
    user.name = dictionary["name"]
    user.age = dictionary["age"]
    user.phone_number = dictionary["phone_number"]
    user.telegram_id = dictionary["telegram_id"]
    user.username = dictionary["username"]
    user.is_in_lottery = dictionary["is_in_lottery"]
    user.is_file_sending = dictionary["is_file_sending"]
    user.creation_date = datetime.datetime.now()
    session.add(user)
    session.commit()
    session.refresh(user)
    return user.id


async def get_all_users():
    return session.query(User).all()


async def add_grade(telegram_id, grade):
    grade_from_user = Grade()
    grade_from_user.telegram_id = telegram_id
    grade_from_user.grade = grade
    session.add(grade_from_user)
    session.commit()


Base.metadata.create_all(engine)
