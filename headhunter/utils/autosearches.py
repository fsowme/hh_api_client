from web import hh_requester


class Autosearch:
    def __init__(self, id: int, name: str, all_url: str, new_url: str) -> None:
        self.id = id
        self.name = name
        self.all_url = all_url
        self.new_url = new_url

    def get_new(self, access_token):

        hh_requester.get_vacancies(self.new_url, access_token)
