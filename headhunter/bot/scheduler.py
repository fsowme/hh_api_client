from telegram.ext.callbackcontext import CallbackContext

from utils.errors import HHError
from web import app, hh_requester, user_manager


def get_new_vacancies(context: CallbackContext):
    with app.app_context():
        users = user_manager.values("telegram_id", "access_token")
        for user in users:
            token = user["access_token"]
            all_searches = get_searches(token)


def get_searches(token: str, items: list = None, page: int = 0) -> list:
    """Recursively get items from any number of pages from api of hh.ru"""
    items = [] if items is None else items
    response = hh_requester.get_autosearches(token, page)
    if not response.is_valid:
        raise HHError()
    searches = response.cleaned_data
    items.extend(searches["items"])
    pages = searches["pages"]
    next_page = searches["page"] + 1
    if next_page == pages or searches["found"] < 1:
        return items
    return get_searches(token, items, next_page)
