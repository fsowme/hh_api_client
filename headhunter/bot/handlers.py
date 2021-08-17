from telegram.ext import CommandHandler
from bot.callbacks import start

start_handler = CommandHandler("start", callback=start)
