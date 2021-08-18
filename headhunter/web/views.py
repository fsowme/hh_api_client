from urllib.parse import urlencode

from flask import redirect, request
from telegram import Update
from werkzeug.exceptions import BadRequest

import utils.errors as errors
from bot import BOT, DISPATCHER
from config import FlaskConfig
from utils.db_manager import DBManager
from utils.hh_requests import HHRequester
from utils.tokens import UserToken
from web.models import User, db

USER_MANAGER = DBManager(User, db)
HH_REQUESTER = HHRequester()


def test():
    return {"test": True}


def oauth():
    if not (code := request.args.get("code")):
        params = {
            "response_type": "code",
            "client_id": FlaskConfig.CLIENT_ID,
            "redirect_uri": FlaskConfig.REDIRECT_URL,
        }
        params = str(urlencode(params))
        hh_auth_url = "".join([FlaskConfig.REG_URL, "?", params])
        return redirect(hh_auth_url)
    try:
        token = UserToken.get_user_token(code)
    except errors.AccountIsLocked:
        return {"error": "Account is locked"}
    except errors.PasswordInvalidated:
        return {"error": "Password expired"}
    except errors.LoginNotVerified:
        return {"error": "Acoount isn't verified"}
    except errors.TokenWasRevoked:
        return {"error": "Token was revoked"}
    except errors.CodeExpired:
        return {"error": "authorization_code expired"}
    except errors.ForbiddenError:
        return {"error": "Too many requests, try again later"}
    except errors.GetTokenError:
        # TODO: log it
        return {"error": "Internal server error"}
    try:
        user_info = HH_REQUESTER.get_user_info(token.access_token)
    except errors.OAuthError:
        # TODO: log it
        return {"error": "Authorization error"}
    if not (user_email := user_info.get("email")):
        return {"error": "User doesn't have email"}
    token_fields = token.__dict__
    try:
        USER_MANAGER.update_or_create(email=user_email, defaults=token_fields)
    except Exception:
        # TODO: log it
        return {"error": "Internal server error"}
    return {
        "at": token.access_token,
        "rt": token.refresh_token,
        "ea": token.expire_at,
    }


def webhook():
    try:
        request_data = request.json
    except BadRequest:
        # TODO: log it
        pass
    telegram_update = Update.de_json(request_data, BOT)
    DISPATCHER.process_update(telegram_update)
    return "Ok"
