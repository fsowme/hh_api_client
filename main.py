from web.app import Application

app = Application()
if __name__ == "__main__":
    app.run("0.0.0.0", "8080", True)
