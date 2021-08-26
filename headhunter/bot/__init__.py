from dotenv import load_dotenv
from telegram.ext import Updater

from config import BotConfig
from bot.handlers import main_conversation

load_dotenv()

UPDATER = Updater(BotConfig.TOKEN, persistence=BotConfig.PERSISTENCE)
DISPATCHER, BOT = UPDATER.dispatcher, UPDATER.bot
DISPATCHER.add_handler(main_conversation)
