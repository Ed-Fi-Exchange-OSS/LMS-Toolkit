# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from unittest.mock import Mock
import pytest

from edfi_schoology_extractor.api.paginated_result import PaginatedResult
from edfi_schoology_extractor.api.request_client import RequestClient

FAKE_KEY = "TEST_KEY"
FAKE_SECRET = "TEST_SECRET"
FAKE_ENDPOINT_URL = "FAKE_URL"
DEFAULT_URL = "https://api.schoology.com/v1/"
FAKE_RESOURCE_NAME = "resource_name"
FAKE_API_RESPONSE = {"total": 2, "links": {"next": "url"}}


@pytest.fixture
def default_request_client(mocker):
    request_client = RequestClient(FAKE_KEY, FAKE_SECRET)
    request_client.get = mocker.MagicMock()
    return request_client


@pytest.fixture
def default_paginated_result(default_request_client, mocker):
    return PaginatedResult(
        request_client=default_request_client,
        page_size=20,
        api_response=FAKE_API_RESPONSE,
        resource_name=FAKE_RESOURCE_NAME,
        requested_url=FAKE_ENDPOINT_URL,
    )


class TestPaginatedResult:
    class Test_when_constructing:
        def test_given_wrong_type_as_request_client_then_throw_assertException(self):

            # Assert
            with pytest.raises(AssertionError):
                PaginatedResult(request_client=0, page_size=1, api_response="None", resource_name=[], requested_url="test")  # type: ignore

        def test_given_wrong_type_as_page_size_then_throw_assertException(
            self, default_request_client
        ):

            # Assert
            with pytest.raises(AssertionError):
                PaginatedResult(request_client=default_request_client, page_size=[], api_response="None", resource_name=[], requested_url="test")  # type: ignore

        def test_given_wrong_type_as_api_response_then_throw_assertException(self):

            # Assert
            with pytest.raises(AssertionError):
                PaginatedResult(request_client=default_request_client, page_size=20, api_response="None", resource_name=[], requested_url="test")  # type: ignore

        def test_given_wrong_type_as_resource_name_then_throw_assertException(self):

            # Assert
            with pytest.raises(AssertionError):
                PaginatedResult(request_client=0, page_size=1, api_response=[], resource_name=[], requested_url="test")  # type: ignore

        def test_given_wrong_type_as_requested_url_then_throw_assertException(self):

            # Assert
            with pytest.raises(AssertionError):
                PaginatedResult(request_client=0, page_size=1, api_response=[], resource_name="test", requested_url=20)  # type: ignore

        def test_given_correct_params_then_set_correct_properties(
            self, default_paginated_result
        ):

            # Assert
            assert default_paginated_result.page_size == 20
            assert default_paginated_result._resource_name == FAKE_RESOURCE_NAME
            assert default_paginated_result.current_page == 1
            assert len(default_paginated_result.current_page_items) == 0
            assert default_paginated_result.requested_url == FAKE_ENDPOINT_URL

    class Test_when_calling_total_pages_property:
        def test_given_total_key_present_in_api_response_then_return_total(
            self, default_paginated_result
        ):

            # Assert
            assert default_paginated_result.total_pages == 2

        def test_given_total_key_not_present_in_api_response_then_return_zero(
            self, default_paginated_result
        ):

            # Act
            default_paginated_result._api_response = dict()

            # Assert
            assert default_paginated_result.total_pages == 0

    class Test_when_calling_get_next_page:
        def test_given_links_and_next_keys_present_in_api_response_then_return_paginated_result(
            self, default_paginated_result
        ):

            # Act
            result = default_paginated_result.get_next_page()

            # Assert
            assert isinstance(result, PaginatedResult)

        def test_given_links_key_present_next_key_not_present_in_api_response_then_return_None(
            self, default_paginated_result
        ):

            # Arrange
            default_paginated_result._api_response = {"links": {}}

            # Act
            result = default_paginated_result.get_next_page()

            # Assert
            assert result is None

        def test_given_resource_name_key_present_in_api_response_then_bind_current_page_items(
            self, mocker, default_paginated_result
        ):

            # Arrange
            FAKE_API_RESPONSE = {FAKE_RESOURCE_NAME: [{"test": "test"}]}
            default_paginated_result.request_client.get = mocker.MagicMock(
                return_value=FAKE_API_RESPONSE
            )

            # Act
            default_paginated_result.get_next_page()

            # Assert
            assert len(default_paginated_result.current_page_items) == 1

        def test_given_links_and_next_key_not_present_in_api_response_then_return_None(
            self, default_paginated_result
        ):

            # Arrange
            default_paginated_result._api_response = dict()

            # Act
            result = default_paginated_result.get_next_page()

            # Assert
            assert result is None


def describe_when_getting_all_pages():
    @pytest.fixture
    def paginated_result():
        request_client = Mock(spec=RequestClient)
        page_size = 22

        users = {
            "user": [{"uid": 1234, "role_id": 321}],
            "total": 1,
            "links": {"self": "ignore"},
        }
        paginated_result = PaginatedResult(
            request_client, page_size, users, "user", "ignore me"
        )
        paginated_result.get_next_page = Mock(return_value=None)

        # act
        paginated_result.get_all_pages()
        return paginated_result

    def it_should_call_get_next_page(paginated_result):
        assert paginated_result.get_next_page.called

    @pytest.fixture
    def result():
        request_client = Mock(spec=RequestClient)
        page_size = 22

        users = {
            "user": [{"uid": 1234, "role_id": 321}],
            "total": 1,
            "links": {"self": "ignore"},
        }
        paginated_result = PaginatedResult(
            request_client, page_size, users, "user", "ignore me"
        )

        # act
        return paginated_result.get_all_pages()

    def it_should_return_all_available_items(result: list):
        assert len(result) == 1
