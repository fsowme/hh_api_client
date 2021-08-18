from json.decoder import JSONDecodeError

import requests
from requests import Response

from config import FlaskConfig
from utils.errors import (
    AUTH_ERR,
    TOKEN_ERR,
    TOKEN_ERR_DETAIL,
    GetTokenError,
    InvalidResponseError,
    OAuthError,
    ServiceUnavailableError,
    UnknownError,
)


class HHRequester:
    base_url = FlaskConfig.HH_BASE_URL

    def get_user_info(self, access_token: str) -> dict:
        url = self.base_url + "/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        response_validator = HHAnswerValidator(response)
        response_data = response_validator.user_info_response_validation()
        return response_data


class HHAnswerValidator:
    def __init__(self, hh_response: Response) -> None:
        self.hh_response = hh_response

    def _get_json(self) -> dict:
        try:
            response_data = self.hh_response.json()
        except JSONDecodeError as error:
            error_text = "Response doesn't contain valid data"
            raise InvalidResponseError(error_text) from error
        return response_data

    def token_response_validation(self):
        hh_reply = self._get_json()
        if self.hh_response.status_code == 200:
            return hh_reply
        if self.hh_response.status_code in (400, 403):
            error = hh_reply.get("error_description") or hh_reply.get("error")
            if exc := (TOKEN_ERR.get(error) or TOKEN_ERR_DETAIL.get(error)):
                raise exc()
            raise GetTokenError("Unknow error from hh api")
        if self.hh_response.status_code == 503:
            raise ServiceUnavailableError("HH service is unavailable")
        raise UnknownError("Unknow error from hh api")

    def user_info_response_validation(self):
        response_data = self._get_json()
        if self.hh_response.status_code == 200:
            return response_data
        if self.hh_response.status_code == 403:
            error = response_data.get("value")
            if exc := AUTH_ERR.get(error):
                raise exc()
            raise OAuthError
        if self.hh_response.status_code == 503:
            raise ServiceUnavailableError("HH service is unavailable")
        raise UnknownError("Unknow error from hh api")
