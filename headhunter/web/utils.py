class UserToken:
    def __init__(self, access, refresh, expiration_data) -> None:
        self.access_token = access
        self.refresh_token = refresh
        self.expiration_data = expiration_data
