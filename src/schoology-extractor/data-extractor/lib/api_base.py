from .request_client import RequestClient


class ApiBase:
    def __init__(self, SCHOOLOGY_KEY, SCHOOLOGY_SECRET):
        self.request_client = RequestClient(SCHOOLOGY_KEY, SCHOOLOGY_SECRET)
