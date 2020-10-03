# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from schoology_extractor.api.paginated_result import PaginatedResult
from schoology_extractor.api.request_client import RequestClient

fake_key = 'TEST_KEY'
fake_secret = 'TEST_SECRET'
fake_endpoint_url = 'FAKE_URL'
default_url = 'https://api.schoology.com/v1/'
fake_resource_name = 'resource_name'
fake_api_response = {
    'total': 2,
    'links': {
        'next': 'url'
    }
}


@pytest.fixture
def default_request_client(mocker):
    request_client = RequestClient(fake_key, fake_secret)
    request_client.get = mocker.MagicMock()
    return request_client


@pytest.fixture
def default_paginated_result(default_request_client, mocker):
    return PaginatedResult(
        request_client=default_request_client,
        page_size=20,
        api_response=fake_api_response,
        resource_name=fake_resource_name,
        requested_url=fake_endpoint_url)


class TestPaginatedResult:
    class Test_when_constructing:
        def test_given_no_parameters_shoud_throw_assertException(self):

            # Assert
            with pytest.raises(AssertionError):
                PaginatedResult(None, None, None, None, None)   # type: ignore

        def test_given_wrong_types_in_parameters_shoud_throw_assertException(self):

            # Assert
            with pytest.raises(AssertionError):
                PaginatedResult(0, 1, 'None', [], '')   # type: ignore

        def test_given_correct_params_then_set_correct_properties(self, default_paginated_result):

            # Assert
            assert default_paginated_result.page_size == 20
            assert default_paginated_result._resource_name == fake_resource_name
            assert default_paginated_result.current_page == 1
            assert len(default_paginated_result.current_page_items) == 0
            assert default_paginated_result.requested_url == fake_endpoint_url

    class Test_when_calling_total_pages_property:
        def test_given_total_key_present_in_api_response_then_return_total(self, default_paginated_result):

            # Assert
            assert default_paginated_result.total_pages == 2

        def test_given_total_key_not_present_in_api_response_then_return_zero(self, default_paginated_result):

            # Act
            default_paginated_result._api_response = dict()

            # Assert
            assert default_paginated_result.total_pages == 0

    class Test_when_calling_get_next_page:
        def test_given_links_and_next_keys_present_in_api_response_then_return_paginated_result(self, default_paginated_result):

            # Act
            result = default_paginated_result.get_next_page()

            # Assert
            assert isinstance(result, PaginatedResult)

        def test_given_links_key_present_next_key_not_present_in_api_response_then_return_None(self, default_paginated_result):

            # Arrange
            default_paginated_result._api_response = {'links': {}}

            # Act
            result = default_paginated_result.get_next_page()

            # Assert
            assert result is None

        def test_given_resource_name_key_present_in_api_response_then_bind_current_page_items(self, mocker, default_paginated_result):

            # Arrange
            fake_api_response = {
                fake_resource_name: [{'test': 'test'}]
            }
            default_paginated_result.request_client.get = mocker.MagicMock(return_value=fake_api_response)

            # Act
            default_paginated_result.get_next_page()

            # Assert
            assert len(default_paginated_result.current_page_items) == 1

        def test_given_links_and_next_key_not_present_in_api_response_then_return_None(self, default_paginated_result):

            # Arrange
            default_paginated_result._api_response = dict()

            # Act
            result = default_paginated_result.get_next_page()

            # Assert
            assert result is None
