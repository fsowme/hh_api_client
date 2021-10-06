from flask import render_template, request
from telegram import Update
from werkzeug.exceptions import BadRequest

from bot import BOT, DISPATCHER
from bot.external_funcs import hello
from utils.tokens import UserToken
from utils.errors import TokenValidationError, UnknownError
from web import hh_requester, user_manager


def test():
    context = {"status": "test", "message": 42}
    return render_template("reg.html", **context)


def oauth():
    err_status, success_status = "Ошибка", "Успешно"
    if not (code := request.args.get("code")):
        message = "The requested url must contain authorization code"
        return render_template("reg.html", status=err_status, message=message)
    if not (telegram_id := request.args.get("telegram_id")):
        message = "Invalid telegram id"
        return render_template("reg.html", status=err_status, message=message)
    rdr_uri_args = {"telegram_id": telegram_id}
    token_hh_response = hh_requester.get_user_token(code, rdr_uri_args)
    if not token_hh_response.is_valid:
        message = token_hh_response.msg
        return render_template("reg.html", status=err_status, message=message)
    try:
        token = UserToken.token_from_dict(token_hh_response.cleaned_data)
    except TokenValidationError as err:
        # TODO: log it
        message = err.error_text if err.for_user else UnknownError.error_text
        return render_template("reg.html", status=err_status, message=message)
    user_hh_response = hh_requester.get_user_info(token.access_token)
    if not user_hh_response.is_valid:
        message = user_hh_response.msg
        return render_template("reg.html", status=err_status, message=message)
    if not (user_email := user_hh_response.cleaned_data.get("email")):
        message = "User doesn't have email"
        return render_template("reg.html", status=err_status, message=message)
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
        message = "Internal server error"
        return render_template("reg.html", status=err_status, message=message)
    hello(BOT, telegram_id)
    message = (
        "Вы авторизовались с помощью аккаунта hh.ru зарегестрированного на "
        f"email: {user_email}"
    )
    return render_template("reg.html", status=success_status, message=message)


def webhook():
    try:
        request_data = request.json
    except BadRequest:
        # TODO: log it
        pass
    telegram_update = Update.de_json(request_data, BOT)
    DISPATCHER.process_update(telegram_update)
    return "Ok"
