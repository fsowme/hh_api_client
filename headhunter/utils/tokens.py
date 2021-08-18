import time
from urllib.parse import urlencode

import requests

from config import FlaskConfig
from utils.errors import TokenValidationError
from utils.hh_requests import HHAnswerValidator


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
            "grant_type": FlaskConfig.GRANT_TYPE_REFRESH,
            "refresh_token": self.refresh_token,
        }
        response = requests.post(url=FlaskConfig.TOKEN_URL, data=data)
        response_validator = HHAnswerValidator(response)
        response_data = response_validator.token_response_validation()
        valid_token_data = self.validate_hh_token(response_data)
        self.__init__(**valid_token_data)
        return True

    @classmethod
    def get_user_token(cls, code: str, rdr_args: dict = None) -> "UserToken":
        redirect_uri = FlaskConfig.REDIRECT_URL
        redirect_uri += "" if rdr_args is None else f"?{urlencode(rdr_args)}"
        data = {
            "grant_type": FlaskConfig.GRANT_TYPE_CODE,
            "client_id": FlaskConfig.CLIENT_ID,
            "client_secret": FlaskConfig.CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "code": code,
        }
        response = requests.post(url=FlaskConfig.TOKEN_URL, data=data)
        now = int(time.time())
        response_validator = HHAnswerValidator(response)
        response_data = response_validator.token_response_validation()
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
