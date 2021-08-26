from telegram import Bot, ReplyKeyboardMarkup

from config import BotConfig
from bot.constants import Keyboards


def hello(bot: Bot, telegram_id):
    markup = ReplyKeyboardMarkup(Keyboards.MAIN_KEYBOARD, resize_keyboard=True)
    text = BotConfig.HELLO_MESSAGE
    bot.send_message(text=text, reply_markup=markup, chat_id=telegram_id)
