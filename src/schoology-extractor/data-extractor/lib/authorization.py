from rauth import OAuth1Service


class Authorization:
    def __init__(self, consumer_key, consumer_secret):
        API_URL = "https://api.schoology.com/v1/"

        self.oauth = OAuth1Service(
            name="Schoology API",
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            request_token_url=f"{API_URL}oauth/request_token/",
            access_token_url="{API_URL}oauth/access_token/",
            authorize_url="https://api.schoology.com/v1/oauth/authorize/",
            base_url=API_URL,
        )

    def get_token(self):
        return self.oauth.get_request_token()

    def get_session(self):
        request_token, request_token_secret = self.get_token()
        return self.oauth.get_auth_session(
            request_token, request_token_secret, params={"format": "json"}
        )
