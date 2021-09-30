import os

from dotenv import load_dotenv
from telegram.ext import PicklePersistence

load_dotenv()

basedir = os.path.abspath(os.getcwd())


class Config:
    CLIENT_ID = os.getenv("CLIENT_ID")
    REDIRECT_URI = os.getenv("REDIRECT_URL")
    HH_BASE_URL = os.getenv("HH_BASE_URL")
    HH_BASE_API_URL = os.getenv("HH_BASE_API_URL")
    REG_URL_PATH = os.getenv("REG_URL_PATH")
    AUTOSEARCHES_PATH = os.getenv("AUTOSEARCHES_PATH")
    VACANCIES_PATH = os.getenv("VACANCIES_PATH")


class FlaskConfig(Config):
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"
    )
    # SQLALCHEMY_DATABASE_URI = (
    #     os.getenv("DB") or f"sqlite:///{os.path.join(basedir, 'sqlite.db')}"
    # )
    JSON_AS_ASCII = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # hh.ru
    TOKEN_URL_PATH = os.getenv("TOKEN_URL_PATH")
    GRANT_TYPE_CODE = os.getenv("GRANT_TYPE_CODE")
    GRANT_TYPE_REFRESH = os.getenv("GRANT_TYPE_REFRESH")
    GRANT_TYPE_CC = os.getenv("GRANT_TYPE_CC")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")


class BotConfig(Config):
    TOKEN = os.getenv("TG_TOKEN")
    PERSISTENCE = PicklePersistence(os.getenv("PERSISTENCE") or "persist.bin")
    HELLO_MESSAGE = "Привет, спасибо за регистрацию."
    NOTIFICATION_INTERVAL = 30  # minutes
