from telegram.ext import CommandHandler, ConversationHandler
from bot.callbacks import start

start_handler = CommandHandler("start", callback=start)

main_conversation = ConversationHandler(
    entry_points=[start_handler],
    states={},
    fallbacks=[],
    name="main_conv",
    persistent=True,
    allow_reentry=True,
)
