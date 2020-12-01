# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
import pytest

from lms_file_tester.validators import file_validation as fileval


def describe_when_validating_users_file():
    def describe_given_valid_columns():
        def it_does_not_return_any_errors(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "UserRole",
                "LocalUserIdentifier",
                "SISUserIdentifier",
                "Name",
                "EmailAddress",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
            ]
            df = pd.DataFrame(columns=columns)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 1).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_users",
                lambda file, nrows: df if nrows == 1 else None,
            )

            # Act
            result = fileval.validate_users_file("random_dir")

            # Arrange
            assert len(result) == 0

    def describe_given_an_extra_column():
        def it_reports_an_error(mocker):
            # Arrange
            columns = [
                "Does not belong here" "SourceSystemIdentifier",
                "SourceSystem",
                "UserRole",
                "LocalUserIdentifier",
                "SISUserIdentifier",
                "Name",
                "EmailAddress",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
            ]
            df = pd.DataFrame(columns=columns)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_users", lambda file, nrows: df
            )

            # Act
            result = fileval.validate_users_file("random_dir")

            # Assert
            assert "Does not belong here" in result[0]

    def describe_given_missing_column():
        @pytest.mark.parametrize(
            "missing",
            [
                "SourceSystemIdentifier",
                "SourceSystem",
                "UserRole",
                "LocalUserIdentifier",
                "SISUserIdentifier",
                "Name",
                "EmailAddress",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
            ],
        )
        def it_reports_an_error(mocker, missing):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "UserRole",
                "LocalUserIdentifier",
                "SISUserIdentifier",
                "Name",
                "EmailAddress",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
            ]
            df = pd.DataFrame(columns=[c for c in columns if c != missing])

            mocker.patch(
                "lms_file_utils.file_reader.get_all_users", lambda file, nrows: df
            )

            # Act
            result = fileval.validate_users_file("random_dir")

            # Arrange
            assert missing in result[0]
