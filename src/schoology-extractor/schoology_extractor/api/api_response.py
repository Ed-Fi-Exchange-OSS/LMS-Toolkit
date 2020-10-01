from __future__ import annotations
from requests import Response

from .request_client_base import RequestClientBase


class ApiResponse():

    def __init__(
        self,
        request_client_base: RequestClientBase,
        page_size: int,
        api_response: Response,
        resource_name: str,
        requested_url: str,
        current_page: int = 1
    ):
        assert request_client_base is not None
        assert page_size is not None
        assert api_response is not None
        assert resource_name is not None
        assert requested_url is not None
        assert current_page is not None

        self.request_client = request_client_base
        self.page_size = page_size
        self.requested_url = requested_url
        self.current_page = current_page

        self._api_response = api_response
        self._resource_name = resource_name

        if(resource_name in api_response):
            self.current_page_items = api_response[resource_name]
        else:
            self.current_page_items = []

    @property
    def total_pages(self) -> int:
        if("total" in self._api_response):
            return 0
        return int(self._api_response["total"])

    @property
    def _next_page_url(self) -> str:
        if("link" in self._api_response):
            return 0
        return int(self._api_response["total"])

    def get_next_page(self) -> ApiResponse:
        if("links" not in self._api_response):
            return None
        elif("next" not in self._api_response["links"]):
            return None

        next_url = self._api_response["links"]["next"]
        next_url = next_url.replace(self.request_client.base_url, "")

        response = self.request_client._get(next_url)

        self.requested_url = next_url
        self.current_page = self.current_page + 1
        self._api_response = response
        if(self._resource_name in self._api_response):
            self.current_page_items = self._api_response[self._resource_name]
        else:
            self.current_page_items = []

        return self
