from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from . import views
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.add_url_rule("/", view_func=views.test)
app.add_url_rule("/oauth", view_func=views.oauth)
