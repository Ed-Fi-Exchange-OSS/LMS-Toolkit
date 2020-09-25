import pytest

from data_extractor.lib.request_client import RequestClient

pytest.fake_key = 'TEST_KEY'
pytest.fake_secret = 'TEST_SECRET'
pytest.fake_endpoint_url = 'FAKE_URL'
pytest.default_url = 'https://api.schoology.com/v1/'


@pytest.fixture
def default_request_client():
    return RequestClient(pytest.fake_key, pytest.fake_secret)


class TestRequestClient:


    class Test_when_constructing:
        def test_given_not_passing_in_a_url_then_use_the_default_url(self):
            request_client = RequestClient(pytest.fake_key, pytest.fake_secret)
            assert request_client.base_url == pytest.default_url

        def test_given_custom_url_then_use_it_for_the_base_url(self):

            # Arrange
            custom_url = "a_custom_url"

            # Act
            request_client = RequestClient(
                pytest.fake_key, pytest.fake_secret, custom_url)

            # Assert
            assert request_client.base_url == custom_url


    class Test_when_building_request_header:
        def test_then_consumer_key_is_present(self, default_request_client):
            assert self._present_in_header(
                default_request_client._request_header,
                header_key="Authorization",
                contained_value=pytest.fake_key
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
                default_request_client._get(None)

        def test_then_oauth_base_get_method_is_called(self, mocker, default_request_client):

            # Arrange
            mock_oauth_client = mocker.Mock()
            default_request_client.oauth = mock_oauth_client

            # Act
            default_request_client._get(pytest.fake_endpoint_url)

            # Assert
            mock_oauth_client.get.assert_called_once()

        def test_then_right_url_is_passed(self, mocker, default_request_client):

            # Arrange
            expected_url = pytest.default_url+pytest.fake_endpoint_url
            mock_oauth_client = mocker.Mock()
            default_request_client.oauth = mock_oauth_client

            # Act
            default_request_client._get(pytest.fake_endpoint_url)

            # Assert
            request_url = mock_oauth_client.get.call_args.kwargs['url']
            assert expected_url in request_url


    class Test_when_get_assignments_by_section_ids_method_is_called:
        def test_given_no_parameters_passed_then_throw_assert_exception(self, default_request_client):
            with pytest.raises(AssertionError):
                default_request_client.get_assignments_by_section_ids(None)

        def test_given_an_array_of_ids_then_make_a_call_per_item_in_array(self, default_request_client, mocker):

            # Arrange
            array_of_ids = ['1', '2', '3', '4']
            mock_oauth_client = mocker.MagicMock(return_value= { "assignment": "test_assignment" })
            default_request_client.oauth = mock_oauth_client

            # Act
            default_request_client.get_assignments_by_section_ids(array_of_ids)

            # Assert
            assert mock_oauth_client.get.call_count == len(array_of_ids)

        def test_given_an_array_as_response_per_request_then_return_information(self, default_request_client, mocker):

            # Arrange
            array_of_ids = ['1', '2', '3', '4']
            fake_list_of_assignments = [{"assignment": "test"}, {"assignment": "test"}, {"assignment": "test"}]
            mock_oauth_client = mocker.Mock()
            response_json = mocker.MagicMock()
            response_json.json = mocker.MagicMock(return_value={"assignment": fake_list_of_assignments})
            mock_oauth_client.get = mocker.MagicMock(return_value=response_json)
            default_request_client.oauth = mock_oauth_client

            # Act
            response = default_request_client.get_assignments_by_section_ids(array_of_ids)

            # Assert
            assert len(response) == (len(array_of_ids) * len(fake_list_of_assignments))

        def test_given_an_empty_array_of_ids_then_make_a_call_per_item_in_array(self, default_request_client, mocker):

            # Arrange
            array_of_ids = []
            mock_oauth_client = mocker.MagicMock(return_value= { "assignment": "test_assignment" })
            default_request_client.oauth = mock_oauth_client

            # Act
            default_request_client.get_assignments_by_section_ids(array_of_ids)

            # Assert
            assert mock_oauth_client.get.call_count == len(array_of_ids)

        def test_given_an_empty_array_of_ids_then_returns_empty_array(self, default_request_client, mocker):

            # Arrange
            array_of_ids = ['1', '2', '3', '4']
            mock_oauth_client = mocker.MagicMock(return_value= {})
            default_request_client.oauth = mock_oauth_client

            # Act
            response = default_request_client.get_assignments_by_section_ids(array_of_ids)

            # Assert
            assert (isinstance(response, list) and len(response) == 0)


    class Test_when_get_section_by_id_method_is_called:
        def test_given_no_parameters_passed_then_throw_assert_exception(self, default_request_client):
            with pytest.raises(AssertionError):
                default_request_client.get_section_by_id(None)

        def test_given_a_parameter_is_passed_then_shoud_make_the_get_call(self, default_request_client, mocker):

            # Arrange
            mock_oauth_client = mocker.MagicMock(return_value= {})
            default_request_client.oauth = mock_oauth_client

            # Act
            default_request_client.get_section_by_id('1')

            # Assert
            assert mock_oauth_client.get.call_count == 1


    class Test_when_get_submissions_by_section_id_method_is_called:
        def test_given_no_parameters_passed_then_throw_assert_exception(self, default_request_client):
            with pytest.raises(AssertionError):
                default_request_client.get_submissions_by_section_id(None)

        def test_given_a_parameter_is_passed_then_shoud_make_the_get_call(self, default_request_client, mocker):

            # Arrange
            mock_oauth_client = mocker.MagicMock(return_value= {})
            default_request_client.oauth = mock_oauth_client

            # Act
            default_request_client.get_submissions_by_section_id('1')

            # Assert
            assert mock_oauth_client.get.call_count == 1


    class Test_when_get_users_method_is_called:
        def test_given_a_parameter_is_passed_then_shoud_make_the_get_call(self, default_request_client, mocker):

            # Arrange
            mock_oauth_client = mocker.MagicMock(return_value= {})
            default_request_client.oauth = mock_oauth_client

            # Act
            default_request_client.get_users()

            # Assert
            assert mock_oauth_client.get.call_count == 1

        def test_given_the_get_call_returns_empty_response_then_return_empty_array(self, default_request_client, mocker):

            # Arrange
            mock_oauth_client = mocker.MagicMock(return_value= {})
            default_request_client.oauth = mock_oauth_client

            # Act
            response = default_request_client.get_users()

            # Assert
            assert len(response) == 0

        def test_given_the_get_call_returns_users_then_return_list_of_users(self, default_request_client, mocker):

            # Arrange
            fake_list_of_users = [{"test": "test"}, {"test": "test"}, {"test": "test"}]
            mock_oauth_client = mocker.Mock()
            response_json = mocker.Mock()
            response_json.json = mocker.MagicMock(return_value= { "user": fake_list_of_users})
            mock_oauth_client.get = mocker.MagicMock(return_value= response_json)
            default_request_client.oauth = mock_oauth_client

            # Act
            response = default_request_client.get_users()

            # Assert
            assert len(response) == len(fake_list_of_users)
