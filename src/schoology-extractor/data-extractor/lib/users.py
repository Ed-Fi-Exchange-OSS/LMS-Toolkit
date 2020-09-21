from .api_base import ApiBase


class Users(ApiBase):
    def __init__(self, SCHOOLOGY_KEY, SCHOOLOGY_SECRET):
        super().__init__(SCHOOLOGY_KEY, SCHOOLOGY_SECRET)

    def get_all(self):
        return self.request_client.get("users")
