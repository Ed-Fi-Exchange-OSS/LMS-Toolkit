# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from lms_ds_loader.file_processor import FileProcessor
from lms_ds_loader.csv_to_sql import CsvToSql


def create_stub(name, data):
    return type(name, (object,), data)


class Test_FileProcessor:
    class Test_constructor:
        def test_given_file_system_is_None_then_raise_error(self):
            with pytest.raises(AssertionError):
                FileProcessor(None, "nothing")

        def test_given_connection_string_is_None_then_raise_error(self):
            with pytest.raises(AssertionError):
                FileProcessor(object(), None)

        def test_given_connection_string_is_whitespace_then_raise_error(self):
            with pytest.raises(AssertionError):
                FileProcessor(object(), "   ")

    class Test_when_processing_files:
        class Test_given_valid_arguments:
            def test_given_there_are_user_files(self, mocker):
                file_1 = "files/Users/9876-12-31-34-56-01.csv"
                file_2 = "files/Users/9876-12-31-34-56-01.csv"
                connection_string = "asdfghjkl"

                # Arrange
                file_system = create_stub(
                    "LmsFileystemProcessor", {"Users": [file_1, file_2]}
                )

                mock_csv_to_sql = mocker.patch.object(CsvToSql, "load_file")

                # Act
                file_processor = FileProcessor(file_system, connection_string)
                file_processor.load_lms_files_into_database()

                # Assert
                assert file_processor.connection_string == connection_string
                mock_csv_to_sql.assert_called_with(file_1, "User")
                mock_csv_to_sql.assert_called_with(file_2, "User")

            def test_given_there_are_no_user_files(self, mocker):
                connection_string = "asdfghjkl"

                # Arrange
                file_system = create_stub("LmsFileystemProcessor", {"Users": []})

                mock_csv_to_sql = mocker.patch.object(CsvToSql, "load_file")

                # Act
                file_processor = FileProcessor(file_system, connection_string)
                file_processor.load_lms_files_into_database()

                # Assert
                assert file_processor.connection_string == connection_string
                assert not mock_csv_to_sql.called
