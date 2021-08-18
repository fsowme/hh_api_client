from urllib.parse import urlencode

from telegram import Update
from telegram.ext import CallbackContext

from config import BotConfig
from web import hh_requester, user_manager


def start(update: Update, context: CallbackContext):
    telegram_id = update.effective_user.id
    redirect_uri = f"{BotConfig.REDIRECT_URL}?telegram_id={telegram_id}"
    params = {
        "response_type": "code",
        "client_id": BotConfig.CLIENT_ID,
        "redirect_uri": redirect_uri,
    }
    params = str(urlencode(params))
    hh_auth_url = f"{BotConfig.REG_URL}?{params}"
    text = "Авторизуйтесь по ссылке с помощью учетной записи hh.ru:\n\n{}\n"
    update.message.reply_text(text.format(hh_auth_url))
