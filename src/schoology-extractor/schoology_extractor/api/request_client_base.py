# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import time
import random

from requests_oauthlib import OAuth1Session


DEFAULT_URL = "https://api.schoology.com/v1/"


class RequestClientBase:
    """
    The RequestClientBase class wraps all the configuration complexity related to authentication and http requests for Schoology API

    Args:
        schoology_key (str): The consumer key given by Schoology
        schoology_secret (str): The consumer secret given by Schoology
        base_url (str, optional): The API base url. Default value: https://api.schoology.com/v1/

    Attributes:
        oauth (OAuth1Session): The two-legged authenticated OAuth1 session
"""

    def __init__(
        self,
        schoology_key: str,
        schoology_secret: str,
        base_url: str = DEFAULT_URL
    ):
        assert schoology_key is not None
        assert schoology_secret is not None
        assert base_url is not None

        self.oauth = OAuth1Session(schoology_key, schoology_secret)
        self.base_url = base_url
        self.consumer_key = schoology_key
        self.consumer_secret = schoology_secret

    @property
    def _request_header(self) -> dict:
        """
        The _request_header property helps to build the Request Header for oauth requests

        Returns:
            dict: Request headers
        """
        auth_header = (
            'OAuth realm="Schoology API",',
            f'oauth_consumer_key="{self.consumer_key}",',
            'oauth_token="",',
            f'oauth_nonce="{"".join( [str(random.randint(0, 9)) for i in range(8)] )}",',
            f'oauth_timestamp="{time.time()}",',
            'oauth_signature_method="PLAINTEXT",',
            'oauth_version="1.0",',
            'oauth_signature="%s%%26%s"' % (self.consumer_secret, "",)
        )

        return {
            "Authorization": ''.join(auth_header),
            "Accept": "application/json",
            "Host": "api.schoology.com",
            "Content-Type": "application/json",
        }

    def _get(self, url: str) -> dict:
        """
        Internal method to create requests and parse responses

        Args:
            url (string): The endpoint that you want to request

        Returns:
            dict: A parsed response from the server
        """
        assert url is not None

        response = self.oauth.get(
            url=self.base_url + url,
            headers=self._request_header,
            auth=self.oauth.auth,
        )
        return response.json()
