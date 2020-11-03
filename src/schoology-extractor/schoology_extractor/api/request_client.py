# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass
import os
import time
import random
from typing import List, Union

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
        """The _request_header property builds the Request Header for oauth requests

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
        resource : string
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

    def get_assignments_by_section_ids(
        self, section_ids: Union[List[str], List[int]], page_size: int = DEFAULT_PAGE_SIZE
    ) -> list:
        """
        Parameters
        ----------
        section_ids : list
            A list of section ids.

        Returns
        -------
        dict
            A parsed response from the server

        Note
        --------
        This function will do one or more requests that return paginated results
        and it will handle paging for each request by itself in order to just return
        a simple list of items, instead of a list with PaginatedResults

        """
        assert isinstance(
            section_ids, list
        ), "Argument `section_ids` should be of type `list`."

        assignments: List[object] = []
        for section_id in section_ids:
            params = self._build_query_params_for_first_page(page_size)
            url = f"sections/{section_id}/assignments?{params}"

            assignments_per_section = PaginatedResult(
                self,
                page_size,
                self.get(url),
                RESOURCE_NAMES.ASSIGNMENT,
                self.base_url + url,
            )
            while True:
                current_page_assignments = assignments_per_section.current_page_items

                for assignment in current_page_assignments:
                    assignment["section_id"] = section_id
                assignments = assignments + current_page_assignments

                if assignments_per_section.get_next_page() is None:
                    break

        return assignments

    def get_assignments(
        self, section_id: int, page_size: int = DEFAULT_PAGE_SIZE
    ) -> list:
        """
        Parameters
        ----------
        section_id : int
            A Section Id

        Returns
        -------
        dict
            A parsed response from the server
        """

        assignments: List[object] = []

        params = self._build_query_params_for_first_page(page_size)
        url = f"sections/{section_id}/assignments?{params}"

        assignments_per_section = PaginatedResult(
            self,
            page_size,
            self.get(url),
            "assignment",
            self.base_url + url,
        )
        while True:
            assignments = assignments + assignments_per_section.current_page_items

            if assignments_per_section.get_next_page() is None:
                break

        return assignments

    def get_section_by_course_ids(
        self, course_ids: list, page_size: int = DEFAULT_PAGE_SIZE
    ) -> list:
        """
        Parameters
        ----------
        section_id : str
            The id of the section.

        Returns
        -------
        List[object]
            A parsed response from the server

        Note
        --------
        This function will do one or more requests that return paginated results
        and it will handle paging for each request by itself in order to just return
        a simple list of items, instead of a list with PaginatedResults
        """
        assert isinstance(
            course_ids, list
        ), "Argument `course_ids` should be of type `list`."

        sections: List[object] = []
        for course_id in course_ids:
            url = f"courses/{course_id}/sections"
            sections_per_course = PaginatedResult(
                self, page_size,
                self.get(url),
                RESOURCE_NAMES.SECTION,
                self.base_url + url
            )
            while True:
                sections = sections + sections_per_course.current_page_items
                if sections_per_course.get_next_page() is None:
                    break

        return sections

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

        response = self.get(url)
        return PaginatedResult(
            self,
            page_size,
            response,
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
        assert isinstance(
            page_size, int
        ), "Argument `page_size` should be of type `int`."
        url = f"users?{self._build_query_params_for_first_page(page_size)}"

        return PaginatedResult(
            self, page_size, self.get(url), "user", self.base_url + url
        )

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
        assert isinstance(
            page_size, int
        ), "Argument `section_id` should be of type `int`."

        url = f"gradingperiods?{self._build_query_params_for_first_page(page_size)}"
        response = self.get(url)

        return PaginatedResult(
            self, page_size, response, "gradingperiods", self.base_url + url
        )

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
        response = self.get(url)

        return PaginatedResult(
            self,
            page_size,
            response,
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
        response = self.get(url)

        return PaginatedResult(
            self,
            page_size,
            response,
            RESOURCE_NAMES.ROLE,
            self.base_url + url)

    def get_enrollments(
        self, section_id: int, page_size: int = DEFAULT_PAGE_SIZE
    ) -> list:
        """
        Retrieves enrollment data for a section, with support for paging.

        Parameters
        ----------
        section_id : int
            A Section Id

        Returns
        -------
        list
            A list of all parsed results from the server, for all pages
        """

        enrollments: List[object] = []

        params = self._build_query_params_for_first_page(page_size)
        url = f"sections/{section_id}/enrollments?{params}"

        enrollments_page = PaginatedResult(
            self,
            page_size,
            self.get(url),
            "enrollment",
            self.base_url + url,
        )
        while True:
            enrollments = enrollments + enrollments_page.current_page_items

            if enrollments_page.get_next_page() is None:
                break

        return enrollments

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
        """

        url = f"sections/{section_id}/attendance"

        result = self.get(url)

        return result["date"]

    def get_discussions(
        self, section_id: int
    ) -> list:
        """
        Retrieves disucssions list for a section.

        Parameters
        ----------
        section_id : int
            A Section Id

        Returns
        -------
        list
            A list of all parsed results from the server
        """

        url = f"sections/{section_id}/discussions"

        result = self.get(url)

        return result["discussion"]

    def get_discussion_replies(
        self, section_id: int, discussion_id: Union[int, str]
    ) -> list:
        """
        Retrieves disucssions list for a section.

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
        """

        url = f"sections/{section_id}/discussions/{discussion_id}/comments"

        result = self.get(url)

        return result["comment"]
