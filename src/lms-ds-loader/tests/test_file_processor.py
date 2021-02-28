# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest
from unittest.mock import Mock

from edfi_lms_ds_loader.helpers.constants import Table, Columns
from edfi_lms_ds_loader.csv_to_sql import CsvToSql
from edfi_lms_ds_loader.file_processor import FileProcessor
from edfi_lms_ds_loader.lms_filesystem_provider import LmsFilesystemProvider
from edfi_lms_ds_loader.mssql_lms_operations import MssqlLmsOperations


class Test_FileProcessor:
    class Test_when_processing_files:
        class Test_given_invalid_object_state:
            def test_given_file_system_is_None_then_raise_error(self):
                with pytest.raises(AssertionError):
                    FileProcessor(None, "nothing").load_lms_files_into_database()

            def test_given_adapter_is_None_then_raise_error(self):
                with pytest.raises(AssertionError):
                    FileProcessor(object(), None).load_lms_files_into_database()

        class Test_given_valid_arguments:
            def test_given_there_are_user_files(self, mocker):
                file_1 = "files/Users/9876-12-31-34-56-01.csv"
                file_2 = "files/Users/9876-12-31-34-56-01.csv"

                # Arrange
                file_system = Mock(spec=LmsFilesystemProvider)
                file_system.Users = [file_1, file_2]

                mock_csv_to_sql = mocker.patch.object(CsvToSql, "load_file")
                db_operations_adapter = Mock(spec=MssqlLmsOperations)

                # Act
                file_processor = FileProcessor(file_system, db_operations_adapter)
                file_processor.load_lms_files_into_database()

                # Assert
                assert file_processor.db_operations_adapter == db_operations_adapter
                mock_csv_to_sql.assert_called_with(
                    file_1, Table.USER, Columns.USER
                )
                mock_csv_to_sql.assert_called_with(
                    file_2, Table.USER, Columns.USER
                )

            def test_given_there_are_no_user_files(self, mocker):

                # Arrange
                file_system = Mock(spec=LmsFilesystemProvider)
                file_system.Users = list()

                db_operations_adapter = Mock(spec=MssqlLmsOperations)

                mock_csv_to_sql = mocker.patch.object(CsvToSql, "load_file")

                # Act
                file_processor = FileProcessor(file_system, db_operations_adapter)
                file_processor.load_lms_files_into_database()

                # Assert
                assert file_processor.file_system == file_system
                assert file_processor.db_operations_adapter == db_operations_adapter
                assert not mock_csv_to_sql.called
