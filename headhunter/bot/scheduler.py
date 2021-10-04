from typing import List, Union

from telegram import Bot, ParseMode
from telegram.ext.callbackcontext import CallbackContext

from web import app, hh_requester, user_manager
from utils.hh_requests import get_all_pages


def send_vacancies(context: CallbackContext) -> None:
    with app.app_context():
        users = user_manager.values("telegram_id", "access_token")
        for user in users:
            token, telegram_id = user["access_token"], user["telegram_id"]
            send_new_vacancies(token, context.bot, telegram_id)


def send_new_vacancies(user_token: str, bot: Bot, telegram_id: int) -> None:
    options = {"token": user_token}
    searches = get_all_pages(hh_requester.get_autosearches, **options)
    for search in searches:

        if not search["subscription"]:
            continue
        new_vacancies_url = search["new_items"]["url"]
        options.update({"url": new_vacancies_url})
        vacancies = get_all_pages(hh_requester.get_vacancies, **options)
        for vacancy in vacancies:
            message_text = make_message_text(vacancy)
            bot.send_message(
                chat_id=telegram_id,
                text=message_text,
                parse_mode=ParseMode.HTML,
            )


def make_message_text(vacancy: List[dict]) -> str:
    name = vacancy.get("name")
    if salary := vacancy.get("salary"):
        currency: str = salary.get("currency")
        salary_from: Union[str, int] = salary.get("from") or "-"
        salary_to: Union[str, int] = salary.get("to") or "-"
        salary = f" From: {salary_from}, to: {salary_to}, currency: {currency}"
    else:
        salary = "По договорённости"
    url = vacancy.get("alternate_url")
    employer = vacancy.get("employer") or {}
    company_name = employer.get("name")
    snippet = vacancy.get("snippet") or {}
    requirements = snippet.get("requirement")
    responsibility = snippet.get("responsibility")
    text = (
        f"Глянь, новая вакансия:\n\n{name}\n\nЗарплата: {salary}\n\n"
        f"Компания: {company_name}\n\nТребования: {requirements}\n\n"
        f"Обязанности: {responsibility}\n\nURL: {url}\n\n"
    )
    text = text.replace("<highlighttext>", "<b>")
    text = text.replace("</highlighttext>", "</b>")
    return text
