from web import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    access_token = db.Column(db.String(100), unique=True, nullable=False)
    refresh_token = db.Column(db.String(100), unique=True, nullable=False)
    expire_at = db.Column(db.Integer, nullable=False)
