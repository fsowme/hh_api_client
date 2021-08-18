import os
from telegram.ext import PicklePersistence
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.getcwd())


class Config:
    CLIENT_ID = os.getenv("CLIENT_ID")
    REDIRECT_URL = os.getenv("REDIRECT_URL")
    REG_URL = os.getenv("REG_URL")


class FlaskConfig(Config):
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("DB") or f"sqlite:///{os.path.join(basedir, 'sqlite.db')}"
    )
    JSON_AS_ASCII = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # hh.ru
    HH_BASE_URL = os.getenv("HH_BASE_URL")
    TOKEN_URL = os.getenv("TOKEN_URL")
    GRANT_TYPE_CODE = os.getenv("GRANT_TYPE_CODE")
    GRANT_TYPE_REFRESH = os.getenv("GRANT_TYPE_REFRESH")
    GRANT_TYPE_CC = os.getenv("GRANT_TYPE_CC")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")


class BotConfig(Config):
    TOKEN = os.getenv("TG_TOKEN")
    PERSISTENCE = PicklePersistence(os.getenv("PERSISTENCE")) or "persist.bin"
