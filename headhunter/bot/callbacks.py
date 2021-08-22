from urllib.parse import urlencode

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext

from config import BotConfig
from web import user_manager


def start(update: Update, context: CallbackContext):
    telegram_id = update.effective_user.id
    text = "Авторизуйтесь по ссылке с помощью учетной записи hh.ru:\n\n{}\n"
    if user := user_manager.get(telegram_id=telegram_id):
        text = (
            "Вы уже авторизованы с помощью аккаунта hh.ru, зарегестрированного"
            f" на почту: '{user.email}', если хотите привязать другой аккаунт,"
            " то перейдите по ссылке:\n\n{}\n"
        )
    redirect_uri = f"{BotConfig.REDIRECT_URI}?telegram_id={telegram_id}"
    params = {
        "response_type": "code",
        "client_id": BotConfig.CLIENT_ID,
        "redirect_uri": redirect_uri,
    }
    params = urlencode(params)
    hh_auth_url = f"{BotConfig.HH_BASE_URL}{BotConfig.REG_URL_PATH}?{params}"
    markup = ReplyKeyboardMarkup(BotConfig.MAIN_KEYBOARD)
    update.message.reply_text(text.format(hh_auth_url), reply_markup=markup)
