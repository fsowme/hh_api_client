from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from .config import CONFIG

engine = create_engine(CONFIG.DB, convert_unicode=True)
db_session = scoped_session(sessionmaker(engine))
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    access_token = Column(String(100), unique=True, nullable=False)
    refresh_token = Column(String(100), unique=True, nullable=False)


def shutdown_db_session(exception=None):
    db_session.remove()
