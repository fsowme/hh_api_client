from telegram.ext import CallbackQueryHandler as CBQHandler
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
)

from bot import callbacks as cb
from bot.constants import States

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
            CBQHandler(cb.sub_autosearch_change_page, pattern="^[0-9]$"),
            CBQHandler(cb.sub_autosearch_action),
        ],
    },
    fallbacks=[],
    name="main_conv",
    persistent=True,
    allow_reentry=True,
    conversation_timeout=120,
)
