from web.app import Application


application = Application()
flask_app = application.app


if __name__ == "__main__":
    application.run("0.0.0.0", "8000", True)
