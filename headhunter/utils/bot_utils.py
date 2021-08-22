from time import time

from telegram import Update
from telegram.ext import CallbackContext

from utils.errors import HHError, TokenValidationError
from utils.tokens import UserToken
from web import hh_requester, user_manager
from web.models import User


def check_user(register_function):
    def check_user_decorator(callback_function):
        def wrapper(*args):
            update: Update = args[0]
            context: CallbackContext = args[1]
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
    now = int(time())
    if now > user.expire_at:
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
