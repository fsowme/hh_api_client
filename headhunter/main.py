from config import BotConfig
from web import app, db
from web.models import User
from web.views import oauth, test, webhook

context = {"User": User, "db": db}

app.add_url_rule("/", view_func=test)
app.add_url_rule("/oauth/", view_func=oauth)
app.add_url_rule(
    f"/{BotConfig.TOKEN}/webhook/", view_func=webhook, methods=["GET", "POST"]
)
app.shell_context_processor(lambda: context)
if __name__ == "__main__":
    from bot import notify_job

    notify_job.start()
    app.run("0.0.0.0", "8080")
