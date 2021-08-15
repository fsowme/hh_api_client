import os

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.getcwd())


class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("DB") or f"sqlite:///{os.path.join(basedir, 'sqlite.db')}"
    )
    JSON_AS_ASCII = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIRECT_URL = os.getenv("REDIRECT_URL")
    # hh.ru
    TOKEN_URL = os.getenv("TOKEN_URL")
    GRANT_TYPE_CODE = os.getenv("GRANT_TYPE")
    GRANT_TYPE_REFRESH = os.getenv("GRANT_TYPE_REFRESH")
    GRANT_TYPE_CC = os.getenv("GRANT_TYPE_CC")
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REG_URL = os.getenv("REG_URL")
