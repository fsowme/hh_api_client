from web import app, db
from web.models import User

context = {"User": User, "db": db}

app.shell_context_processor(lambda: context)
if __name__ == "__main__":
    app.run("0.0.0.0", "8080", True)
