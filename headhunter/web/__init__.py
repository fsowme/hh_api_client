from flask import Flask
from flask_migrate import Migrate

from . import views
from .config import Config
from .models import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)
app.add_url_rule("/", view_func=views.test)
app.add_url_rule("/oauth", view_func=views.oauth)
