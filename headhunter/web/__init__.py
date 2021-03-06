from flask import Flask

from flask_migrate import Migrate

from config import FlaskConfig
from utils.db_manager import DBManager
from utils.hh_requests import HHRequester
from web.models import User, db


app = Flask(__name__)
app.config.from_object(FlaskConfig)
db.init_app(app)
migrate = Migrate(app, db)

user_manager = DBManager(User, db)
hh_requester = HHRequester()
