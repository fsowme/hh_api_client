from flask import Flask
from flask_migrate import Migrate

from config import BotConfig, FlaskConfig
from web import views
from web.models import db

app = Flask(__name__)
app.config.from_object(FlaskConfig)
db.init_app(app)
migrate = Migrate(app, db)
app.add_url_rule("/", view_func=views.test)
app.add_url_rule("/oauth/", view_func=views.oauth)
app.add_url_rule("/webhook/", view_func=views.webhook, methods=["GET", "POST"])
# app.add_url_rule(f"/{BotConfig.TOKEN}/webhook", view_func=views.webhook)
