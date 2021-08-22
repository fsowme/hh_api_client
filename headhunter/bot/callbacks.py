from urllib.parse import urlencode

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, Bot
from telegram.ext import CallbackContext

from bot.constants import Keyboards, States
from config import BotConfig
from utils.bot_utils import check_user
from web import user_manager, hh_requester


def hello(bot: Bot, telegram_id):
    markup = ReplyKeyboardMarkup(Keyboards.MAIN_KEYBOARD)
    text = BotConfig.HELLO_MESSAGE
    bot.send_message(text=text, reply_markup=markup, chat_id=telegram_id)


def start(update: Update, context: CallbackContext):
    message = update.message or update.callback_query.message
    telegram_id = update.effective_user.id
    text = "Авторизуйтесь по ссылке с помощью учетной записи hh.ru:\n\n{}\n"
    markup = ReplyKeyboardRemove()
    state = None
    if user := user_manager.get(telegram_id=telegram_id):
        text = (
            "Вы уже авторизованы с помощью аккаунта hh.ru, зарегестрированного"
            f" на почту: '{user.email}', если хотите привязать другой аккаунт,"
            " то перейдите по ссылке:\n\n{}\n"
        )
        markup = ReplyKeyboardMarkup(Keyboards.MAIN_KEYBOARD)
        state = States.MAIN_PAGE
    redirect_uri = f"{BotConfig.REDIRECT_URI}?telegram_id={telegram_id}"
    params = {
        "response_type": "code",
        "client_id": BotConfig.CLIENT_ID,
        "redirect_uri": redirect_uri,
    }
    params = urlencode(params)
    hh_auth_url = f"{BotConfig.HH_BASE_URL}{BotConfig.REG_URL_PATH}?{params}"
    message.reply_text(text.format(hh_auth_url), reply_markup=markup)
    return state


def account_settings(update: Update, context: CallbackContext):
    markup = ReplyKeyboardMarkup(Keyboards.ACCOUNT_SETTINGS)
    update.message.reply_text(
        "Вы в меню настроки аккаунта, выберите действие", reply_markup=markup
    )
    return States.ACCOUNT_SETTINGS


@check_user(start)
def autosearches(update: Update, context: CallbackContext):
    access_token = context.user_data["access_token"]
    autosearch_response = hh_requester.get_autosearches(access_token)
    if not autosearch_response.is_valid:
        update.message.reply_text("Не удалось получить список автопоисков.")
        return account_settings(update, None)

    clean_searches = autosearch_response.cleaned_data
    searches_names = "\n".join(
        [search["name"] for search in clean_searches["items"]]
    )
    text = (
        "Тут можно посмотреть, изменить или удалить автопоиски\n"
        f"{searches_names}"
    )
    markup = ReplyKeyboardMarkup(Keyboards.SAVED_SEARCHES)
    update.message.reply_text(text, reply_markup=markup)
    return States.AUTOSEARCHES


def autosearches_action(update: Update, context: CallbackContext):
    text = f"Action: {update.message.text}"
    if update.message.text == Keyboards.BACK_TEXT:
        return account_settings(update, None)
    update.message.reply_text(text)
    return States.AUTOSEARCHES
