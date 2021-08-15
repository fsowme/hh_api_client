from urllib.parse import urlencode

from flask import redirect, request

from .config import Config
from .utils import UserToken


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
    token = UserToken.get_user_token(code)
