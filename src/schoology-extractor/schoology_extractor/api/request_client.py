# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass
import os
import time
import random
from typing import Union

from opnieuw import retry
from requests.exceptions import ConnectionError, HTTPError, Timeout
from requests.packages.urllib3.exceptions import ProtocolError  # type: ignore
from requests_oauthlib import OAuth1Session  # type: ignore

from .paginated_result import PaginatedResult
from schoology_extractor.helpers.constants import RESOURCE_NAMES

DEFAULT_URL = os.environ.get("SCHOOLOGY_BASE_URL") or "https://api.schoology.com/v1/"
DEFAULT_PAGE_SIZE = 20

REQUEST_RETRY_COUNT = int(os.environ.get("REQUEST_RETRY_COUNT") or 4)
REQUEST_RETRY_TIMEOUT_SECONDS = int(
    os.environ.get("REQUEST_RETRY_TIMEOUT_SECONDS") or 60
)


@dataclass
class RequestClient:
    """
    The RequestClient class wraps all the configuration complexity related
    to authentication and http requests for Schoology API

    Parameters
    ----------
    schoology_key : str
        The consumer key given by Schoology.
    schoology_secret : str
        The consumer secret given by Schoology.
    base_url : Optional[str]
        The API base url. Default value: https://api.schoology.com/v1/

    Attributes
    ----------
    oauth : OAuth1Session
        The two-legged authenticated OAuth1 session.
    """
    schoology_key: str
    schoology_secret: str
    base_url: str = DEFAULT_URL

    def __post_init__(self):
        self.oauth = OAuth1Session(self.schoology_key, self.schoology_secret)

    @property
    def _request_header(self) -> dict:
        """
        The _request_header property builds the Request Header for oauth requests

        Returns
        -------
        dict
            Request headers.
        """

        assert isinstance(
            self.schoology_key, str
        ), "Property `schoology_key` should be of type `str`."
        assert isinstance(
            self.schoology_secret, str
        ), "Property `schoology_secret` should be of type `str`."

        auth_header = (
            'OAuth realm="Schoology API",',
            f'oauth_consumer_key="{self.schoology_key}",',
            'oauth_token="",',
            f'oauth_nonce="{"".join( [str(random.randint(0, 9)) for i in range(8)] )}",',
            f'oauth_timestamp="{time.time()}",',
            'oauth_signature_method="PLAINTEXT",',
            'oauth_version="1.0",',
            'oauth_signature="%s%%26%s"'
            % (
                self.schoology_secret,
                "",
            ),
        )

        return {
            "Authorization": "".join(auth_header),
            "Accept": "application/json",
            "Host": "api.schoology.com",
            "Content-Type": "application/json",
        }

    def _build_query_params_for_first_page(self, page_size: int):
        assert isinstance(page_size, int), "Argument `page_size` should be of type `int`."
        return f"start=0&limit={page_size}"

    @retry(
        retry_on_exceptions=(ConnectionError, HTTPError, ProtocolError, Timeout),
        max_calls_total=REQUEST_RETRY_COUNT,
        retry_window_after_first_call_in_seconds=REQUEST_RETRY_TIMEOUT_SECONDS,
    )
    def get(self, resource: str) -> dict:
        """
        Send an HTTP GET request.

        Parameters
        ----------
        resource : str
            The resource endpoint that you want to request.

        Returns
        -------
        dict
            A parsed response from the server
        """

        assert isinstance(resource, str), "Argument `resource` should be of type `str`."
        assert isinstance(
            self.base_url, str
        ), "Property `base_url` should be of type `str`."

        response = self.oauth.get(
            url=self.base_url + resource,
            headers=self._request_header,
            auth=self.oauth.auth,
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"{response.reason} ({response.status_code}): {response.text}"
            )

        return response.json()

    def get_assignments(
        self, section_id: int, page_size: int = DEFAULT_PAGE_SIZE
    ) -> PaginatedResult:
        """
        Parameters
        ----------
        section_id : int
            A Section Id
        page_size : int
            Number of items per page

        Returns
        -------
        PaginatedResult
            A parsed response from the server
        """

        url = f"sections/{section_id}/assignments?{self._build_query_params_for_first_page(page_size)}"

        return PaginatedResult(
            self,
            page_size,
            self.get(url),
            RESOURCE_NAMES.ASSIGNMENT,
            self.base_url + url,
        )

    def get_section_by_course_id(
        self, course_id: Union[int, str], page_size: int = DEFAULT_PAGE_SIZE
    ) -> PaginatedResult:
        """
        Parameters
        ----------
        course_id : Union[int, str]
            The id of the section.
        page_size : int
            Number of items per page

        Returns
        -------
        PaginatedResult
            A parsed response from the server
        """

        url = f"courses/{course_id}/sections"
        return PaginatedResult(
            self, page_size,
            self.get(url),
            RESOURCE_NAMES.SECTION,
            self.base_url + url
        )

    def get_submissions_by_section_id_and_grade_item_id(
        self, section_id: int, grade_item_id: int, page_size: int = DEFAULT_PAGE_SIZE
    ) -> PaginatedResult:
        """
        Retrieves submissions for assignments or discussions in a section.

        Parameters
        ----------
        section_id : int
            The id of the section
        grade_item_id : int
            Grade Item Id, which can either be an Assignment ID or a Discussion ID
        page_size : int
            Number of items per page

        Returns
        -------
        PaginatedResult
            A parsed response from the server
        """

        query_params = self._build_query_params_for_first_page(page_size)
        url = f"sections/{section_id}/submissions/{grade_item_id}?{query_params}"

        return PaginatedResult(
            self,
            page_size,
            self.get(url),
            RESOURCE_NAMES.REVISION,
            self.base_url + url
        )

    def get_users(self, page_size: int = DEFAULT_PAGE_SIZE) -> PaginatedResult:
        """
        Gets all the users from the Schoology API

        Parameters
        ----------
        page_size : int
            Number of items per page.

        Returns
        -------
        PaginatedResult
            A parsed response from the server
        """

        url = f"users?{self._build_query_params_for_first_page(page_size)}"

        return PaginatedResult(self, page_size, self.get(url), "user", self.base_url + url)

    def get_grading_periods(
        self, page_size: int = DEFAULT_PAGE_SIZE
    ) -> PaginatedResult:
        """
        Gets all the grading periods from the Schoology API

        Parameters
        ----------
        page_size : int
            Number of items per page.

        Returns
        -------
        PaginatedResult
            A parsed response from the server
        """

        url = f"gradingperiods?{self._build_query_params_for_first_page(page_size)}"

        return PaginatedResult(self, page_size, self.get(url), "gradingperiods", self.base_url + url)

    def get_courses(self, page_size: int = DEFAULT_PAGE_SIZE) -> PaginatedResult:
        """
        Gets all the courses from the Schoology API

        Parameters
        ----------
        page_size : int
            Number of items per page.

        Returns
        -------
        PaginatedResult
            A parsed response from the server

        """

        url = f"courses?{self._build_query_params_for_first_page(page_size)}"

        return PaginatedResult(
            self,
            page_size,
            self.get(url),
            RESOURCE_NAMES.COURSE,
            self.base_url + url)

    def get_roles(self, page_size: int = DEFAULT_PAGE_SIZE) -> PaginatedResult:
        """
        Gets all the roles from the Schoology API

        Parameters
        ----------
        page_size : int
            Number of items per page.

        Returns
        -------
        PaginatedResult
            A parsed response from the server

        """

        url = f"roles?{self._build_query_params_for_first_page(page_size)}"

        return PaginatedResult(
            self,
            page_size,
            self.get(url),
            RESOURCE_NAMES.ROLE,
            self.base_url + url)

    def get_enrollments(
        self, section_id: int, page_size: int = DEFAULT_PAGE_SIZE
    ) -> PaginatedResult:
        """
        Retrieves enrollment data for a section, with support for paging.

        Parameters
        ----------
        section_id : int
            A Section Id
        page_size : int
            Number of items per page.

        Returns
        -------
        PaginatedResult
            A parsed response from the server
        """

        params = self._build_query_params_for_first_page(page_size)
        url = f"sections/{section_id}/enrollments?{params}"

        return PaginatedResult(
            self,
            page_size,
            self.get(url),
            RESOURCE_NAMES.ENROLLMENT,
            self.base_url + url,
        )

    def get_attendance(
        self, section_id: int
    ) -> list:
        """
        Retrieves attendance event data for a section. Note: attendance does
        not support paging.

        Parameters
        ----------
        section_id : int
            A Section Id

        Returns
        -------
        list
            A list of all parsed results from the server

        Notes
        -----
        The endpoint for this resource doesn't support pagination.
        that's why it returns a list.
        """

        url = f"sections/{section_id}/attendance"

        result = self.get(url)

        return result["date"]

    def get_discussions(
        self, section_id: int
    ) -> list:
        """
        Retrieves discussions list for a section.

        Parameters
        ----------
        section_id : int
            A Section Id

        Returns
        -------
        list
            A list of all parsed results from the server

        Notes
        -----
        The endpoint for this resource doesn't support pagination.
        that's why it returns a list.
        """

        result = self.get(f"sections/{section_id}/discussions")
        return result["discussion"]

    def get_discussion_replies(
        self, section_id: int, discussion_id: Union[int, str]
    ) -> list:
        """
        Retrieves replies list for a discussion.

        Parameters
        ----------
        section_id : int
            A Section Id
        discussion_id : Union[int, str]
            The Id of the discussion

        Returns
        -------
        list
            A list of all parsed results from the server

        Notes
        -----
        The endpoint for this resource doesn't support pagination.
        that's why it returns a list.
        """

        result = self.get(f"sections/{section_id}/discussions/{discussion_id}/comments")
        return result["comment"]
