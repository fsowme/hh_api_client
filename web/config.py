import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    DB = os.getenv("DB")
    REDIRECT_URL = os.getenv("REDIRECT_URL")
    # hh.ru
    TOKEN_URL = os.getenv("TOKEN_URL")
    GRANT_TYPE = os.getenv("GRANT_TYPE")
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
