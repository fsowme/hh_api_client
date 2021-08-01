from flask import Flask

from web import views
from web.config import Config
from web.models import shutdown_db_session


class Application:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)
        self.app.teardown_appcontext(shutdown_db_session)
        self.init_views()

    def init_views(self):
        self.app.add_url_rule("/", view_func=views.test)
        self.app.add_url_rule("/oauth", view_func=views.oauth)

    # def __getattr__(self, item):
    #     return getattr(self.app, item)

    def run(self, host=None, port=None, debug=None):
        self.app.run(host, port, debug)

    def wsgi_app(self, environ, start_response):
        return self.app.wsgi_app(environ, start_response)

    def __call__(self, environ, start_response):
        return self.app.__call__(environ, start_response)
