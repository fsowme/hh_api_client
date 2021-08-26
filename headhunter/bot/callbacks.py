from urllib.parse import urlencode

from telegram import ReplyKeyboardMarkup as RKMarkup
from telegram import ReplyKeyboardMarkup as RKRemove
from telegram import Update
from telegram.ext import CallbackContext as CBContext

from bot.constants import CBQueryData, Keyboards, States
from bot.keyboards import autosearches_keyboard
from bot.patterns import data_checker
from config import BotConfig
from utils.bot_utils import check_user, get_autosearches
from web import hh_requester, user_manager


def start(update: Update, context: CBContext):
    message = update.message or update.callback_query.message
    telegram_id = update.effective_user.id
    text = "Авторизуйтесь по ссылке с помощью учетной записи hh.ru:\n\n{}\n"
    markup = RKRemove()
    state = None
    if user := user_manager.get(telegram_id=telegram_id):
        text = (
            "Вы уже авторизованы с помощью аккаунта hh.ru, зарегестрированного"
            f" на почту: '{user.email}', если хотите привязать другой аккаунт,"
            " то перейдите по ссылке:\n\n{}\n"
        )
        markup = RKMarkup(Keyboards.MAIN_KEYBOARD, resize_keyboard=True)
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


@check_user(start)
def account_settings(update: Update, context: CBContext):
    markup = RKMarkup(Keyboards.ACCOUNT_SETTINGS, resize_keyboard=True)
    text = "Вы в меню настроки аккаунта, выберите действие"
    update.message.reply_text(text, reply_markup=markup)
    return States.ACCOUNT_SETTINGS


@check_user(start)
def autosearches(update: Update, context: CBContext):
    text = "Тут можно настрить автопоиски\n"
    keyboard = Keyboards.SAVED_SEARCHES
    markup = RKMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    if query := update.callback_query:
        query.message.reply_text(text, reply_markup=markup)
        query.answer()
    else:
        update.message.reply_text(text, reply_markup=markup)
    return States.AUTOSEARCHES


@check_user(start)
def add_autosearch(update: Update, context: CBContext):
    text = f"Action: {update.message.text}"
    update.message.reply_text(text)
    return States.AUTOSEARCHES


@check_user(start)
def change_autosearch(update: Update, context: CBContext):
    return add_autosearch(update, context)


@get_autosearches(account_settings)
@check_user(start)
def sub_autosearch(update: Update, context: CBContext, page: int = 0):
    markup = autosearches_keyboard(context.user_data["autosearches"])
    text = "Подпишись на вакансии найденные автопоиском:"
    if update.callback_query:
        # TODO: make unsub from autosearch
        update.callback_query.message.edit_text(text, reply_markup=markup)
        update.callback_query.answer()
        return States.SUB_VACANCIES
    update.message.reply_text(text, reply_markup=markup)
    return States.SUB_VACANCIES


@get_autosearches(account_settings)
@check_user(start)
def sub_autosearch_action(update: Update, context: CBContext, page: int = 0):
    query = update.callback_query
    if not data_checker.is_sub_search(query.data):
        text = f"Error with button, try again or press '{Keyboards.BACK}'"
        query.answer(text, show_alert=True)
        # TODO: log it
    command, search_id = query.data.split(sep=";")
    access_token = context.user_data["access_token"]

    if command == CBQueryData.SUB_PREFIX:
        hh_requester.sub_autosearch(access_token, search_id)
    else:
        hh_requester.sub_autosearch(access_token, search_id, False)
    query.answer("Statuses updated")
    # return sub_autosearch(update, context)


def sub_autosearch_change_page(update: Update, context: CBContext):
    return sub_autosearch(update, context, update.callback_query.data)
