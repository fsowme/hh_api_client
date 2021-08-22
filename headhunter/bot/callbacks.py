from urllib.parse import urlencode

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext

from bot.constants import Keyboards, States
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
<<<<<<< HEAD
    hh_auth_url = f"{BotConfig.REG_URL}?{params}"
    markup = ReplyKeyboardMarkup(Keyboards.MAIN_KEYBOARD)
=======
    hh_auth_url = f"{BotConfig.HH_BASE_URL}{BotConfig.REG_URL_PATH}?{params}"
    markup = ReplyKeyboardMarkup(BotConfig.MAIN_KEYBOARD)
>>>>>>> web
    update.message.reply_text(text.format(hh_auth_url), reply_markup=markup)
    return States.MAIN_PAGE


def account_settings(update: Update, context: CallbackContext):
    markup = ReplyKeyboardMarkup(Keyboards.ACCOUNT_SETTINGS)
    update.message.reply_text(
        "Вы в меню настроки аккаунта, выберите действие", reply_markup=markup
    )
    return States.ACCOUNT_SETTINGS


def autosearches(update: Update, context: CallbackContext):
    markup = ReplyKeyboardMarkup(Keyboards.SAVED_SEARCHES)
    text = "Тут можно посмотреть, изменить или удалить автопоиски"
    update.message.reply_text(text, reply_markup=markup)
    return States.AUTOSEARCHES


def autosearches_action(update: Update, context: CallbackContext):
    text = f"Action: {update.message.text}"
    if update.message.text == Keyboards.BACK_TEXT:
        return account_settings(update, None)
    update.message.reply_text(text)
    return States.AUTOSEARCHES
