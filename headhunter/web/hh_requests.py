import requests

from .config import Config
from .utils import UserToken


class HHRequester:
    base_url = Config.HH_BASE_URL

    def get_user_info(self, token: UserToken) -> dict:
        url = self.base_url + "/me"
        headers = {"Authorization": f"Bearer {token.access_token}"}
        response = requests.get(url, headers=headers)
        # TODO: validate status instead raise_for_status
        response.raise_for_status()
        response_data = response.json()
        return response_data
