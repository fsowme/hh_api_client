from urllib.parse import urlencode

import requests
from flask import redirect, request, session

from .config import Config


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
        print(hh_auth_url)
        return redirect(hh_auth_url)
    data = {
        "grant_type": Config.GRANT_TYPE,
        "client_id": Config.CLIENT_ID,
        "client_secret": Config.CLIENT_SECRET,
        "code": code,
    }
    response = requests.post(Config.TOKEN_URL, data=data)
    # TODO: validate hh answer instead raise_for_status()
    response.raise_for_status()
    response_data: dict = response.json()
    session.update(response_data)
    return response_data
