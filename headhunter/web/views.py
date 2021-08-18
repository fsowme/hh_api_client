from flask import request
from telegram import Update
from werkzeug.exceptions import BadRequest

from bot import BOT, DISPATCHER
from utils import errors
from utils.tokens import UserToken
from web import app, hh_requester, user_manager


def test():
    return {"test": True}


def oauth():
    if not (code := request.args.get("code")):
        return {"error": "The requested url must contain authorization code"}
    if not (telegram_id := request.args.get("telegram_id")):
        return {"error": "Invalid telegram id"}
    rdr_uri_args = {"telegram_id": telegram_id}
    try:
        token = UserToken.get_user_token(code, rdr_uri_args)
    except errors.CodeNotFound:
        return {"error": "Invalid authorization code"}
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
        user_info = hh_requester.get_user_info(token.access_token)
    except errors.OAuthError:
        # TODO: log it
        return {"error": "Authorization error"}
    if not (user_email := user_info.get("email")):
        return {"error": "User doesn't have email"}
    user_fields = token.__dict__ | {"telegram_id": telegram_id}
    try:
        user_manager.update_or_create(email=user_email, defaults=user_fields)
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


app.add_url_rule("/", view_func=test)
app.add_url_rule("/oauth/", view_func=oauth)
app.add_url_rule("/webhook/", view_func=webhook, methods=["GET", "POST"])
# app.add_url_rule(f"/{BotConfig.TOKEN}/webhook", view_func=views.webhook)
