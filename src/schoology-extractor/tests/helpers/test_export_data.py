# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os

import pytest
import pandas as pd

from schoology_extractor.helpers.export_data import df_to_csv, to_csv, to_string


def describe_when_exporting_data():
    def describe_when_writing_dataframe_to_csv():
        def it_should_not_include_index(fs):
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

        def it_should_not_write_file_for_empty_DataFrame(fs):
            # Act
            df_to_csv(pd.DataFrame(), "path")

            # Assert
            assert not os.path.exists("path")

    def describe_when_writing_list_to_csv():
        def given_no_data_parameter_then_throw_assert_exception():
            with pytest.raises(AssertionError):
                to_csv(None, "")  # type: ignore

        def test_given_no_output_parameter_then_throw_assert_exception():
            with pytest.raises(AssertionError):
                to_csv([], None)  # type: ignore

        def it_should_write_to_file(fs):
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

    def describe_when_to_string_method_is_called():
        def given_no_data_parameter_then_throw_assert_exception():
            with pytest.raises(AssertionError):
                to_string(None)  # type: ignore

        def it_should_call_DataFrame_method():
            # Arrange
            fake_data = [{"test": "test"}, {"test": "test"}]
            expected_result = "   test\n0  test\n1  test"

            # Act
            result = to_string(fake_data)

            # Assert
            assert result == expected_result
