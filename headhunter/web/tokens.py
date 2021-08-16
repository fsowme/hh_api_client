import time

import requests

from .config import Config
from .errors import TokenValidationError


class UserToken:
    def __init__(
        self, access_token: str, refresh_token: str, expire_at: int
    ) -> None:
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expire_at = expire_at

    def update_token(self, force=False) -> bool:
        if self.expire_at < time.time() and not force:
            return False
        data = {
            "grant_type": Config.GRANT_TYPE_REFRESH,
            "refresh_token": self.refresh_token,
        }
        response = requests.post(url=Config.TOKEN_URL, data=data)
        response.raise_for_status()
        response_data = response.json()
        valid_token_data = self.validate_hh_token(response_data)
        self.__init__(**valid_token_data)
        return True

    @classmethod
    def get_user_token(cls, code: str) -> "UserToken":
        data = {
            "grant_type": Config.GRANT_TYPE_CODE,
            "client_id": Config.CLIENT_ID,
            "client_secret": Config.CLIENT_SECRET,
            "redirect_uri": Config.REDIRECT_URL,
            "code": code,
        }
        response = requests.post(url=Config.TOKEN_URL, data=data)
        now = int(time.time())
        # TODO: validate hh answer instead raise_for_status()
        response.raise_for_status()
        response_data: dict = response.json()
        valid_token_data = cls.validate_hh_token(response_data, now)
        return cls(**valid_token_data)

    @staticmethod
    def validate_hh_token(token_data: dict, expire_offset: int = 0) -> dict:
        _HH_TOKEN_FIELDS = "access_token", "refresh_token", "expires_in"
        valid_data = {}
        if not token_data:
            raise TokenValidationError("Token data is empty")
        for field in _HH_TOKEN_FIELDS:
            if not (value := token_data.get(field)):
                error_text = "Token data doesn't contain '{}' or it is invalid"
                raise TokenValidationError(error_text.format(field))
            if field == "expires_in":
                continue
            valid_data[field] = value
        expires_in = token_data["expires_in"]
        try:
            int(expires_in)
        except (TypeError, ValueError):
            error_text = "Field 'expires_in' contain invalid data ({})"
            raise TokenValidationError(error_text.format(expires_in))
        valid_data["expire_at"] = int(expires_in) + expire_offset
        return valid_data
