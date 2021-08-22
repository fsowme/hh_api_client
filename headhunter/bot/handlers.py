from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)

from bot.callbacks import (
    start,
    account_settings,
    autosearches,
    autosearches_action,
)
from bot.constants import States

start_handler = CommandHandler("start", callback=start)


main_conversation = ConversationHandler(
    entry_points=[start_handler],
    states={
        States.MAIN_PAGE: [
            MessageHandler(
                Filters.regex("^Настрока аккаунта$"), account_settings
            )
        ],
        States.ACCOUNT_SETTINGS: [
            MessageHandler(Filters.regex("^Автопоиски$"), autosearches)
        ],
        States.AUTOSEARCHES: [
            MessageHandler(
                Filters.regex("^Добавить$|^Назад$"), autosearches_action
            ),
            CallbackQueryHandler(autosearches_action, pattern=""),
        ],
    },
    fallbacks=[],
    name="main_conv",
    persistent=True,
    allow_reentry=True,
)
