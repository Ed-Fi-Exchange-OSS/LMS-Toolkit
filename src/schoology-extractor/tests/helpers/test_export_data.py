# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest
import pandas as pd

from schoology_extractor.helpers.export_data import to_csv, to_string


class TestExportData():
    class Test_when_to_csv_method_is_called():
        def test_given_no_data_parameter_then_throw_assert_exception(self):
            with pytest.raises(AssertionError):
                to_csv(None, '')   # type: ignore

        def test_given_no_output_parameter_then_throw_assert_exception(self):
            with pytest.raises(AssertionError):
                to_csv([], None)   # type: ignore

        def test_then_call_DataFrame_method(self, mocker):

            # Arrange
            DataFrame_mock = mocker.patch.object(pd, "DataFrame")

            # Act
            to_csv([], '')

            # Assert
            DataFrame_mock.assert_called_once()

    class Test_when_to_string_method_is_called():
        def test_given_no_data_parameter_then_throw_assert_exception(self):
            with pytest.raises(AssertionError):
                to_string(None)   # type: ignore

        def test_then_call_DataFrame_method(self, mocker):
            # Arrange
            fake_data = [
                {"test": "test"},
                {"test": "test"}
            ]
            expected_result = '   test\n0  test\n1  test'

            # Act
            result = to_string(fake_data)

            # Assert
            assert result == expected_result
