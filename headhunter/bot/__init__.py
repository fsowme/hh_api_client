from dotenv import load_dotenv
from telegram.ext import CallbackContext, Updater


from bot.handlers import main_conversation
from bot.scheduler import get_new_vacancies
from config import BotConfig

load_dotenv()


def job_hello(context: CallbackContext):
    print(context)
    message = f"Hello {context.user_data}"
    context.bot.send_message(chat_id=128609524, text=message)


UPDATER = Updater(BotConfig.TOKEN, persistence=BotConfig.PERSISTENCE)
DISPATCHER, BOT = UPDATER.dispatcher, UPDATER.bot
DISPATCHER.add_handler(main_conversation)

j = UPDATER.job_queue
# j.run_repeating(get_new_vacancies, interval=10)
j.run_once(get_new_vacancies, when=3)
j.start()
