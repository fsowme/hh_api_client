from flask import request
from telegram import Update
from werkzeug.exceptions import BadRequest

from bot import BOT, DISPATCHER
from bot.callbacks import hello
from utils.errors import UnknownError, TokenValidationError
from utils.tokens import UserToken
from web import hh_requester, user_manager


def test():
    return {"test": True}


def oauth():
    if not (code := request.args.get("code")):
        return {"error": "The requested url must contain authorization code"}
    if not (telegram_id := request.args.get("telegram_id")):
        return {"error": "Invalid telegram id"}
    rdr_uri_args = {"telegram_id": telegram_id}
    token_hh_response = hh_requester.get_user_token(code, rdr_uri_args)
    if not token_hh_response.is_valid:
        return {"error": token_hh_response.msg}
    try:
        token = UserToken.token_from_dict(token_hh_response.cleaned_data)
    except TokenValidationError as error:
        # TODO: log it
        msg = error.error_text if error.for_user else UnknownError.error_text
        return {"error": msg}
    user_hh_response = hh_requester.get_user_info(token.access_token)
    if not user_hh_response.is_valid:
        return {"error": user_hh_response.msg}

    if not (user_email := user_hh_response.cleaned_data.get("email")):
        return {"error": "User doesn't have email"}
    user_fields = {
        "telegram_id": telegram_id,
        "access_token": token.access_token,
        "refresh_token": token.refresh_token,
        "expire_at": token.expire_at,
    }
    try:
        user_manager.update_or_create(email=user_email, defaults=user_fields)
    except Exception:
        # TODO: log it
        return {"error": "Internal server error"}
    hello(BOT, telegram_id)
    return "Ok"


def webhook():
    try:
        request_data = request.json
    except BadRequest:
        # TODO: log it
        pass
    telegram_update = Update.de_json(request_data, BOT)
    DISPATCHER.process_update(telegram_update)
    return "Ok"
