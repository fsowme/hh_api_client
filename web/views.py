import requests
from flask import redirect, request, session

from web.config import Config


def test():
    # test code
    # user = User(name="name_1", access_token="at_1", refresh_token="rt_1")
    # db_session.add(user)
    # db_session.commit()
    return {"test": True}


def oauth():
    if not (code := request.args.get("code")):
        return redirect(Config.REDIRECT_URL)
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
