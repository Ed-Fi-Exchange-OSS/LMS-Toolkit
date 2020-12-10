# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os

import pytest
import pandas as pd

from schoology_extractor.helpers.csv_writer import df_to_csv


def describe_when_writing_dataframe_to_csv():
    def describe_given_DataFrame_has_data():
        def the_output_should_not_include_the_index(fs):
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

    def describe_given_DataFrame_is_empty():
        def it_should_write_file_for_empty_DataFrame(fs):
            # Arrange
            path = "path"

            # Act
            df_to_csv(pd.DataFrame(), path)

            # Assert
            assert os.path.exists(path)

        def and_the_file_should_be_empty(fs):
            # Arrange
            path = "path"

            # Act
            df_to_csv(pd.DataFrame(), path)

            # Assert
            with open(path) as f:
                contents = f.read()
                assert "\n" == contents
