# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from __future__ import annotations
from typing import Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .request_client import RequestClient


class PaginatedResult:
    """
    The PaginatedResult class is bound with information from the response of the Schoology
    api, specifically when it returns a list of items that could be paginated.

    Args:
        request_client (RequestClient): The request client.
        page_size (int): The number of items per page.
        api_response (dict): The original response as a dictionary.
        resource_name (str): The name used by the Schoology API for the current resource.
        requested_url(str): The URL where you got the response from.
        current_page(int, optional=1): The page that you have requested

    Attributes:
        request_client (RequestClient): The request client.
        page_size (int): The number of items per page.
        requested_url(str): The URL where you got the response from.
        current_page_items(list): The list of items for the current page.
        _api_response (dict): The original response as a dictionary.
        _resource_name (str): The name used by the Schoology API for the current resource.

    """

    def __init__(
        self,
        request_client: "RequestClient",
        page_size: int,
        api_response: dict,
        resource_name: str,
        requested_url: str,
        current_page: int = 1,
    ):
        assert hasattr(request_client, "get")
        assert isinstance(page_size, int)
        assert isinstance(api_response, dict)
        assert isinstance(resource_name, str)
        assert isinstance(requested_url, str)
        assert isinstance(current_page, int)

        self.request_client = request_client
        self.page_size = page_size
        self.requested_url = requested_url
        self.current_page = current_page

        if resource_name in api_response:
            self.current_page_items = api_response[resource_name]
        else:
            self.current_page_items = []

        self._api_response = api_response
        self._resource_name = resource_name

    @property
    def total_pages(self) -> int:
        """
        Number of pages for the current resource with the current page size.

        Returns:
            int: Request headers
        """
        if "total" not in self._api_response:
            return 0
        return int(self._api_response["total"])

    def get_next_page(self) -> Optional[PaginatedResult]:
        """
        Send an HTTP GET request for the next page.

        Returns:
            Optional[PaginatedResult]: If there are more pages.
        """
        if "links" not in self._api_response:
            return None

        if "next" not in self._api_response["links"]:
            return None

        next_url = self._api_response["links"]["next"]
        next_url = next_url.replace(self.request_client.base_url, "")

        response = self.request_client.get(next_url)

        self.requested_url = next_url
        self.current_page = self.current_page + 1
        self._api_response = response
        if self._resource_name in self._api_response:
            self.current_page_items = self._api_response[self._resource_name]
        else:
            self.current_page_items = []

        return self
