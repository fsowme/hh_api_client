class Keyboards:
    BACK = "Назад"
    TAG = "\U00002705 %s"
    PREVIOUS = "Предыдущая стр."
    NEXT = "Следующая стр."
    MAIN_KEYBOARD = [
        ["Настрока аккаунта"],
    ]
    ACCOUNT_SETTINGS = [["Автопоиски"], [BACK]]
    SAVED_SEARCHES = [["Подписка"], [BACK]]


class States:
    MAIN_PAGE, ACCOUNT_SETTINGS, AUTOSEARCHES, SUB_VACANCIES = range(1, 5)


class CBQueryData:
    SEPARATOR = ";"
    SUB_PREFIX, UNSUB_PREFIX = "sub", "unsub"
    SUB = "".join([SUB_PREFIX, SEPARATOR, "%s"])
    UNSUB = "".join([UNSUB_PREFIX, SEPARATOR, "%s"])
