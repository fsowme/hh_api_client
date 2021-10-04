from dotenv import load_dotenv
from telegram.ext import CallbackContext, Updater

from bot.handlers import main_conversation
from bot.scheduler import send_vacancies
from config import BotConfig

load_dotenv()


def job_hello(context: CallbackContext):
    message = f"Hello {context.user_data}"
    context.bot.send_message(chat_id=128609524, text=message)


UPDATER = Updater(BotConfig.TOKEN, persistence=BotConfig.PERSISTENCE)
DISPATCHER, BOT = UPDATER.dispatcher, UPDATER.bot
DISPATCHER.add_handler(main_conversation)

notify_job = UPDATER.job_queue
notify_job.run_repeating(send_vacancies, interval=600, first=5)
# notify_job.run_once(send_vacancies, when=3)
