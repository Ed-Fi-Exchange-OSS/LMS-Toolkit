# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os

from pandas import DataFrame
from pandas.testing import assert_frame_equal
import pytest

from schoology_extractor.helpers.csv_reader import load_data_frame

DIR_NAME = os.path.dirname(os.path.realpath(__file__))


def describe_when_reading_a_csv_file():
    def describe_given_unrecognized_file_time():
        def it_should_raise_an_error():
            file_name = os.path.join(DIR_NAME, "test.xlsx")

            with pytest.raises(RuntimeError):
                load_data_frame(file_name)

    def describe_given_gzipped_file():
        def it_should_load_the_DataFrame():
            # Arrange
            file_name = os.path.join(DIR_NAME, "test.csv.gz")

            expected = DataFrame([["A1", "B1"], ["A2", "B2"]], columns=["one", "two"])

            # Act
            result = load_data_frame(file_name)

            # Assert
            assert_frame_equal(result, expected)

    def describe_given_plain_file():
        def it_should_load_the_DataFrame():
            # Arrange
            file_name = os.path.join(DIR_NAME, "test.csv")

            expected = DataFrame([["A1", "B1"], ["A2", "B2"]], columns=["one", "two"])

            # Act
            result = load_data_frame(file_name)

            # Assert
            assert_frame_equal(result, expected)
