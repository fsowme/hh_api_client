from telegram.ext.callbackcontext import CallbackContext

from utils.errors import HHError
from web import app, hh_requester, user_manager


def get_new_vacancies(context: CallbackContext):
    with app.app_context():
        users = user_manager.values("telegram_id", "access_token")
        for user in users:
            token = user["access_token"]
            all_searches = hh_requester.get_autosearches(token, recursive=True)
            if not all_searches:
                continue

            # new_url = all_searches[0]["new_items"]["url"]
            # vacancies = hh_requester.get_vacancies(
            #     new_url, token, recursive=True
            # )
