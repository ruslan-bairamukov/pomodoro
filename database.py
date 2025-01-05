import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config.settings import settings


engine = create_engine("sqlite:///pomodoro.db")


def get_db_connection() -> Session:
    return sessionmaker(engine)
