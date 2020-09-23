from requests_oauthlib import OAuth1Session
import random
import time

DEFAULT_URL = "https://api.schoology.com/v1/"


class RequestClient:
    """
    The RequestClient class wraps all the configuration complexity related to authentication and http requests for Schoology API

    Args:
        SCHOOLOGY_KEY (str): The consumer key given by Schoology
        SCHOOLOGY_SECRET (str): The consumer secret given by Schoology
        BASE_URL (str, optional): The API base url. Default value: https://api.schoology.com/v1/

    Attributes:
        oauth (OAuth1Session): The two-legged authenticated OAuth1 session
"""

    def __init__(self, SCHOOLOGY_KEY, SCHOOLOGY_SECRET, BASE_URL=DEFAULT_URL):
        self.oauth = OAuth1Session(SCHOOLOGY_KEY, SCHOOLOGY_SECRET)
        self.base_url = BASE_URL
        self.consumer_key = SCHOOLOGY_KEY
        self.consumer_secret = SCHOOLOGY_SECRET

    def get(self, url):
        response = self.oauth.get(
            url=self.base_url + url,
            headers=self._request_header,
            auth=self.oauth.auth,
        )
        return response.json()

    @property
    def _request_header(self):
        auth_header = 'OAuth realm="Schoology API",'
        auth_header += 'oauth_consumer_key="%s",' % self.consumer_key
        auth_header += 'oauth_token="",'
        auth_header += 'oauth_nonce="%s",' % "".join(
            [str(random.randint(0, 9)) for i in range(8)]
        )
        auth_header += 'oauth_timestamp="%d",' % time.time()
        auth_header += 'oauth_signature_method="PLAINTEXT",'
        auth_header += 'oauth_version="1.0",'
        auth_header += 'oauth_signature="%s%%26%s"' % (
            self.consumer_secret,
            "",
        )
        return {
            "Authorization": auth_header,
            "Accept": "application/json",
            "Host": "api.schoology.com",
            "Content-Type": "application/json",
        }
