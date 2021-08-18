from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    access_token = db.Column(db.String(100), unique=True, nullable=False)
    refresh_token = db.Column(db.String(100), unique=True, nullable=False)
    expire_at = db.Column(db.Integer, nullable=False)
    telegram_id = db.Column(db.Integer, unique=True)
    responses = relationship("Response", backref="user")


class Response(db.Model):
    __tablename__ = "response"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
