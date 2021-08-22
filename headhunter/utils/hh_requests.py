from abc import ABC, abstractclassmethod
from json.decoder import JSONDecodeError
from typing import Dict, List
from urllib.parse import urlencode

import requests
from requests import Response

from config import FlaskConfig
from utils.errors import (
    AUTH_ERR,
    TOKEN_ERR,
    GetTokenError,
    InvalidResponseError,
    OAuthError,
    ServiceUnavailableError,
    UnknownError,
    ValidationError,
)


class HHReplyValidator(ABC):
    def __init__(self, hh_response: Response) -> None:
        self.hh_response = hh_response

    def _get_json(self) -> dict:
        try:
            response_data = self.hh_response.json()
        except JSONDecodeError as error:
            raise InvalidResponseError() from error
        return response_data

    @abstractclassmethod
    def validate(self) -> dict:
        pass


class HHReplyTokenValidator(HHReplyValidator):
    def validate(self) -> dict:
        hh_reply = self._get_json()
        if self.hh_response.status_code == 200:
            return hh_reply
        if self.hh_response.status_code in (400, 403):
            error = hh_reply.get("error_description") or hh_reply.get("error")
            error: str
            exception = TOKEN_ERR.get(error, GetTokenError)
            raise exception()
        if self.hh_response.status_code == 503:
            raise ServiceUnavailableError()
        raise UnknownError()


class HHReplyUserInfoValidator(HHReplyValidator):
    def validate(self) -> dict:
        hh_reply = self._get_json()
        if self.hh_response.status_code == 200:
            return hh_reply
        response_errors: List[Dict[str, str]] = hh_reply.get("errors")
        if self.hh_response.status_code == 503:
            raise ServiceUnavailableError()
        for response_error in response_errors:
            error_type = response_error.get("type")
            if error_type == "oauth":
                error: str = response_error.get("value")
                exception = AUTH_ERR.get(error, OAuthError)
                raise exception()
        raise UnknownError()


class HHResponse:
    def __init__(self, validator: HHReplyValidator):
        self.validator = validator
        self.cleaned_data = None
        self.msg = None
        self._is_valid = None
        self._response_data = None

    @property
    def is_valid(self, force=False):
        if self._is_valid is not None and not force:
            return self._is_valid
        try:
            self._response_data = self.validator._get_json()
            self.cleaned_data = self.validator.validate()
        except (InvalidResponseError, ValidationError) as e:
            # TODO: log it
            self.msg = e.error_text if e.for_user else UnknownError.error_text
            self._is_valid = False
        else:
            self._is_valid = True
        return self._is_valid


class HHRequester:
    client_id = FlaskConfig.CLIENT_ID
    client_secret = FlaskConfig.CLIENT_SECRET
    grant_type_code = FlaskConfig.GRANT_TYPE_CODE
    grant_type_refresh = FlaskConfig.GRANT_TYPE_REFRESH
    base_url = FlaskConfig.HH_BASE_URL
    api_base_url = FlaskConfig.HH_BASE_API_URL
    token_url_path = FlaskConfig.TOKEN_URL_PATH
    redirect_uri = FlaskConfig.REDIRECT_URI
    autosearches_path = FlaskConfig.AUTOSEARCHES_PATH

    def get_user_token(self, code: str, rdr_args: dict = None) -> HHResponse:
        full_rdr_uri = self.redirect_uri
        full_rdr_uri += "" if rdr_args is None else f"?{urlencode(rdr_args)}"
        data = {
            "grant_type": self.grant_type_code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": full_rdr_uri,
            "code": code,
        }
        url = "".join([self.base_url, self.token_url_path])
        response = requests.post(url=url, data=data)
        validator = HHReplyTokenValidator(response)
        return HHResponse(validator)

    def update_token(self, refresh_token) -> HHResponse:
        data = {
            "grant_type": self.grant_type_refresh,
            "refresh_token": refresh_token,
        }
        url = "".join([self.base_url, self.token_url_path])
        response = requests.post(url=url, data=data)
        validator = HHReplyTokenValidator(response)
        return HHResponse(validator)

    def get_user_info(self, access_token: str) -> HHResponse:
        url = self.api_base_url + "/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        validator = HHReplyUserInfoValidator(response)
        return HHResponse(validator)

    def get_autosearches(self, access_token: str) -> HHResponse:
        url = self.api_base_url + self.autosearches_path
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        validator = HHReplyUserInfoValidator(response)
        return HHResponse(validator)
