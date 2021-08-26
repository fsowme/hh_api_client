import re

from bot.constants import CBQueryData


class CBDataChecker:
    def is_sub_search(self, text: str) -> bool:
        sub, unsub = CBQueryData.SUB_PREFIX, CBQueryData.UNSUB_PREFIX
        pattern = rf"^({sub}|{unsub}){CBQueryData.SEPARATOR}[0-9]+$"
        return bool(re.match(pattern, text))


data_checker = CBDataChecker()
