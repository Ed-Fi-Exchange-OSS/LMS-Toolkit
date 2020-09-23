import pytest
from data_extractor.lib.request_client import RequestClient

pytest.FAKE_KEY = 'TEST_KEY'
pytest.FAKE_SECRET = 'TEST_SECRET'
pytest.FAKE_ENDPOINT_URL = 'FAKE_URL'
pytest.DEFAULT_URL = 'https://api.schoology.com/v1/'


@pytest.fixture
def default_request_client():
    return RequestClient(pytest.FAKE_KEY, pytest.FAKE_SECRET)


class TestRequestClient:
    class TestInitMethod:
        def test_default_base_url_is_set(self):
            request_client = RequestClient(pytest.FAKE_KEY, pytest.FAKE_SECRET)
            assert request_client.base_url == pytest.DEFAULT_URL

        def test_custom_base_url_is_set(self):
            custom_url = "a_custom_url"
            request_client = RequestClient(
                pytest.FAKE_KEY, pytest.FAKE_SECRET, custom_url)
            assert request_client.base_url == custom_url

    class TestRequestHeaderProperty:
        def test_consumer_key_is_set(self, default_request_client):
            assert self._present_in_header(
                default_request_client._request_header,
                header_key="Authorization",
                contained_value=pytest.FAKE_KEY
            )

        def test_oauth_present_in_header(self, default_request_client):
            assert self._present_in_header(
                default_request_client._request_header,
                header_key="Authorization",
                contained_value="OAuth"
            )

        def _present_in_header(self, request_header, header_key, contained_value):
            header_section = request_header[header_key]
            return header_section.find(contained_value) != -1

    class TestGetMethod:
        def test_oauth_get_method_is_called(self, mocker, default_request_client):
            mock_oauth_client = mocker.Mock()
            default_request_client.oauth = mock_oauth_client
            default_request_client.get('')
            mock_oauth_client.get.assert_called_once()

        def test_right_url_is_passed(self, mocker, default_request_client):
            expected_url = pytest.DEFAULT_URL+pytest.FAKE_ENDPOINT_URL

            mock_oauth_client = mocker.Mock()
            default_request_client.oauth = mock_oauth_client
            default_request_client.get(pytest.FAKE_ENDPOINT_URL)
            assert expected_url in mock_oauth_client.get.call_args.kwargs['url']
