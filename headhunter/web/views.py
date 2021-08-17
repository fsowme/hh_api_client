from urllib.parse import urlencode

from flask import redirect, request

from .config import Config
from .db_manager import DBManager
from .errors import AccountIsLocked, LoginNotVerified, PasswordInvalidated
from .hh_requests import HHRequester
from .models import User
from .tokens import UserToken

USER_MANAGER = DBManager(User)
HH_REQUESTER = HHRequester()


def test():
    return {"test": True}


def oauth():
    if not (code := request.args.get("code")):
        params = {
            "response_type": "code",
            "client_id": Config.CLIENT_ID,
            "redirect_uri": Config.REDIRECT_URL,
        }
        hh_auth_url = "".join([Config.REG_URL, "?", str(urlencode(params))])
        return redirect(hh_auth_url)
    try:
        token = UserToken.get_user_token(code)
    except AccountIsLocked:
        return {"error": "Account is locked"}
    except PasswordInvalidated:
        return {"error": "Password expired"}
    except LoginNotVerified:
        return {"error": "Acoount isn't verified"}
    user_info = HH_REQUESTER.get_user_info(token.access_token)
    user_email = user_info["email"]
    USER_MANAGER.update_or_create(email=user_email, defaults=token.__dict__)
    return {
        "at": token.access_token,
        "rt": token.refresh_token,
        "ea": token.expire_at,
    }
