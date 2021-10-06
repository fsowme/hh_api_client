from abc import ABC, abstractclassmethod
from json.decoder import JSONDecodeError
from typing import Dict, List
from urllib.parse import urlencode

import requests

from config import FlaskConfig
from requests import Response
from utils.errors import (
    AUTH_ERR,
    TOKEN_ERR,
    GetTokenError,
    HHError,
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


class HHTokenValidator(HHReplyValidator):
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


class HHDataValidator(HHReplyValidator):
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
    def is_valid(self, force=False) -> bool:
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
    vacancies_path = FlaskConfig.VACANCIES_PATH

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
        response = self._request(url, "post", data=data)
        validator = HHTokenValidator(response)
        return HHResponse(validator)

    def update_token(self, refresh_token) -> HHResponse:
        data = {
            "grant_type": self.grant_type_refresh,
            "refresh_token": refresh_token,
        }
        url = "".join([self.base_url, self.token_url_path])
        response = self._request(url, "post", data=data)
        validator = HHTokenValidator(response)
        return HHResponse(validator)

    def get_user_info(self, access_token: str) -> HHResponse:
        url = self.api_base_url + "/me"
        response = self._request(url, "get", token=access_token)
        validator = HHDataValidator(response)
        return HHResponse(validator)

    def get_autosearches(self, token: str, page: int = None) -> HHResponse:
        params = {} if page is None else {"page": page}
        url = self.api_base_url + self.autosearches_path
        response = self._request(url, "get", params=params, token=token)
        validator = HHDataValidator(response)
        return HHResponse(validator)

    def sub_autosearch(
        self, token: str, search_id: str, is_sub: bool = True
    ) -> HHResponse:
        url = self.api_base_url + self.autosearches_path + f"/{search_id}"
        params = {"subscription": is_sub}
        response = self._request(url, "put", params=params, token=token)
        validator = HHDataValidator(response)
        return HHResponse(validator)

    def get_vacancies(
        self, url: str, token: str, page: int = None
    ) -> HHResponse:
        params = {} if page is None else {"page": page}
        response = self._request(url, "get", params=params, token=token)
        validator = HHDataValidator(response)
        return HHResponse(validator)

    @staticmethod
    def _request(
        url: str,
        method: str,
        headers: dict = None,
        params: dict = None,
        data: dict = None,
        token: str = None,
    ) -> Response:
        data = {} if data is None else data
        headers = {} if headers is None else headers
        params = {} if params is None else params
        if token is not None:
            headers.update({"Authorization": f"Bearer {token}"})
        request_method = getattr(requests, method)
        return request_method(url, headers=headers, params=params, data=data)


def get_all_pages(method, *, items: list = None, **options: dict) -> list:
    """Recursively get items from any number of pages from api of hh.ru"""
    items = [] if items is None else items
    response: HHResponse = method(**options)
    if not response.is_valid:
        raise HHError()
    items_on_page = response.cleaned_data
    items.extend(items_on_page["items"])
    pages = items_on_page["pages"]
    next_page = items_on_page["page"] + 1
    if next_page == pages or items_on_page["found"] < 1:
        return items
    options["page"] = next_page
    return get_all_pages(method, items=items, **options)
