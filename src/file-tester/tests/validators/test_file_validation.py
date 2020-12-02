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
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "UserRole",
                    "LocalUserIdentifier",
                    "SISUserIdentifier",
                    "Name",
                    "EmailAddress",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_users",
                lambda dir, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_users_file("random_dir")

            # Arrange
            assert len(result) == 0

    def describe_given_invalid_date_format():
        def it_returns_an_error_for_CreateDate(mocker):
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
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "UserRole",
                    "LocalUserIdentifier",
                    "SISUserIdentifier",
                    "Name",
                    "EmailAddress",
                    "EntityStatus",
                    "9876-12-16T15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_users",
                lambda dir, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_users_file("random_dir")

            # Arrange
            assert result[0] == "Users file has an invalid timestamp format for CreateDate"

        def it_returns_an_error_for_LastModifiedDate(mocker):
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
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "UserRole",
                    "LocalUserIdentifier",
                    "SISUserIdentifier",
                    "Name",
                    "EmailAddress",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17T14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_users",
                lambda dir, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_users_file("random_dir")

            # Arrange
            assert result[0] == "Users file has an invalid timestamp format for LastModifiedDate"

    def describe_given_an_extra_column():
        def it_reports_an_error(mocker):
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
                "SourceCreateDate",
                "SourceLastModifiedDate",
                "Does not belong here",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "UserRole",
                    "LocalUserIdentifier",
                    "SISUserIdentifier",
                    "Name",
                    "EmailAddress",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                    "does not belong here",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_users", lambda dir, nrows: df
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
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ],
        )
        def it_reports_an_error(mocker, missing: str):
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
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]

            data = [[]]
            if "SourceSystemIdentifier" != missing:
                data[0].append("SourceSystemIdentifier")
            if "SourceSystem" != missing:
                data[0].append("SourceSystem")
            if "UserRole" != missing:
                data[0].append("UserRole")
            if "LocalUserIdentifier" != missing:
                data[0].append("LocalUserIdentifier")
            if "SISUserIdentifier" != missing:
                data[0].append("SISUserIdentifier")
            if "Name" != missing:
                data[0].append("Name")
            if "EmailAddress" != missing:
                data[0].append("EmailAddress")
            if "EntityStatus" != missing:
                data[0].append("EntityStatus")
            if "CreateDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "LastModifiedDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "SourceCreateDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "SourceLastModifiedDate" != missing:
                data[0].append("9876-12-19 10:11:12")

            df = pd.DataFrame(
                columns=[c for c in columns if c != missing],
                data=data,
            )

            mocker.patch(
                "lms_file_utils.file_reader.get_all_users", lambda dir, nrows: df
            )

            # Act
            result = fileval.validate_users_file("random_dir")

            # Arrange
            assert missing in result[0]

    def describe_given_file_does_not_exist():
        def it_returns_an_error(mocker):
            mocker.patch(
                "lms_file_utils.file_reader.get_all_users",
                lambda dir, nrows: pd.DataFrame(),
            )

            # Act
            result = fileval.validate_users_file("random_dir")

            # Arrange
            assert (
                result[0] == "Users file could not be read or the file does not exist."
            )


def describe_when_validating_sections_file():
    def describe_given_valid_columns():
        def it_does_not_return_any_errors(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "SISSectionIdentifier",
                "Title",
                "SectionDescription",
                "Term",
                "LMSSectionStatus",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "SISSectionIdentifier",
                    "Title",
                    "SectionDescription",
                    "Term",
                    "LMSSectionStatus",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_sections",
                lambda dir, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_sections_file("random_dir")

            # Arrange
            assert len(result) == 0

    def describe_given_invalid_date_format():
        def it_returns_an_error_for_CreateDate(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "SISSectionIdentifier",
                "Title",
                "SectionDescription",
                "Term",
                "LMSSectionStatus",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "SISSectionIdentifier",
                    "Title",
                    "SectionDescription",
                    "Term",
                    "LMSSectionStatus",
                    "EntityStatus",
                    "9876-12-16T15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_sections",
                lambda dir, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_sections_file("random_dir")

            # Arrange
            assert result[0] == "Sections file has an invalid timestamp format for CreateDate"

        def it_returns_an_error_for_LastModifiedDate(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "SISSectionIdentifier",
                "Title",
                "SectionDescription",
                "Term",
                "LMSSectionStatus",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "SISSectionIdentifier",
                    "Title",
                    "SectionDescription",
                    "Term",
                    "LMSSectionStatus",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17T14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_sections",
                lambda dir, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_sections_file("random_dir")

            # Arrange
            assert result[0] == "Sections file has an invalid timestamp format for LastModifiedDate"

    def describe_given_an_extra_column():
        def it_reports_an_error(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "SISSectionIdentifier",
                "Title",
                "SectionDescription",
                "Term",
                "LMSSectionStatus",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
                "Does not belong here",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "SISSectionIdentifier",
                    "Title",
                    "SectionDescription",
                    "Term",
                    "LMSSectionStatus",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                    "Does not belong here",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_sections", lambda dir, nrows: df
            )

            # Act
            result = fileval.validate_sections_file("random_dir")

            # Assert
            assert "Does not belong here" in result[0]

    def describe_given_missing_column():
        @pytest.mark.parametrize(
            "missing",
            [
                "SourceSystemIdentifier",
                "SourceSystem",
                "SISSectionIdentifier",
                "Title",
                "SectionDescription",
                "Term",
                "LMSSectionStatus",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ],
        )
        def it_reports_an_error(mocker, missing):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "SISSectionIdentifier",
                "Title",
                "SectionDescription",
                "Term",
                "LMSSectionStatus",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [[]]
            if "SourceSystemIdentifier" != missing:
                data[0].append("SourceSystemIdentifier")
            if "SourceSystem" != missing:
                data[0].append("SourceSystem")
            if "SISSectionIdentifier" != missing:
                data[0].append("SISSectionIdentifier")
            if "Title" != missing:
                data[0].append("Title")
            if "SectionDescription" != missing:
                data[0].append("SectionDescription")
            if "Term" != missing:
                data[0].append("Term")
            if "LMSSectionStatus" != missing:
                data[0].append("LMSSectionStatus")
            if "EntityStatus" != missing:
                data[0].append("EntityStatus")
            if "CreateDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "LastModifiedDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "SourceCreateDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "SourceLastModifiedDate" != missing:
                data[0].append("9876-12-19 10:11:12")

            df = pd.DataFrame(columns=[c for c in columns if c != missing], data=data)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_sections", lambda dir, nrows: df
            )

            # Act
            result = fileval.validate_sections_file("random_dir")

            # Arrange
            assert missing in result[0]

    def describe_given_file_does_not_exist():
        def it_returns_an_error(mocker):
            mocker.patch(
                "lms_file_utils.file_reader.get_all_sections",
                lambda dir, nrows: pd.DataFrame(),
            )

            # Act
            result = fileval.validate_sections_file("random_dir")

            # Arrange
            assert (
                result[0]
                == "Sections file could not be read or the file does not exist."
            )


def describe_when_validating_system_activities_file():
    def describe_given_valid_columns():
        def it_does_not_return_any_errors(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "LMSUserSourceSystemIdentifier",
                "ActivityDateTime",
                "ActivityType",
                "ActivityStatus",
                "ParentSourceSystemIdentifier",
                "ActivityTimeInMinutes",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "LMSUserSourceSystemIdentifier",
                    "ActivityDateTime",
                    "ActivityType",
                    "ActivityStatus",
                    "ParentSourceSystemIdentifier",
                    "ActivityTimeInMinutes",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_system_activities",
                lambda dir, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_system_activities_file("random_dir")

            # Arrange
            assert len(result) == 0

    def describe_given_invalid_date_format():
        def it_returns_an_error_for_CreateDate(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "LMSUserSourceSystemIdentifier",
                "ActivityDateTime",
                "ActivityType",
                "ActivityStatus",
                "ParentSourceSystemIdentifier",
                "ActivityTimeInMinutes",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "LMSUserSourceSystemIdentifier",
                    "ActivityDateTime",
                    "ActivityType",
                    "ActivityStatus",
                    "ParentSourceSystemIdentifier",
                    "ActivityTimeInMinutes",
                    "EntityStatus",
                    "9876-12-16T15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_system_activities",
                lambda dir, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_system_activities_file("random_dir")

            # Arrange
            assert result[0] == "System Activities file has an invalid timestamp format for CreateDate"

        def it_returns_an_error_for_LastModifiedDate(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "LMSUserSourceSystemIdentifier",
                "ActivityDateTime",
                "ActivityType",
                "ActivityStatus",
                "ParentSourceSystemIdentifier",
                "ActivityTimeInMinutes",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "LMSUserSourceSystemIdentifier",
                    "ActivityDateTime",
                    "ActivityType",
                    "ActivityStatus",
                    "ParentSourceSystemIdentifier",
                    "ActivityTimeInMinutes",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17T14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_system_activities",
                lambda dir, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_system_activities_file("random_dir")

            # Arrange
            assert result[0] == "System Activities file has an invalid timestamp format for LastModifiedDate"

    def describe_given_an_extra_column():
        def it_reports_an_error(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "LMSUserSourceSystemIdentifier",
                "ActivityDateTime",
                "ActivityType",
                "ActivityStatus",
                "ParentSourceSystemIdentifier",
                "ActivityTimeInMinutes",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
                "Does not belong here",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "LMSUserSourceSystemIdentifier",
                    "ActivityDateTime",
                    "ActivityType",
                    "ActivityStatus",
                    "ParentSourceSystemIdentifier",
                    "ActivityTimeInMinutes",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                    "Does not belong here",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_system_activities",
                lambda dir, nrows: df,
            )

            # Act
            result = fileval.validate_system_activities_file("random_dir")

            # Assert
            assert "Does not belong here" in result[0]

    def describe_given_missing_column():
        @pytest.mark.parametrize(
            "missing",
            [
                "SourceSystemIdentifier",
                "SourceSystem",
                "LMSUserSourceSystemIdentifier",
                "ActivityDateTime",
                "ActivityType",
                "ActivityStatus",
                "ParentSourceSystemIdentifier",
                "ActivityTimeInMinutes",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ],
        )
        def it_reports_an_error(mocker, missing):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "LMSUserSourceSystemIdentifier",
                "ActivityDateTime",
                "ActivityType",
                "ActivityStatus",
                "ParentSourceSystemIdentifier",
                "ActivityTimeInMinutes",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]

            data = [[]]
            if "SourceSystemIdentifier" != missing:
                data[0].append("SourceSystemIdentifier")
            if "SourceSystem" != missing:
                data[0].append("SourceSystem")
            if "LMSUserSourceSystemIdentifier" != missing:
                data[0].append("LMSUserSourceSystemIdentifier")
            if "ActivityDateTime" != missing:
                data[0].append("ActivityDateTime")
            if "ActivityType" != missing:
                data[0].append("ActivityType")
            if "ActivityStatus" != missing:
                data[0].append("ActivityStatus")
            if "ParentSourceSystemIdentifier" != missing:
                data[0].append("ParentSourceSystemIdentifier")
            if "ActivityTimeInMinutes" != missing:
                data[0].append("ActivityTimeInMinutes")
            if "EntityStatus" != missing:
                data[0].append("EntityStatus")
            if "CreateDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "LastModifiedDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "SourceCreateDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "SourceLastModifiedDate" != missing:
                data[0].append("9876-12-19 10:11:12")

            df = pd.DataFrame(columns=[c for c in columns if c != missing], data=data)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_system_activities",
                lambda dir, nrows: df,
            )

            # Act
            result = fileval.validate_system_activities_file("random_dir")

            # Arrange
            assert missing in result[0]

    def describe_given_file_does_not_exist():
        def it_returns_an_error(mocker):
            mocker.patch(
                "lms_file_utils.file_reader.get_all_system_activities",
                lambda dir, nrows: pd.DataFrame(),
            )

            # Act
            result = fileval.validate_system_activities_file("random_dir")

            # Arrange
            assert (
                result[0]
                == "System Activities file could not be read or the file does not exist."
            )


def describe_when_validating_section_associations_file():
    def describe_given_valid_columns():
        def it_does_not_return_any_errors(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "EnrollmentStatus",
                "StartDate",
                "EndDate",
                "LMSUserSourceSystemIdentifier",
                "LMSSectionSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "EnrollmentStatus",
                    "StartDate",
                    "EndDate",
                    "LMSUserSourceSystemIdentifier",
                    "LMSSectionSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_section_associations",
                lambda dir, sections, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_section_associations_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert len(result) == 0

    def describe_given_invalid_date_format():
        def it_returns_an_error_for_CreateDate(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "EnrollmentStatus",
                "StartDate",
                "EndDate",
                "LMSUserSourceSystemIdentifier",
                "LMSSectionSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "EnrollmentStatus",
                    "StartDate",
                    "EndDate",
                    "LMSUserSourceSystemIdentifier",
                    "LMSSectionSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16T15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_section_associations",
                lambda dir, sections, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_section_associations_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert result[0] == "Section Associations file has an invalid timestamp format for CreateDate"

        def it_returns_an_error_for_LastModifiedDate(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "EnrollmentStatus",
                "StartDate",
                "EndDate",
                "LMSUserSourceSystemIdentifier",
                "LMSSectionSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "EnrollmentStatus",
                    "StartDate",
                    "EndDate",
                    "LMSUserSourceSystemIdentifier",
                    "LMSSectionSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17T14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_section_associations",
                lambda dir, sections, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_section_associations_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert result[0] == "Section Associations file has an invalid timestamp format for LastModifiedDate"

    def describe_given_an_extra_column():
        def it_reports_an_error(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "EnrollmentStatus",
                "StartDate",
                "EndDate",
                "LMSUserSourceSystemIdentifier",
                "LMSSectionSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
                "Does not belong here",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "EnrollmentStatus",
                    "StartDate",
                    "EndDate",
                    "LMSUserSourceSystemIdentifier",
                    "LMSSectionSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                    "Does not belong here",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_section_associations",
                lambda dir, sections, nrows: df,
            )

            # Act
            result = fileval.validate_section_associations_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Assert
            assert "Does not belong here" in result[0]

    def describe_given_missing_column():
        @pytest.mark.parametrize(
            "missing",
            [
                "SourceSystemIdentifier",
                "SourceSystem",
                "EnrollmentStatus",
                "StartDate",
                "EndDate",
                "LMSUserSourceSystemIdentifier",
                "LMSSectionSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ],
        )
        def it_reports_an_error(mocker, missing):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "EnrollmentStatus",
                "StartDate",
                "EndDate",
                "LMSUserSourceSystemIdentifier",
                "LMSSectionSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [[]]
            if "SourceSystemIdentifier" != missing:
                data[0].append("SourceSystemIdentifier")
            if "SourceSystem" != missing:
                data[0].append("SourceSystem")
            if "EnrollmentStatus" != missing:
                data[0].append("EnrollmentStatus")
            if "StartDate" != missing:
                data[0].append("StartDate")
            if "EndDate" != missing:
                data[0].append("EndDate")
            if "LMSUserSourceSystemIdentifier" != missing:
                data[0].append("LMSUserSourceSystemIdentifier")
            if "LMSSectionSourceSystemIdentifier" != missing:
                data[0].append("LMSSectionSourceSystemIdentifier")
            if "EntityStatus" != missing:
                data[0].append("EntityStatus")
            if "CreateDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "LastModifiedDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "SourceCreateDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "SourceLastModifiedDate" != missing:
                data[0].append("9876-12-19 10:11:12")

            df = pd.DataFrame(columns=[c for c in columns if c != missing], data=data)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_section_associations",
                lambda dir, sections, nrows: df,
            )

            # Act
            result = fileval.validate_section_associations_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert missing in result[0]

    def describe_given_file_does_not_exist():
        def it_returns_an_error(mocker):
            mocker.patch(
                "lms_file_utils.file_reader.get_all_section_associations",
                lambda dir, sections, nrows: pd.DataFrame(),
            )

            # Act
            result = fileval.validate_section_associations_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert (
                result[0]
                == "Section Associations file could not be read or the file does not exist."
            )


def describe_when_validating_section_activities_file():
    def describe_given_valid_columns():
        def it_does_not_return_any_errors(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "ActivityType",
                "ActivityDateTime",
                "ActivityStatus",
                "MessagePost",
                "TotalActivityTimeInMinutes",
                "LMSSectionSourceSystemIdentifier",
                "UserSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "ActivityType",
                    "ActivityDateTime",
                    "ActivityStatus",
                    "MessagePost",
                    "TotalActivityTimeInMinutes",
                    "LMSSectionSourceSystemIdentifier",
                    "UserSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_section_activities",
                lambda dir, sections, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_section_activities_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert len(result) == 0

    def describe_given_invalid_date_format():
        def it_returns_an_error_for_CreateDate(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "ActivityType",
                "ActivityDateTime",
                "ActivityStatus",
                "MessagePost",
                "TotalActivityTimeInMinutes",
                "LMSSectionSourceSystemIdentifier",
                "UserSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "ActivityType",
                    "ActivityDateTime",
                    "ActivityStatus",
                    "MessagePost",
                    "TotalActivityTimeInMinutes",
                    "LMSSectionSourceSystemIdentifier",
                    "UserSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16T15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_section_activities",
                lambda dir, sections, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_section_activities_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert result[0] == "Section Activities file has an invalid timestamp format for CreateDate"

        def it_returns_an_error_for_LastModifiedDate(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "ActivityType",
                "ActivityDateTime",
                "ActivityStatus",
                "MessagePost",
                "TotalActivityTimeInMinutes",
                "LMSSectionSourceSystemIdentifier",
                "UserSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "ActivityType",
                    "ActivityDateTime",
                    "ActivityStatus",
                    "MessagePost",
                    "TotalActivityTimeInMinutes",
                    "LMSSectionSourceSystemIdentifier",
                    "UserSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17T14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_section_activities",
                lambda dir, sections, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_section_activities_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert result[0] == "Section Activities file has an invalid timestamp format for LastModifiedDate"

    def describe_given_an_extra_column():
        def it_reports_an_error(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "ActivityType",
                "ActivityDateTime",
                "ActivityStatus",
                "MessagePost",
                "TotalActivityTimeInMinutes",
                "LMSSectionSourceSystemIdentifier",
                "UserSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
                "Does not belong here",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "ActivityType",
                    "ActivityDateTime",
                    "ActivityStatus",
                    "MessagePost",
                    "TotalActivityTimeInMinutes",
                    "LMSSectionSourceSystemIdentifier",
                    "UserSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                    "Does not belong here",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_section_activities",
                lambda dir, sections, nrows: df,
            )

            # Act
            result = fileval.validate_section_activities_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Assert
            assert "Does not belong here" in result[0]

    def describe_given_missing_column():
        @pytest.mark.parametrize(
            "missing",
            [
                "SourceSystemIdentifier",
                "SourceSystem",
                "ActivityType",
                "ActivityDateTime",
                "ActivityStatus",
                "MessagePost",
                "TotalActivityTimeInMinutes",
                "LMSSectionSourceSystemIdentifier",
                "UserSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ],
        )
        def it_reports_an_error(mocker, missing):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "ActivityType",
                "ActivityDateTime",
                "ActivityStatus",
                "MessagePost",
                "TotalActivityTimeInMinutes",
                "LMSSectionSourceSystemIdentifier",
                "UserSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [[]]
            if "SourceSystemIdentifier" != missing:
                data[0].append("SourceSystemIdentifier")
            if "SourceSystem" != missing:
                data[0].append("SourceSystem")
            if "ActivityType" != missing:
                data[0].append("ActivityType")
            if "ActivityDateTime" != missing:
                data[0].append("ActivityDateTime")
            if "ActivityStatus" != missing:
                data[0].append("ActivityStatus")
            if "MessagePost" != missing:
                data[0].append("MessagePost")
            if "TotalActivityTimeInMinutes" != missing:
                data[0].append("TotalActivityTimeInMinutes")
            if "LMSSectionSourceSystemIdentifier" != missing:
                data[0].append("LMSSectionSourceSystemIdentifier")
            if "UserSourceSystemIdentifier" != missing:
                data[0].append("UserSourceSystemIdentifier")
            if "EntityStatus" != missing:
                data[0].append("EntityStatus")
            if "CreateDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "LastModifiedDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "SourceCreateDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "SourceLastModifiedDate" != missing:
                data[0].append("9876-12-19 10:11:12")

            df = pd.DataFrame(columns=[c for c in columns if c != missing], data=data)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_section_activities",
                lambda dir, sections, nrows: df,
            )

            # Act
            result = fileval.validate_section_activities_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert missing in result[0]

    def describe_given_file_does_not_exist():
        def it_returns_an_error(mocker):
            mocker.patch(
                "lms_file_utils.file_reader.get_all_section_activities",
                lambda dir, sections, nrows: pd.DataFrame(),
            )

            # Act
            result = fileval.validate_section_activities_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert (
                result[0]
                == "Section Activities file could not be read or the file does not exist."
            )


def describe_when_validating_assignments_file():
    def describe_given_valid_columns():
        def it_does_not_return_any_errors(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "Title",
                "AssignmentCategory",
                "AssignmentDescription",
                "StartDateTime",
                "EndDateTime",
                "DueDateTime",
                "SubmissionType",
                "MaxPoints",
                "LMSSectionSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "Title",
                    "AssignmentCategory",
                    "AssignmentDescription",
                    "StartDateTime",
                    "EndDateTime",
                    "DueDateTime",
                    "SubmissionType",
                    "MaxPoints",
                    "LMSSectionSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_assignments",
                lambda dir, sections, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_assignments_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert len(result) == 0

    def describe_given_invalid_date_format():
        def it_returns_an_error_for_CreateDate(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "Title",
                "AssignmentCategory",
                "AssignmentDescription",
                "StartDateTime",
                "EndDateTime",
                "DueDateTime",
                "SubmissionType",
                "MaxPoints",
                "LMSSectionSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "Title",
                    "AssignmentCategory",
                    "AssignmentDescription",
                    "StartDateTime",
                    "EndDateTime",
                    "DueDateTime",
                    "SubmissionType",
                    "MaxPoints",
                    "LMSSectionSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16T15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_assignments",
                lambda dir, sections, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_assignments_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert result[0] == "Assignments file has an invalid timestamp format for CreateDate"

        def it_returns_an_error_for_LastModifiedDate(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "Title",
                "AssignmentCategory",
                "AssignmentDescription",
                "StartDateTime",
                "EndDateTime",
                "DueDateTime",
                "SubmissionType",
                "MaxPoints",
                "LMSSectionSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "Title",
                    "AssignmentCategory",
                    "AssignmentDescription",
                    "StartDateTime",
                    "EndDateTime",
                    "DueDateTime",
                    "SubmissionType",
                    "MaxPoints",
                    "LMSSectionSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17T14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_assignments",
                lambda dir, sections, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_assignments_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert result[0] == "Assignments file has an invalid timestamp format for LastModifiedDate"

    def describe_given_an_extra_column():
        def it_reports_an_error(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "Title",
                "AssignmentCategory",
                "AssignmentDescription",
                "StartDateTime",
                "EndDateTime",
                "DueDateTime",
                "SubmissionType",
                "MaxPoints",
                "LMSSectionSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
                "Does not belong here",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "Title",
                    "AssignmentCategory",
                    "AssignmentDescription",
                    "StartDateTime",
                    "EndDateTime",
                    "DueDateTime",
                    "SubmissionType",
                    "MaxPoints",
                    "LMSSectionSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                    "Does not belong here",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_assignments",
                lambda dir, sections, nrows: df,
            )

            # Act
            result = fileval.validate_assignments_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Assert
            assert "Does not belong here" in result[0]

    def describe_given_missing_column():
        @pytest.mark.parametrize(
            "missing",
            [
                "SourceSystemIdentifier",
                "SourceSystem",
                "Title",
                "AssignmentCategory",
                "AssignmentDescription",
                "StartDateTime",
                "EndDateTime",
                "DueDateTime",
                "SubmissionType",
                "MaxPoints",
                "LMSSectionSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ],
        )
        def it_reports_an_error(mocker, missing):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "Title",
                "AssignmentCategory",
                "AssignmentDescription",
                "StartDateTime",
                "EndDateTime",
                "DueDateTime",
                "SubmissionType",
                "MaxPoints",
                "LMSSectionSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [[]]
            if "SourceSystemIdentifier" != missing:
                data[0].append("SourceSystemIdentifier")
            if "SourceSystem" != missing:
                data[0].append("SourceSystem")
            if "Title" != missing:
                data[0].append("Title")
            if "AssignmentCategory" != missing:
                data[0].append("AssignmentCategory")
            if "AssignmentDescription" != missing:
                data[0].append("AssignmentDescription")
            if "StartDateTime" != missing:
                data[0].append("StartDateTime")
            if "EndDateTime" != missing:
                data[0].append("EndDateTime")
            if "DueDateTime" != missing:
                data[0].append("DueDateTime")
            if "SubmissionType" != missing:
                data[0].append("SubmissionType")
            if "MaxPoints" != missing:
                data[0].append("MaxPoints")
            if "LMSSectionSourceSystemIdentifier" != missing:
                data[0].append("LMSSectionSourceSystemIdentifier")
            if "EntityStatus" != missing:
                data[0].append("EntityStatus")
            if "CreateDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "LastModifiedDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "SourceCreateDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "SourceLastModifiedDate" != missing:
                data[0].append("9876-12-19 10:11:12")

            df = pd.DataFrame(columns=[c for c in columns if c != missing], data=data)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_assignments",
                lambda dir, sections, nrows: df,
            )

            # Act
            result = fileval.validate_assignments_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert missing in result[0]

    def describe_given_file_does_not_exist():
        def it_returns_an_error(mocker):
            mocker.patch(
                "lms_file_utils.file_reader.get_all_assignments",
                lambda dir, sections, nrows: pd.DataFrame(),
            )

            # Act
            result = fileval.validate_assignments_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert (
                result[0]
                == "Assignments file could not be read or the file does not exist."
            )


def describe_when_validating_submissions_file():
    def describe_given_valid_columns():
        def it_does_not_return_any_errors(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "SubmissionStatus",
                "SubmissionDateTime",
                "EarnedPoints",
                "Grade",
                "AssignmentSourceSystemIdentifier",
                "LMSUserSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "SubmissionStatus",
                    "SubmissionDateTime",
                    "EarnedPoints",
                    "Grade",
                    "AssignmentSourceSystemIdentifier",
                    "LMSUserSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_submissions",
                lambda dir, assignments, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_submissions_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert len(result) == 0

    def describe_given_invalid_date_format():
        def it_returns_an_error_for_CreateDate(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "SubmissionStatus",
                "SubmissionDateTime",
                "EarnedPoints",
                "Grade",
                "AssignmentSourceSystemIdentifier",
                "LMSUserSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "SubmissionStatus",
                    "SubmissionDateTime",
                    "EarnedPoints",
                    "Grade",
                    "AssignmentSourceSystemIdentifier",
                    "LMSUserSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16T15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_submissions",
                lambda dir, assignments, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_submissions_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert result[0] == "Submissions file has an invalid timestamp format for CreateDate"

        def it_returns_an_error_for_LastModifiedDate(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "SubmissionStatus",
                "SubmissionDateTime",
                "EarnedPoints",
                "Grade",
                "AssignmentSourceSystemIdentifier",
                "LMSUserSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "SubmissionStatus",
                    "SubmissionDateTime",
                    "EarnedPoints",
                    "Grade",
                    "AssignmentSourceSystemIdentifier",
                    "LMSUserSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17T14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_submissions",
                lambda dir, assignments, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_submissions_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert result[0] == "Submissions file has an invalid timestamp format for LastModifiedDate"

    def describe_given_an_extra_column():
        def it_reports_an_error(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "SubmissionStatus",
                "SubmissionDateTime",
                "EarnedPoints",
                "Grade",
                "AssignmentSourceSystemIdentifier",
                "LMSUserSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
                "Does not belong here",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "SubmissionStatus",
                    "SubmissionDateTime",
                    "EarnedPoints",
                    "Grade",
                    "AssignmentSourceSystemIdentifier",
                    "LMSUserSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                    "Does not belong here",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_submissions",
                lambda dir, assignments, nrows: df,
            )

            # Act
            result = fileval.validate_submissions_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Assert
            assert "Does not belong here" in result[0]

    def describe_given_missing_column():
        @pytest.mark.parametrize(
            "missing",
            [
                "SourceSystemIdentifier",
                "SourceSystem",
                "SubmissionStatus",
                "SubmissionDateTime",
                "EarnedPoints",
                "Grade",
                "AssignmentSourceSystemIdentifier",
                "LMSUserSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ],
        )
        def it_reports_an_error(mocker, missing):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "SubmissionStatus",
                "SubmissionDateTime",
                "EarnedPoints",
                "Grade",
                "AssignmentSourceSystemIdentifier",
                "LMSUserSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [[]]
            if "SourceSystemIdentifier" != missing:
                data[0].append("SourceSystemIdentifier")
            if "SourceSystem" != missing:
                data[0].append("SourceSystem")
            if "SubmissionStatus" != missing:
                data[0].append("SubmissionStatus")
            if "SubmissionDateTime" != missing:
                data[0].append("SubmissionDateTime")
            if "EarnedPoints" != missing:
                data[0].append("EarnedPoints")
            if "Grade" != missing:
                data[0].append("Grade")
            if "AssignmentSourceSystemIdentifier" != missing:
                data[0].append("AssignmentSourceSystemIdentifier")
            if "LMSUserSourceSystemIdentifier" != missing:
                data[0].append("LMSUserSourceSystemIdentifier")
            if "EntityStatus" != missing:
                data[0].append("EntityStatus")
            if "CreateDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "LastModifiedDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "SourceCreateDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "SourceLastModifiedDate" != missing:
                data[0].append("9876-12-19 10:11:12")

            df = pd.DataFrame(columns=[c for c in columns if c != missing], data=data)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_submissions",
                lambda dir, assignments, nrows: df,
            )

            # Act
            result = fileval.validate_submissions_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert missing in result[0]

    def describe_given_file_does_not_exist():
        def it_returns_an_error(mocker):
            mocker.patch(
                "lms_file_utils.file_reader.get_all_submissions",
                lambda dir, assignments, nrows: pd.DataFrame(),
            )

            # Act
            result = fileval.validate_submissions_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert (
                result[0]
                == "Submissions file could not be read or the file does not exist."
            )


def describe_when_validating_grades_file():
    def describe_given_valid_columns():
        def it_does_not_return_any_errors(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "Grade",
                "GradeType",
                "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "Grade",
                    "GradeType",
                    "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_grades",
                lambda dir, sections, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_grades_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert len(result) == 0

    def describe_given_invalid_date_format():
        def it_returns_an_error_for_CreateDate(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "Grade",
                "GradeType",
                "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "Grade",
                    "GradeType",
                    "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16T15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_grades",
                lambda dir, sections, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_grades_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert result[0] == "Grades file has an invalid timestamp format for CreateDate"

        def it_returns_an_error_for_LastModifiedDate(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "Grade",
                "GradeType",
                "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "Grade",
                    "GradeType",
                    "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17T14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_grades",
                lambda dir, sections, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_grades_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert result[0] == "Grades file has an invalid timestamp format for LastModifiedDate"

    def describe_given_an_extra_column():
        def it_reports_an_error(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "Grade",
                "GradeType",
                "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
                "Does not belong here",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "Grade",
                    "GradeType",
                    "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                    "Does not belong here",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_grades",
                lambda dir, sections, nrows: df,
            )

            # Act
            result = fileval.validate_grades_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Assert
            assert "Does not belong here" in result[0]

    def describe_given_missing_column():
        @pytest.mark.parametrize(
            "missing",
            [
                "SourceSystemIdentifier",
                "SourceSystem",
                "Grade",
                "GradeType",
                "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ],
        )
        def it_reports_an_error(mocker, missing):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "Grade",
                "GradeType",
                "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [[]]
            if "SourceSystemIdentifier" != missing:
                data[0].append("SourceSystemIdentifier")
            if "SourceSystem" != missing:
                data[0].append("SourceSystem")
            if "Grade" != missing:
                data[0].append("Grade")
            if "GradeType" != missing:
                data[0].append("GradeType")
            if "LMSUserLMSSectionAssociationSourceSystemIdentifier" != missing:
                data[0].append("LMSUserLMSSectionAssociationSourceSystemIdentifier")
            if "EntityStatus" != missing:
                data[0].append("EntityStatus")
            if "CreateDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "LastModifiedDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "SourceCreateDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "SourceLastModifiedDate" != missing:
                data[0].append("9876-12-19 10:11:12")

            df = pd.DataFrame(columns=[c for c in columns if c != missing], data=data)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_grades",
                lambda dir, sections, nrows: df,
            )

            # Act
            result = fileval.validate_grades_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert missing in result[0]

    def describe_given_file_does_not_exist():
        def it_returns_an_error(mocker):
            mocker.patch(
                "lms_file_utils.file_reader.get_all_grades",
                lambda dir, sections, nrows: pd.DataFrame(),
            )

            # Act
            result = fileval.validate_grades_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert (
                result[0] == "Grades file could not be read or the file does not exist."
            )


def describe_when_validating_attendance_events_file():
    def describe_given_valid_columns():
        def it_does_not_return_any_errors(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "EventDate",
                "AttendanceStatus",
                "LMSSectionAssociationSystemIdentifier",
                "LMSUserSourceSystemIdentifier",
                "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "EventDate",
                    "AttendanceStatus",
                    "LMSSectionAssociationSystemIdentifier",
                    "LMSUserSourceSystemIdentifier",
                    "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 2).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_attendance_events",
                lambda dir, sections, nrows: df if nrows == 2 else None,
            )

            # Act
            result = fileval.validate_attendance_events_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert len(result) == 0

    def describe_given_invalid_date_format():
        def it_returns_an_error_for_CreateDate(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "EventDate",
                "AttendanceStatus",
                "LMSSectionAssociationSystemIdentifier",
                "LMSUserSourceSystemIdentifier",
                "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "EventDate",
                    "AttendanceStatus",
                    "LMSSectionAssociationSystemIdentifier",
                    "LMSUserSourceSystemIdentifier",
                    "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16T15:16:17",  # This has the error
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_attendance_events",
                lambda dir, sections, nrows: df,
            )

            # Act
            result = fileval.validate_attendance_events_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert result[0] == "Attendance Events file has an invalid timestamp format for CreateDate"

        def it_returns_an_error_for_LastModifiedDate(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "EventDate",
                "AttendanceStatus",
                "LMSSectionAssociationSystemIdentifier",
                "LMSUserSourceSystemIdentifier",
                "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "EventDate",
                    "AttendanceStatus",
                    "LMSSectionAssociationSystemIdentifier",
                    "LMSUserSourceSystemIdentifier",
                    "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17T14:15:16",  # This has the error
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_attendance_events",
                lambda dir, sections, nrows: df,
            )

            # Act
            result = fileval.validate_attendance_events_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert result[0] == "Attendance Events file has an invalid timestamp format for LastModifiedDate"

    def describe_given_an_extra_column():
        def it_reports_an_error(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "EventDate",
                "AttendanceStatus",
                "LMSSectionAssociationSystemIdentifier",
                "LMSUserSourceSystemIdentifier",
                "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
                "Does not belong here",
            ]
            data = [
                [
                    "SourceSystemIdentifier",
                    "SourceSystem",
                    "9876-12-19 10:11:12",
                    "AttendanceStatus",
                    "LMSSectionAssociationSystemIdentifier",
                    "LMSUserSourceSystemIdentifier",
                    "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                    "EntityStatus",
                    "9876-12-16 15:16:17",
                    "9876-12-17 14:15:16",
                    "9876-12-18 13:14:15",
                    "9876-12-19 10:11:12",
                    "Does not belong here",
                ]
            ]
            df = pd.DataFrame(columns=columns, data=data)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_attendance_events",
                lambda dir, sections, nrows: df,
            )

            # Act
            result = fileval.validate_attendance_events_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Assert
            assert "Does not belong here" in result[0]

    def describe_given_missing_column():
        @pytest.mark.parametrize(
            "missing",
            [
                "SourceSystemIdentifier",
                "SourceSystem",
                "EventDate",
                "AttendanceStatus",
                "LMSSectionAssociationSystemIdentifier",
                "LMSUserSourceSystemIdentifier",
                "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ],
        )
        def it_reports_an_error(mocker, missing):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "EventDate",
                "AttendanceStatus",
                "LMSSectionAssociationSystemIdentifier",
                "LMSUserSourceSystemIdentifier",
                "LMSUserLMSSectionAssociationSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            data = [[]]
            if "SourceSystemIdentifier" != missing:
                data[0].append("SourceSystemIdentifier")
            if "SourceSystem" != missing:
                data[0].append("SourceSystem")
            if "EventDate" != missing:
                data[0].append("EventDate")
            if "AttendanceStatus" != missing:
                data[0].append("AttendanceStatus")
            if "LMSSectionAssociationSystemIdentifier" != missing:
                data[0].append("LMSSectionAssociationSystemIdentifier")
            if "LMSUserSourceSystemIdentifier" != missing:
                data[0].append("LMSUserSourceSystemIdentifier")
            if "LMSUserLMSSectionAssociationSourceSystemIdentifier" != missing:
                data[0].append("LMSUserLMSSectionAssociationSourceSystemIdentifier")
            if "EntityStatus" != missing:
                data[0].append("EntityStatus")
            if "CreateDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "LastModifiedDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "SourceCreateDate" != missing:
                data[0].append("9876-12-19 10:11:12")
            if "SourceLastModifiedDate" != missing:
                data[0].append("9876-12-19 10:11:12")

            df = pd.DataFrame(columns=[c for c in columns if c != missing], data=data)

            mocker.patch(
                "lms_file_utils.file_reader.get_all_attendance_events",
                lambda dir, sections, nrows: df,
            )

            # Act
            result = fileval.validate_attendance_events_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert missing in result[0]

    def describe_given_file_does_not_exist():
        def it_returns_an_error(mocker):
            mocker.patch(
                "lms_file_utils.file_reader.get_all_attendance_events",
                lambda dir, sections, nrows: pd.DataFrame(),
            )

            # Act
            result = fileval.validate_attendance_events_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert (
                result[0]
                == "Attendance Events file could not be read or the file does not exist."
            )
