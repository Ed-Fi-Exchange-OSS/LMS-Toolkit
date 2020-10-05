# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import time
import random

from requests_oauthlib import OAuth1Session

from .paginated_result import PaginatedResult


DEFAULT_URL = "https://api.schoology.com/v1/"


class RequestClient:
    '''
    The RequestClient class wraps all the configuration complexity related
    to authentication and http requests for Schoology API

    Parameters
    ----------
    schoology_key : str
        The consumer key given by Schoology.
    schoology_secret : str
        The consumer secret given by Schoology.
    base_url : str, optional
        The API base url. Default value: https://api.schoology.com/v1/

    Attributes
    ----------
    oauth : OAuth1Session
        The two-legged authenticated OAuth1 session.
    '''

    def __init__(
        self, schoology_key: str, schoology_secret: str, base_url: str = DEFAULT_URL
    ):
        assert isinstance(schoology_key, str), "Argument `schoology_key` should be of type `str`."
        assert isinstance(schoology_secret, str), "Argument `schoology_secret` should be of type `str`."
        assert isinstance(base_url, str), "Argument `base_url` should be of type `str`."

        self.oauth = OAuth1Session(schoology_key, schoology_secret)
        self.base_url = base_url
        self.consumer_key = schoology_key
        self.consumer_secret = schoology_secret

    @property
    def _request_header(self) -> dict:
        """The _request_header property builds the Request Header for oauth requests

        Returns
        -------
        dict
            Request headers.

        """
        auth_header = (
            'OAuth realm="Schoology API",',
            f'oauth_consumer_key="{self.consumer_key}",',
            'oauth_token="",',
            f'oauth_nonce="{"".join( [str(random.randint(0, 9)) for i in range(8)] )}",',
            f'oauth_timestamp="{time.time()}",',
            'oauth_signature_method="PLAINTEXT",',
            'oauth_version="1.0",',
            'oauth_signature="%s%%26%s"'
            % (
                self.consumer_secret,
                "",
            ),
        )

        return {
            "Authorization": "".join(auth_header),
            "Accept": "application/json",
            "Host": "api.schoology.com",
            "Content-Type": "application/json",
        }

    def get(self, url: str) -> dict:
        """
        Send an HTTP GET request.

        Parameters
        ----------
        url : string
            The endpoint that you want to request.

        Returns
        -------
        dict
            A parsed response from the server

        """
        assert isinstance(url, str), "Argument `url` should be of type `str`."

        response = self.oauth.get(
            url=self.base_url + url,
            headers=self._request_header,
            auth=self.oauth.auth,
        )
        return response.json()

    def get_assignments_by_section_ids(self, section_ids: list) -> list:
        """
        Parameters
        ----------
        section_ids : list
            A list of section ids.

        Returns
        -------
        dict
            A parsed response from the server

        """
        assert isinstance(section_ids, list), "Argument `section_ids` should be of type `list`."

        assignments = []
        for section_id in section_ids:
            url = f"sections/{section_id}/assignments"
            assignments_per_section = PaginatedResult(
                self, 20, self.get(url), "assignment", self.base_url + url
            )
            while True:
                assignments = assignments + assignments_per_section.current_page_items
                if assignments_per_section.get_next_page() is None:
                    break

        return assignments

    def get_section_by_id(self, section_id: str) -> dict:
        """
        Parameters
        ----------
        section_id : str
            The id of the section.

        Returns
        -------
        dict
            A parsed response from the server

        """
        assert isinstance(section_id, str), "Argument `section_id` should be of type `str`."

        response = self.get(f"sections/{section_id}")
        return response

    def get_submissions_by_section_id(
        self, section_id: str, page_size: int = 20
    ) -> PaginatedResult:
        """
        Parameters
        ----------
        section_id : str
            The id of the section.
        page_size : int
            Number of items per page.

        Returns
        -------
        PaginatedResult
            A parsed response from the server

        """
        assert isinstance(section_id, str), "Argument `section_id` should be of type `str`."
        assert isinstance(page_size, int), "Argument `page_size` should be of type `int`."

        url = f"sections/{section_id}/submissions"
        return PaginatedResult(
            self, page_size, self.get(url), "user", self.base_url + url
        )

    def get_users(self, page_size: int = 20) -> PaginatedResult:
        """
        Gets all the users from the Schoology API

        Parameters
        ----------
        section_id : str
            The id of the section.
        page_size : int
            Number of items per page.

        Returns
        -------
        PaginatedResult
            A parsed response from the server

        """
        url = f"users?start=0&limit={page_size}"

        return PaginatedResult(
            self, page_size, self.get(url), "user", self.base_url + url
        )
