from urllib.parse import urlencode

from telegram import Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext

from bot.constants import Keyboards, States
from bot.keyboards import autosearches_keyboard
from config import BotConfig
from utils.bot_utils import check_user, get_autosearches
from web import user_manager


def hello(bot: Bot, telegram_id):
    markup = ReplyKeyboardMarkup(Keyboards.MAIN_KEYBOARD, resize_keyboard=True)
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
        markup = ReplyKeyboardMarkup(
            Keyboards.MAIN_KEYBOARD, resize_keyboard=True
        )
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
def account_settings(update: Update, context: CallbackContext):
    markup = ReplyKeyboardMarkup(
        Keyboards.ACCOUNT_SETTINGS, resize_keyboard=True
    )
    update.message.reply_text(
        "Вы в меню настроки аккаунта, выберите действие", reply_markup=markup
    )
    return States.ACCOUNT_SETTINGS


@check_user(start)
def autosearches(update: Update, context: CallbackContext):
    text = "Тут можно настрить автопоиски\n"
    markup = ReplyKeyboardMarkup(
        Keyboards.SAVED_SEARCHES, resize_keyboard=True, one_time_keyboard=True
    )
    update.message.reply_text(text, reply_markup=markup)
    return States.AUTOSEARCHES


@check_user(start)
def add_autosearch(update: Update, context: CallbackContext):
    text = f"Action: {update.message.text}"
    update.message.reply_text(text)
    return States.AUTOSEARCHES


@check_user(start)
def change_autosearch(update: Update, context: CallbackContext):
    return add_autosearch(update, context)


@get_autosearches(account_settings)
@check_user(start)
def sub_autosearch(update: Update, context: CallbackContext):

    markup = autosearches_keyboard(context.user_data["autosearches"])
    text = "Подпишись на вакансии найденные автопоиском:"
    if update.callback_query:
        # TODO: make unsub from autosearch
        update.callback_query.message.edit_text(text, reply_markup=markup)
        update.callback_query.answer()
        return States.SUB_VACANCIES
    update.message.reply_text(text, reply_markup=markup)
    return States.SUB_VACANCIES


@check_user(start)
def sub_autosearch_action(update: Update, context: CallbackContext):
    print(update.callback_query)
    return sub_autosearch(update, context)
