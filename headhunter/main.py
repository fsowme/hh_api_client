from web import app, db, views
from web.models import User

context = {"User": User, "db": db}
app.add_url_rule("/", view_func=views.test)
app.add_url_rule("/oauth/", view_func=views.oauth)
app.add_url_rule("/webhook/", view_func=views.webhook, methods=["GET", "POST"])

app.shell_context_processor(lambda: context)
if __name__ == "__main__":
    app.run("0.0.0.0", "8080", True)
