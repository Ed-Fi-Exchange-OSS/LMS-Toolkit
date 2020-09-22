from .request_client import RequestClient


class Users:
    def __init__(self, SCHOOLOGY_KEY, SCHOOLOGY_SECRET):
        self.request_client = RequestClient(SCHOOLOGY_KEY, SCHOOLOGY_SECRET)

    def get_all(self):
        return self.request_client.get("users")
