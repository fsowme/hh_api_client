from telegram import Update
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext):
    telegram_id = update.effective_user.id
    update.message.reply_text(telegram_id)
