# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass
import logging
import os
import time
import random
from typing import Any, Dict, List, Union
from http import HTTPStatus
import socket

from opnieuw import retry
from requests import Response
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout
from requests.packages.urllib3.exceptions import ProtocolError  # type: ignore
from requests_oauthlib import OAuth1Session  # type: ignore

from .paginated_result import PaginatedResult
from edfi_schoology_extractor.helpers.constants import RESOURCE_NAMES

DEFAULT_URL = os.environ.get("SCHOOLOGY_BASE_URL") or "https://api.schoology.com/v1/"
DEFAULT_PAGE_SIZE = 20

REQUEST_RETRY_COUNT = int(os.environ.get("REQUEST_RETRY_COUNT") or 4)
REQUEST_RETRY_TIMEOUT_SECONDS = int(
    os.environ.get("REQUEST_RETRY_TIMEOUT_SECONDS") or 60
)

logger = logging.getLogger(__name__)


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

    def __post_init__(self) -> None:
        self.oauth = OAuth1Session(self.schoology_key, self.schoology_secret)

    @property
    def _request_header(self) -> Dict[str, str]:
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

    def _build_query_params_for_first_page(self, page_size: int) -> str:
        return f"start=0&limit={page_size}"

    def _check_for_rate_limiting(self, response: Response, http_method: str, url: str) -> None:
        """
        Check for a rate limit response. If it has occurred, log and
        raise an exception to be caught to trigger a retry.

        Parameters
        ----------
        response: Response
            The HTTP response to check
        http_method: str
            A human-readable string describing the http method, used for logging
        url: str
            The url of the request, used for logging

        Raises
        -------
        HTTPError
            If the response indicates a rate limit
        """
        if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            logger.warn(
                "Hit API rate limiting on %s to %s, will retry with backoff",
                http_method,
                url,
            )
            raise HTTPError(
                f"{response.reason} ({response.status_code}): {response.text}"
            )

    def _check_for_success(self, response: Response, success_status: HTTPStatus) -> None:
        """
        Check a response for success. If unsuccessful, log and
        raise an exception.

        Parameters
        ----------
        response: Response
            The HTTP response to check
        success_status: HTTPStatus
            The HTTP status that indicates success

        Raises
        -------
        RuntimeError
            If the response indicates failure
        """
        if response.status_code != success_status:
            raise RuntimeError(
                f"{response.reason} ({response.status_code}): {response.text}"
            )

    def _check_response(
        self, response: Response, success_status: HTTPStatus, http_method: str, url: str
    ) -> None:
        """
        Check a response for rate limiting and success

        Parameters
        ----------
        response: Response
            The HTTP response to check
        success_status: HTTPStatus
            The HTTP status that indicates success
        http_method: str
            A human-readable string describing the http method, used for logging
        url: str
            The url of the request, used for logging

        Raises
        -------
        HTTPError
            If the response indicates a rate limit, to trigger a retry
        RuntimeError
            If the response indicates failure
        """
        self._check_for_rate_limiting(response, http_method, url)
        self._check_for_success(response, success_status)

    @retry(
        retry_on_exceptions=(
            IOError,
            ConnectionError,
            RequestException,
            HTTPError,
            ProtocolError,
            Timeout,
            RuntimeError,
            socket.timeout,
            socket.error
        ),
        max_calls_total=REQUEST_RETRY_COUNT,
        retry_window_after_first_call_in_seconds=REQUEST_RETRY_TIMEOUT_SECONDS,
    )
    def get(self, resource: str) -> Dict[str, Any]:
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

        Raises
        -------
        RuntimeError
            If the GET operation is unsuccessful
        """
        assert isinstance(
            self.base_url, str
        ), "Property `base_url` should be of type `str`."

        url = self.base_url + resource
        response = self.oauth.get(
            url=url,
            headers=self._request_header,
            auth=self.oauth.auth,
        )

        self._check_response(
            response=response, success_status=HTTPStatus.OK, http_method="GET", url=url
        )
        return response.json()  # type: ignore

    @retry(
        retry_on_exceptions=(
            IOError,
            ConnectionError,
            RequestException,
            HTTPError,
            ProtocolError,
            Timeout,
            RuntimeError,
            socket.timeout,
            socket.error
        ),
        max_calls_total=REQUEST_RETRY_COUNT,
        retry_window_after_first_call_in_seconds=REQUEST_RETRY_TIMEOUT_SECONDS,
    )
    def post(self, resource: str, json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a HTTP POST request.

        Parameters
        ----------
        resource : str
            The resource endpoint that you want to POST to.
        json : str
            The body of the POST as a JSON-like dict.

        Returns
        -------
        dict
            A parsed response from the server

        Raises
        -------
        RuntimeError
            If the POST operation is unsuccessful.
        """
        url = f"{self.base_url}{resource}"
        response = self.oauth.post(
            url=url,
            headers=self._request_header,
            auth=self.oauth.auth,
            json=json,
        )

        self._check_response(
            response=response,
            success_status=HTTPStatus.CREATED,
            http_method="POST",
            url=url,
        )

        return response.json()  # type: ignore

    @retry(
        retry_on_exceptions=(
            IOError,
            ConnectionError,
            RequestException,
            HTTPError,
            ProtocolError,
            Timeout,
            RuntimeError,
            socket.timeout,
            socket.error
        ),
        max_calls_total=REQUEST_RETRY_COUNT,
        retry_window_after_first_call_in_seconds=REQUEST_RETRY_TIMEOUT_SECONDS,
    )
    def bulk_post(self, resource: str, json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a bulk HTTP POST request.

        Parameters
        ----------
        resource : str
            The resource endpoint that you want to POST to.
        json : str
            The body of the POST as a JSON-like dict.  This must be in the
            bulk form specified by the API. Note that 50 is the maximum
            number permitted by the API for a bulk operation.

        Returns
        -------
        dict
            A parsed response from the server

        Raises
        -------
        RuntimeError
            If the bulk POST operation as a whole is unsuccessful. Does not
            attempt to check status codes for each individual operation.
        """
        url = f"{self.base_url}{resource}"
        response = self.oauth.post(
            url=url,
            headers=self._request_header,
            auth=self.oauth.auth,
            json=json,
        )

        self._check_response(
            response=response,
            success_status=HTTPStatus.MULTI_STATUS,
            http_method="bulk POST",
            url=url,
        )

        return response.json()  # type: ignore

    @retry(
        retry_on_exceptions=(
            IOError,
            ConnectionError,
            RequestException,
            HTTPError,
            ProtocolError,
            Timeout,
            RuntimeError,
            socket.timeout,
            socket.error
        ),
        max_calls_total=REQUEST_RETRY_COUNT,
        retry_window_after_first_call_in_seconds=REQUEST_RETRY_TIMEOUT_SECONDS,
    )
    def bulk_delete(self, resource: str, parameters: str) -> Dict[str, Any]:
        """
        Send a bulk HTTP DELETE request.

        Parameters
        ----------
        resource : str
            The resource endpoint that you want to DELETE to.
        parameters : str
            A URL parameter string required for the bulk delete operation,
            typically a list of ids of the resources to delete

        Returns
        -------
        dict
            A parsed response from the server

        Raises
        -------
        RuntimeError
            If the bulk DELETE operation as a whole is unsuccessful.  Does not
            attempt to check status codes for each individual operation.
        """
        url = f"{self.base_url}{resource}?{parameters}"
        response = self.oauth.delete(
            url=url,
            headers=self._request_header,
            auth=self.oauth.auth,
        )

        self._check_response(
            response=response,
            success_status=HTTPStatus.MULTI_STATUS,
            http_method="bulk DELETE",
            url=url,
        )

        return response.json()  # type: ignore

    @retry(
        retry_on_exceptions=(
            IOError,
            ConnectionError,
            RequestException,
            HTTPError,
            ProtocolError,
            Timeout,
            RuntimeError,
            socket.timeout,
            socket.error
        ),
        max_calls_total=REQUEST_RETRY_COUNT,
        retry_window_after_first_call_in_seconds=REQUEST_RETRY_TIMEOUT_SECONDS,
    )
    def delete(self, resource: str, id: str) -> None:
        """
        Send a HTTP DELETE request.

        Parameters
        ----------
        resource : str
            The resource endpoint that you want to DELETE to.
        id : str
            A Schoology generated id of the specific resource to delete.

        Returns
        -------
        dict
            A parsed response from the server

        Raises
        -------
        RuntimeError
            If the bulk DELETE operation as a whole is unsuccessful.  Does not
            attempt to check status codes for each individual operation.
        """
        url = f"{self.base_url}{resource}/{id}"
        response = self.oauth.delete(
            url=url,
            headers=self._request_header,
            auth=self.oauth.auth,
        )

        self._check_response(
            response=response,
            success_status=HTTPStatus.NO_CONTENT,
            http_method="DELETE",
            url=url,
        )

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
            self, page_size, self.get(url), RESOURCE_NAMES.SECTION, self.base_url + url
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
            self, page_size, self.get(url), RESOURCE_NAMES.REVISION, self.base_url + url
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

        return PaginatedResult(
            self, page_size, self.get(url), "user", self.base_url + url
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

        return PaginatedResult(
            self, page_size, self.get(url), RESOURCE_NAMES.COURSE, self.base_url + url
        )

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
            self, page_size, self.get(url), RESOURCE_NAMES.ROLE, self.base_url + url
        )

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

    def get_attendance(self, section_id: int) -> List[Dict[str, Any]]:
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

        return result["date"]  # type: ignore

    def get_discussions(self, section_id: int) -> List[Dict[str, Any]]:
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
        return result["discussion"]  # type: ignore

    def get_discussion_replies(
        self, section_id: int, discussion_id: Union[int, str]
    ) -> List[Dict[str, Any]]:
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
        return result["comment"]  # type: ignore

    def get_section_updates(
        self, section_id: int, page_size: int = DEFAULT_PAGE_SIZE
    ) -> PaginatedResult:
        """
        Retrieves updates for a section.

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
        url = f"sections/{section_id}/updates"
        return PaginatedResult(
            self,
            page_size,
            self.get(url),
            RESOURCE_NAMES.SECTION_UPDATE_API,
            self.base_url + url,
        )

    def get_section_update_replies(
        self, section_id: int, update_id: int, page_size: int = DEFAULT_PAGE_SIZE
    ) -> PaginatedResult:
        """
        Retrieves replies for a section update.

        Parameters
        ----------
        section_id : int
            A Section Id
        update_id : int
            An Update Id
        page_size : int
            Number of items per page

        Returns
        -------
        PaginatedResult
            A parsed response from the server
        """
        url = f"sections/{section_id}/updates/{update_id}/comments"
        return PaginatedResult(
            self,
            page_size,
            self.get(url),
            RESOURCE_NAMES.SECTION_UPDATE_COMMENT,
            self.base_url + url,
        )
