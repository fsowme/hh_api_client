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
    responses = db.relationship("Response", backref="user")


class Response(db.Model):
    __tablename__ = "response"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    vacancy_id = db.Column(
        db.Integer, db.ForeignKey("vacancy.id"), nullable=False
    )


class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200))
    vacancies = db.relationship("Vacancy", backref="company")


class Vacancy(db.Model):
    __tablename__ = "vacancy"
    id = db.Column(db.Integer, primary_key=True)
    prof = db.Column(db.String(200))
    url = db.Column(db.String(200))
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    responses = db.relationship("Response", backref="vacancy")
