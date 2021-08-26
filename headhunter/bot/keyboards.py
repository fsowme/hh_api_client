from telegram import InlineKeyboardButton as IKButton
from telegram import InlineKeyboardMarkup as IKMarkup

from bot.constants import CBQueryData, Keyboards


def autosearches_keyboard(searches: dict) -> IKMarkup:
    keyboard = []
    for search in searches["items"]:
        _id, name = search["id"], search["name"]
        text, button_data = name, CBQueryData.SUB % _id
        if search["subscription"]:
            text, button_data = Keyboards.TAG % name, CBQueryData.UNSUB % _id
        keyboard.append([IKButton(text, callback_data=button_data)])
    back_button = IKButton(Keyboards.BACK, callback_data=Keyboards.BACK)
    keyboard.append([back_button])
    page, pages = int(searches["page"]), int(searches["pages"])
    paginator = []
    if page > 0:
        prev_page = IKButton(Keyboards.PREVIOUS, callback_data=str(page - 1))
        paginator.append(prev_page)
    if page < pages - 1:
        next_page = IKButton(Keyboards.NEXT, callback_data=str(page + 1))
        paginator.append(next_page)
    keyboard.append(paginator)
    return IKMarkup(keyboard)
