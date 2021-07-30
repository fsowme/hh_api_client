from flask import Flask

from . import views
from .config import CONFIG
from .models import shutdown_db_session


class Application:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(CONFIG)
        self.init_views()
        self.app.teardown_appcontext(shutdown_db_session)

    def init_views(self):
        self.app.add_url_rule("/", view_func=views.test)

    def run(self, host=None, port=None, debug=None):
        self.app.run(host, port, debug)
