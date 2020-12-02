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
            df = pd.DataFrame(columns=columns)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 1).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_users",
                lambda dir, nrows: df if nrows == 1 else None,
            )

            # Act
            result = fileval.validate_users_file("random_dir")

            # Arrange
            assert len(result) == 0

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
            df = pd.DataFrame(columns=columns)

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
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            df = pd.DataFrame(columns=[c for c in columns if c != missing])

            mocker.patch(
                "lms_file_utils.file_reader.get_all_users", lambda dir, nrows: df
            )

            # Act
            result = fileval.validate_users_file("random_dir")

            # Arrange
            assert missing in result[0]


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
            df = pd.DataFrame(columns=columns)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 1).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_sections",
                lambda dir, nrows: df if nrows == 1 else None,
            )

            # Act
            result = fileval.validate_sections_file("random_dir")

            # Arrange
            assert len(result) == 0

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
            df = pd.DataFrame(columns=columns)

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
            df = pd.DataFrame(columns=[c for c in columns if c != missing])

            mocker.patch(
                "lms_file_utils.file_reader.get_all_sections", lambda dir, nrows: df
            )

            # Act
            result = fileval.validate_sections_file("random_dir")

            # Arrange
            assert missing in result[0]


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
            df = pd.DataFrame(columns=columns)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 1).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_system_activities",
                lambda dir, nrows: df if nrows == 1 else None,
            )

            # Act
            result = fileval.validate_system_activities_file("random_dir")

            # Arrange
            assert len(result) == 0

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
            df = pd.DataFrame(columns=columns)

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
            df = pd.DataFrame(columns=[c for c in columns if c != missing])

            mocker.patch(
                "lms_file_utils.file_reader.get_all_system_activities",
                lambda dir, nrows: df,
            )

            # Act
            result = fileval.validate_system_activities_file("random_dir")

            # Arrange
            assert missing in result[0]


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
            df = pd.DataFrame(columns=columns)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 1).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_section_associations",
                lambda dir, sections, nrows: df if nrows == 1 else None,
            )

            # Act
            result = fileval.validate_section_associations_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert len(result) == 0

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
            df = pd.DataFrame(columns=columns)

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
            df = pd.DataFrame(columns=[c for c in columns if c != missing])

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
            df = pd.DataFrame(columns=columns)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 1).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_section_activities",
                lambda dir, sections, nrows: df if nrows == 1 else None,
            )

            # Act
            result = fileval.validate_section_activities_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert len(result) == 0

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
            df = pd.DataFrame(columns=columns)

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
            df = pd.DataFrame(columns=[c for c in columns if c != missing])

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
            df = pd.DataFrame(columns=columns)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 1).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_assignments",
                lambda dir, sections, nrows: df if nrows == 1 else None,
            )

            # Act
            result = fileval.validate_assignments_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert len(result) == 0

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
            df = pd.DataFrame(columns=columns)

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
            df = pd.DataFrame(columns=[c for c in columns if c != missing])

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


def describe_when_validating_submissions_file():
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
            df = pd.DataFrame(columns=columns)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 1).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_submissions",
                lambda dir, assignments, nrows: df if nrows == 1 else None,
            )

            # Act
            result = fileval.validate_submissions_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert len(result) == 0

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
            df = pd.DataFrame(columns=columns)

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
            df = pd.DataFrame(columns=[c for c in columns if c != missing])

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
            df = pd.DataFrame(columns=columns)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 1).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_grades",
                lambda dir, sections, nrows: df if nrows == 1 else None,
            )

            # Act
            result = fileval.validate_grades_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert len(result) == 0

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
            df = pd.DataFrame(columns=columns)

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
            df = pd.DataFrame(columns=[c for c in columns if c != missing])

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


def describe_when_validating_attendance_events_file():
    def describe_given_valid_columns():
        def it_does_not_return_any_errors(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "Date",
                "AttendanceStatus",
                "SectionAssociationSystemIdentifier",
                "UserSourceSystemIdentifier",
                "UserLMSSectionAssociationSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            df = pd.DataFrame(columns=columns)

            mocker.patch(
                # This has an implicit assertion built in (if nrows == 1).
                # There is a better way to do this, just not remembering it at
                # the moment...
                "lms_file_utils.file_reader.get_all_attendance_events",
                lambda dir, sections, nrows: df if nrows == 1 else None,
            )

            # Act
            result = fileval.validate_attendance_events_file(
                "random_dir", pd.DataFrame([{"a": 1}])
            )

            # Arrange
            assert len(result) == 0

    def describe_given_an_extra_column():
        def it_reports_an_error(mocker):
            # Arrange
            columns = [
                "SourceSystemIdentifier",
                "SourceSystem",
                "Date",
                "AttendanceStatus",
                "SectionAssociationSystemIdentifier",
                "UserSourceSystemIdentifier",
                "UserLMSSectionAssociationSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
                "Does not belong here",
            ]
            df = pd.DataFrame(columns=columns)

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
                "Date",
                "AttendanceStatus",
                "SectionAssociationSystemIdentifier",
                "UserSourceSystemIdentifier",
                "UserLMSSectionAssociationSourceSystemIdentifier",
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
                "Date",
                "AttendanceStatus",
                "SectionAssociationSystemIdentifier",
                "UserSourceSystemIdentifier",
                "UserLMSSectionAssociationSourceSystemIdentifier",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
                "SourceCreateDate",
                "SourceLastModifiedDate",
            ]
            df = pd.DataFrame(columns=[c for c in columns if c != missing])

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
