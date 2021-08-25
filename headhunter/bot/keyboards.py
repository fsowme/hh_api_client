from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants import Keyboards


def autosearches_keyboard(searches: dict) -> InlineKeyboardMarkup:
    keyboard = []
    for search in searches["items"]:
        name: str = search["name"]
        if search["subscription"]:
            name += " \U00002705"
        search_id: int = search["id"]
        keyboard.append([InlineKeyboardButton(name, callback_data=search_id)])
    back_text = Keyboards.BACK
    keyboard.append([InlineKeyboardButton(back_text, callback_data=back_text)])
    return InlineKeyboardMarkup(keyboard)
