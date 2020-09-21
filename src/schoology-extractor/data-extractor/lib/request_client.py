from .authorization import Authorization

DEFAULT_URL = "https://api.schoology.com/v1/"


class RequestClient:
    def __init__(self, SCHOOLOGY_KEY, SCHOOLOGY_SECRET, BASE_URL=DEFAULT_URL):
        self.oauth = Authorization(SCHOOLOGY_KEY, SCHOOLOGY_SECRET)
        self.base_url = BASE_URL
        self._session = None

    @property
    def session(self):
        if self._session is None:
            self._session = self.oauth.get_session()
        return self._session

    def get(self, url):
        r = self.session.get("users")
        return r
