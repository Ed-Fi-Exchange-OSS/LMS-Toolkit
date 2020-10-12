# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest
import pandas as pd

from schoology_extractor.helpers.export_data import df_to_csv, to_csv, to_string


class TestExportData:
    class Test_when_writing_dataframe_to_csv:
        def test_then_do_not_include_index(self, mocker, fs):
            path = "a/b.csv"
            df = pd.DataFrame([{"a": 1}, {"a": 2}])
            expected = "a\n1\n2\n"

            # Arrange
            fs.create_dir("a")

            # Act
            df_to_csv(df, path)

            # Assert
            with open(path) as f:
                contents = f.read()
                assert expected == contents

    class Test_when_writing_list_to_csv:
        def test_given_no_data_parameter_then_throw_assert_exception(self):
            with pytest.raises(AssertionError):
                to_csv(None, "")  # type: ignore

        def test_given_no_output_parameter_then_throw_assert_exception(self):
            with pytest.raises(AssertionError):
                to_csv([], None)  # type: ignore

        def test_then_write_to_file(self, fs):
            path = "a/b.csv"
            input = [{"a": 1}, {"a": 2}]
            expected = "a\n1\n2\n"

            # Arrange
            fs.create_dir("a")

            # Act
            to_csv(input, path)

            # Assert
            with open(path) as f:
                contents = f.read()
                assert expected == contents

    class Test_when_to_string_method_is_called:
        def test_given_no_data_parameter_then_throw_assert_exception(self):
            with pytest.raises(AssertionError):
                to_string(None)  # type: ignore

        def test_then_call_DataFrame_method(self, mocker):
            # Arrange
            fake_data = [{"test": "test"}, {"test": "test"}]
            expected_result = "   test\n0  test\n1  test"

            # Act
            result = to_string(fake_data)

            # Assert
            assert result == expected_result
