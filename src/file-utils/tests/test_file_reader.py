# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Callable, List
import pandas as pd
from unittest.mock import Mock
import pytest

from edfi_lms_file_utils.file_reader import (
    _read_csv,
    get_all_users,
    get_all_sections,
    get_all_section_associations,
    get_all_section_activities,
    get_all_system_activities,
    get_all_assignments,
    get_all_submissions,
    get_all_grades,
    get_all_attendance_events,
    read_assignments_file,
    read_attendance_events_file,
    read_grades_file,
    read_section_activities_file,
    read_section_associations_file,
    read_sections_file,
    read_submissions_file,
    read_system_activities_file,
    read_users_file,
)
from edfi_lms_file_utils.constants import DataTypes
from .constants import BASE_DIRECTORY

SECTIONS = "sections"
USERS = "users"
SYSTEM_ACTIVITIES = "system-activities"
SECTION_ACTIVITIES = "section-activities"
SECTION_ASSOCIATIONS = "section-associations"
GRADES = "grades"
ASSIGNMENTS = "assignments"
SUBMISSIONS = "submissions"
ATTENDANCE_EVENTS = "attendance-events"

# Could substitute constants above into constants below, but this gives better
# transparency on exactly what to expect
SECTIONS_FILE = "base_dir/sections/2020-11-19-04-05-06.csv"
USERS_FILE = "base_dir/users/2020-11-19-04-05-06.csv"
ASSIGNMENTS_FILE = "base_dir/section=1/assignments/2020-11-19-04-05-06.csv"
ASSOCIATIONS_FILE = "base_dir/section=1/section-associations/2020-11-19-04-05-06.csv"
GRADES_FILE = "base_dir/section=1/grades/2020-11-19-04-05-06.csv"
SUBMISSIONS_FILE = "base_dir/section=1/assignment=2/submissions/2020-11-19-04-05-06.csv"
ATTENDANCE_FILE = "base_dir/section=1/attendance-events/2020-11-19-04-05-06.csv"
SECTION_ACTIVITIES_FILE = (
    "base_dir/section=1/section-activities/2020-11-19-04-05-06.csv"
)
SYSTEM_ACTIVITIES_FILE = "base_dir/system-activities/2020-11-19/2020-11-19-04-05-06.csv"

INPUT_DF = pd.DataFrame(
    [{"SourceSystemIdentifier": 1, "LMSSectionSourceSystemIdentifier": 2}]
)


def generate_data_frame(resource: str) -> pd.DataFrame:
    return pd.DataFrame([{resource: 1}])


def describe_given_files_exist() -> None:
    @pytest.fixture
    def fixture(mocker) -> None:

        mocker.patch(
            "edfi_lms_file_utils.file_repository.get_users_file", lambda _: USERS_FILE
        )
        mocker.patch(
            "edfi_lms_file_utils.file_repository.get_sections_file",
            lambda _: SECTIONS_FILE,
        )
        mocker.patch(
            "edfi_lms_file_utils.file_repository.get_system_activities_files",
            lambda _: [SYSTEM_ACTIVITIES_FILE],
        )
        mocker.patch(
            "edfi_lms_file_utils.file_repository.get_section_associations_file",
            lambda _a, _b: ASSOCIATIONS_FILE,
        )
        mocker.patch(
            "edfi_lms_file_utils.file_repository.get_section_activities_file",
            lambda _a, _b: SECTION_ACTIVITIES_FILE,
        )
        mocker.patch(
            "edfi_lms_file_utils.file_repository.get_assignments_file",
            lambda _a, _b: ASSIGNMENTS_FILE,
        )
        mocker.patch(
            "edfi_lms_file_utils.file_repository.get_grades_file",
            lambda _a, _b: GRADES_FILE,
        )
        mocker.patch(
            "edfi_lms_file_utils.file_repository.get_submissions_file",
            lambda _a, _b, _c: SUBMISSIONS_FILE,
        )
        mocker.patch(
            "edfi_lms_file_utils.file_repository.get_attendance_events_file",
            lambda _a, _b: ATTENDANCE_FILE,
        )

        def _fake_reader(file: str, **kwargs) -> pd.DataFrame:
            switcher = {
                USERS_FILE: generate_data_frame(USERS),
                SECTIONS_FILE: generate_data_frame(SECTIONS),
                SYSTEM_ACTIVITIES_FILE: generate_data_frame(SYSTEM_ACTIVITIES),
                ASSOCIATIONS_FILE: generate_data_frame(SECTION_ASSOCIATIONS),
                SECTION_ACTIVITIES_FILE: generate_data_frame(SECTION_ACTIVITIES),
                ASSIGNMENTS_FILE: generate_data_frame(ASSIGNMENTS),
                GRADES_FILE: generate_data_frame(GRADES),
                SUBMISSIONS_FILE: generate_data_frame(SUBMISSIONS),
                ATTENDANCE_FILE: generate_data_frame(ATTENDANCE_EVENTS),
            }
            return switcher.get(file, pd.DataFrame())

        pd.read_csv = Mock(side_effect=_fake_reader)

    def describe_when_getting_users() -> None:
        def it_should_read_file_into_DataFrame(mocker, fixture) -> None:
            df = get_all_users(BASE_DIRECTORY)

            assert df.iloc[0][USERS] == 1

    def describe_when_getting_section() -> None:
        def it_should_read_file_into_DataFrame(mocker, fixture) -> None:
            df = get_all_sections(BASE_DIRECTORY)

            assert df.iloc[0][SECTIONS] == 1

    def describe_when_getting_system_activities() -> None:
        def it_should_read_file_into_DataFrame(mocker, fixture) -> None:
            df = get_all_system_activities(BASE_DIRECTORY)

            assert df.iloc[0][SYSTEM_ACTIVITIES] == 1

    def describe_when_getting_section_associations() -> None:
        def describe_given_there_are_sections() -> None:
            def it_should_read_file_into_DataFrame(mocker, fixture) -> None:

                df = get_all_section_associations(BASE_DIRECTORY, INPUT_DF)

                assert df.iloc[0][SECTION_ASSOCIATIONS] == 1

        def describe_given_empty_section_list() -> None:
            def it_should_return_empty_data_frame(mocker, fixture) -> None:
                df = get_all_section_associations(BASE_DIRECTORY, pd.DataFrame())

                assert df.empty

    def describe_when_getting_section_activities() -> None:
        def describe_given_there_are_sections() -> None:
            def it_should_read_file_into_DataFrame(mocker, fixture) -> None:

                df = get_all_section_activities(BASE_DIRECTORY, INPUT_DF)

                assert df.iloc[0][SECTION_ACTIVITIES] == 1

        def describe_given_empty_section_list() -> None:
            def it_should_return_empty_data_frame(mocker, fixture) -> None:
                df = get_all_section_activities(BASE_DIRECTORY, pd.DataFrame())

                assert df.empty

    def describe_when_getting_assignments() -> None:
        def it_should_read_file_into_DataFrame(mocker, fixture) -> None:

            df = get_all_assignments(BASE_DIRECTORY, INPUT_DF)

            assert df.iloc[0][ASSIGNMENTS] == 1

        def describe_given_empty_section_list() -> None:
            def it_should_return_empty_data_frame(mocker, fixture) -> None:
                df = get_all_assignments(BASE_DIRECTORY, pd.DataFrame())

                assert df.empty

    def describe_when_getting_submissions() -> None:
        def it_should_read_file_into_DataFrame(mocker, fixture) -> None:

            df = get_all_submissions(BASE_DIRECTORY, INPUT_DF)

            assert df.iloc[0][SUBMISSIONS] == 1

        def describe_given_empty_assignments_list() -> None:
            def it_should_return_empty_data_frame(mocker, fixture) -> None:

                df = get_all_submissions(BASE_DIRECTORY, pd.DataFrame())

                assert df.empty

    def describe_when_getting_grades() -> None:
        def it_should_read_file_into_DataFrame(mocker, fixture) -> None:

            df = get_all_grades(BASE_DIRECTORY, INPUT_DF)

            assert df.iloc[0][GRADES] == 1

        def describe_given_empty_section_list() -> None:
            def it_should_return_empty_data_frame(mocker, fixture) -> None:
                df = get_all_grades(BASE_DIRECTORY, pd.DataFrame())

                assert df.empty

    def describe_when_getting_attendance_events() -> None:
        def it_should_read_file_into_DataFrame(mocker, fixture) -> None:

            df = get_all_attendance_events(BASE_DIRECTORY, INPUT_DF)

            assert df.iloc[0][ATTENDANCE_EVENTS] == 1

        def describe_given_empty_section_list() -> None:
            def it_should_return_empty_data_frame(mocker, fixture) -> None:
                df = get_all_attendance_events(BASE_DIRECTORY, pd.DataFrame())

                assert df.empty


def describe_given_there_are_no_files_to_read() -> None:
    @pytest.fixture
    def fixture(mocker) -> None:

        mocker.patch(
            "edfi_lms_file_utils.file_repository.get_users_file", lambda _: None
        )
        mocker.patch(
            "edfi_lms_file_utils.file_repository.get_sections_file", lambda _: None
        )
        mocker.patch(
            "edfi_lms_file_utils.file_repository.get_system_activities_files",
            lambda _: None,
        )
        mocker.patch(
            "edfi_lms_file_utils.file_repository.get_section_associations_file",
            lambda _a, _b: None,
        )
        mocker.patch(
            "edfi_lms_file_utils.file_repository.get_section_activities_file",
            lambda _a, _b: None,
        )
        mocker.patch(
            "edfi_lms_file_utils.file_repository.get_assignments_file",
            lambda _a, _b: None,
        )
        mocker.patch(
            "edfi_lms_file_utils.file_repository.get_grades_file", lambda _a, _b: None
        )
        mocker.patch(
            "edfi_lms_file_utils.file_repository.get_submissions_file",
            lambda _a, _b, _c: None,
        )
        mocker.patch(
            "edfi_lms_file_utils.file_repository.get_attendance_events_file",
            lambda _a, _b: None,
        )

    def describe_when_getting_users() -> None:
        def it_should_return_an_empty_DataFrame(mocker, fixture) -> None:
            df = get_all_users(BASE_DIRECTORY)

            assert df.empty

    def describe_when_getting_section() -> None:
        def it_should_return_an_empty_DataFrame(mocker, fixture) -> None:
            df = get_all_sections(BASE_DIRECTORY)

            assert df.empty

    def describe_when_getting_system_activities() -> None:
        def it_should_return_an_empty_DataFrame(mocker, fixture) -> None:
            df = get_all_system_activities(BASE_DIRECTORY)

            assert df.empty

    def describe_when_getting_section_associations() -> None:
        def it_should_return_an_empty_DataFrame(mocker, fixture) -> None:

            df = get_all_section_associations(BASE_DIRECTORY, INPUT_DF)

            assert df.empty

    def describe_when_getting_section_activities() -> None:
        def it_should_return_an_empty_DataFrame(mocker, fixture) -> None:

            df = get_all_section_activities(BASE_DIRECTORY, INPUT_DF)

            assert df.empty

    def describe_when_getting_assignments() -> None:
        def it_should_return_an_empty_DataFrame(mocker, fixture) -> None:

            df = get_all_assignments(BASE_DIRECTORY, INPUT_DF)

            assert df.empty

    def describe_when_getting_submissions() -> None:
        def it_should_return_an_empty_DataFrame(mocker, fixture) -> None:

            df = get_all_submissions(BASE_DIRECTORY, INPUT_DF)

            assert df.empty

    def describe_when_getting_grades() -> None:
        def it_should_return_an_empty_DataFrame(mocker, fixture) -> None:

            df = get_all_grades(BASE_DIRECTORY, INPUT_DF)

            assert df.empty

    def describe_when_getting_attendance_events() -> None:
        def it_should_return_an_empty_DataFrame(mocker, fixture) -> None:

            df = get_all_attendance_events(BASE_DIRECTORY, INPUT_DF)

            assert df.empty


def describe_when_reading_files_from_path():
    @pytest.fixture
    def mock_read_csv(mocker):
        read_csv_mock = Mock(spec=_read_csv)
        mocker.patch("edfi_lms_file_utils.file_reader._read_csv", read_csv_mock)
        return read_csv_mock

    def describe_when_getting_files_with_specific_types():
        def describe_given_resource_name_is_user():
            def it_should_define_correct_data_type_to_read_csv_method(
                mock_read_csv: Mock,
            ):
                read_users_file("")
                assert mock_read_csv.call_args_list[0][0][2] == DataTypes.USERS

        def describe_given_resource_name_is_sections():
            def it_should_define_correct_data_type_to_read_csv_method(
                mock_read_csv: Mock,
            ):
                read_sections_file("")
                assert mock_read_csv.call_args_list[0][0][2] == DataTypes.SECTIONS

    def describe_when_getting_general_files():
        methods_to_test: List[Callable] = [
            read_system_activities_file,
            read_section_associations_file,
            read_section_activities_file,
            read_assignments_file,
            read_submissions_file,
            read_grades_file,
            read_attendance_events_file,
        ]

        def it_should_call_read_csv_method(mock_read_csv: Mock):
            for count in range(len(methods_to_test)):
                methods_to_test[count]("")
            assert mock_read_csv.call_count == len(methods_to_test)
