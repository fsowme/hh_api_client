from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)

from bot import callbacks as cb
from bot.constants import Keyboards, States

start_handler = CommandHandler("start", callback=cb.start)

main_conversation = ConversationHandler(
    entry_points=[start_handler],
    states={
        States.MAIN_PAGE: [
            MessageHandler(
                Filters.regex("^Настрока аккаунта$"), cb.account_settings
            )
        ],
        States.ACCOUNT_SETTINGS: [
            MessageHandler(Filters.regex("^Автопоиски$"), cb.autosearches)
        ],
        States.AUTOSEARCHES: [
            MessageHandler(Filters.regex("^Добавить$"), cb.add_autosearch),
            MessageHandler(Filters.regex("^Изменить$"), cb.change_autosearch),
            MessageHandler(Filters.regex("^Подписка$"), cb.sub_autosearch),
            MessageHandler(Filters.regex("^Назад$"), cb.account_settings),
        ],
        States.SUB_VACANCIES: [
            CallbackQueryHandler(cb.autosearches, pattern=Keyboards.BACK),
            CallbackQueryHandler(cb.sub_autosearch_action, pattern=""),
        ],
    },
    fallbacks=[],
    name="main_conv",
    persistent=True,
    allow_reentry=True,
)
