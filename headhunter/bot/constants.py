class Keyboards:
    BACK = "Назад"
    MAIN_KEYBOARD = [
        ["Настрока аккаунта"],
        # ["Отклики"],
        # ["Вакансии"],
        # ["Подписаться на вакансии"],
    ]
    ACCOUNT_SETTINGS = [["Автопоиски"]]  # , ["Уведомления"]]
    SAVED_SEARCHES = [["Добавить", "Изменить"], ["Подписка"], [BACK]]

    SUB_VACANCIES = []


class States:
    MAIN_PAGE, ACCOUNT_SETTINGS, AUTOSEARCHES, SUB_VACANCIES = range(1, 5)
