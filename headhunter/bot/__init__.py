from dotenv import load_dotenv
from telegram.ext import Updater

from bot.handlers import main_conversation
from bot.scheduler import send_vacancies
from config import BotConfig

load_dotenv()


UPDATER = Updater(BotConfig.TOKEN, persistence=BotConfig.PERSISTENCE)
DISPATCHER, BOT = UPDATER.dispatcher, UPDATER.bot
DISPATCHER.add_handler(main_conversation)

notify_job = UPDATER.job_queue
notify_job.run_repeating(
    send_vacancies, interval=BotConfig.NOTIFICATION_INTERVAL * 60, first=5
)
