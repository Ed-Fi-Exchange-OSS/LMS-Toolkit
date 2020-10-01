# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from schoology_extractor.api.request_client_base import RequestClientBase

fake_key = 'TEST_KEY'
fake_secret = 'TEST_SECRET'
fake_endpoint_url = 'FAKE_URL'
default_url = 'https://api.schoology.com/v1/'


@pytest.fixture
def default_request_client():
    return RequestClientBase(fake_key, fake_secret)


class TestRequestClientBase:

    class Test_when_constructing:
        def test_given_not_passing_in_a_url_then_use_the_default_url(self):
            request_client = RequestClientBase(fake_key, fake_secret)
            assert request_client.base_url == default_url

        def test_given_custom_url_then_use_it_for_the_base_url(self):

            # Arrange
            custom_url = "a_custom_url"

            # Act
            request_client = RequestClientBase(
                fake_key, fake_secret, custom_url)

            # Assert
            assert request_client.base_url == custom_url

        def test_given_None_as_parameters_then_assert_should_fail(self):
            # Assert
            with pytest.raises(AssertionError):
                RequestClientBase(None, None)

    class Test_when_building_request_header:
        def test_then_consumer_key_is_present(self, default_request_client):
            assert self._present_in_header(
                default_request_client._request_header,
                header_key="Authorization",
                contained_value=fake_key
            )

        def test_then_oauth_word_is_present(self, default_request_client):
            assert self._present_in_header(
                default_request_client._request_header,
                header_key="Authorization",
                contained_value="OAuth"
            )

        def _present_in_header(self, request_header, header_key, contained_value):
            header_section = request_header[header_key]
            return header_section.find(contained_value) != -1

    class Test_when_get_method_is_called:
        def test_given_no_parameters_passed_then_throw_assert_exception(self, default_request_client):
            with pytest.raises(AssertionError):
                default_request_client.get(None)

        def test_then_oauth_base_get_method_is_called(self, mocker, default_request_client):

            # Arrange
            mock_oauth_client = mocker.Mock()
            default_request_client.oauth = mock_oauth_client

            # Act
            default_request_client.get(fake_endpoint_url)

            # Assert
            mock_oauth_client.get.assert_called_once()

        def test_then_right_url_is_passed(self, mocker, default_request_client):

            # Arrange
            expected_url = default_url+fake_endpoint_url
            mock_oauth_client = mocker.Mock()
            default_request_client.oauth = mock_oauth_client

            # Act
            default_request_client.get(fake_endpoint_url)

            # Assert
            request_url = mock_oauth_client.get.call_args.kwargs['url']
            assert expected_url in request_url
