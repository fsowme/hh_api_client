from web.app import Application

application = Application()

if __name__ == "__main__":
    application.run("0.0.0.0", "8000", True)
