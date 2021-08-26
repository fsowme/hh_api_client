from functools import wraps
from time import time

from telegram import Update
from telegram.ext import CallbackContext

from utils.errors import HHError, TokenValidationError
from utils.tokens import UserToken
from web import hh_requester, user_manager
from web.models import User


def get_autosearches(break_function):
    """
    Decorator factory

    Get autosearches and put it to context if answer from HH api is valid
    and data of answer is not empty. Remove autosearches from context after run
    decorated callback function and before return

    Factory get just one parameter: callback function to be called if
    answer from api of HH invalid or data of answer is empty.

    Decorated function must have two required arguments and
    one optional argument:
        required:
            1. update: telegram.Update
            2. context: telegram.ext.CallbackContext
        optional:
            3. page: int = 0
    Wrapper function

    """

    def get_autosearches_decorator(callback_function):
        def wrapper(update: Update, context: CallbackContext, page: int = 0):
            access_token: str = context.user_data["access_token"]
            search_response = hh_requester.get_autosearches(access_token, page)
            if not search_response.is_valid:
                update.message.reply_text(
                    "Не удалось получить список автопоисков."
                )
                return break_function(update, context)
            clean_searches = search_response.cleaned_data
            if clean_searches.get("found") == 0:
                update.message.reply_text(
                    "Список сохранённых автопоисков пуст"
                )
                return break_function(update, context)
            context.user_data["autosearches"] = clean_searches
            wrapped_result = callback_function(update, context)
            try:
                del context.user_data["autosearches"]
            except KeyError:
                pass
            return wrapped_result

        return wrapper

    return get_autosearches_decorator


def check_user(register_function):
    """
    Decorator factory

    Check user in db and if user is exist then get and put token to context.

    Factory get just one parameter: callback function to be called if
    user not exist

    Decorated function must have two arguments:
        1. update: telegram.Update
        2. context: telegram.ext.CallbackContext
    """

    def check_user_decorator(callback_function):
        """Decorator for Telegram bot callback functions"""

        def wrapper(update: Update, context: CallbackContext):
            telegram_id = update.effective_user.id
            try:
                if not (user := user_manager.get(telegram_id=telegram_id)):
                    raise TokenValidationError()
                token_to_context(user, context)
            except TokenValidationError:
                return register_function(update, None)
            return callback_function(update, context)

        return wrapper

    return check_user_decorator


def token_to_context(user: User, context: CallbackContext) -> None:
    if user.expire_at <= int(time()):
        token_response = hh_requester.update_token(user.refresh_token)
        if not token_response.is_valid:
            raise HHError()
        token = UserToken.token_from_dict(token_response.cleaned_data)
        user.access_token = token.access_token
        user.refresh_token = token.refresh_token
        user.expire_at = token.expire_at
        user.save()
    context.user_data["access_token"] = user.access_token
    context.user_data["refresh_token"] = user.refresh_token
    context.user_data["expire_at"] = user.expire_at
