# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
from unittest.mock import Mock
import pytest

from lms_file_utils.file_reader import (
    get_all_users,
    get_all_sections,
    get_all_section_associations,
    get_all_section_activities,
    get_all_system_activities,
    get_all_assignments,
    get_all_submissions,
    get_all_grades,
    get_all_attendance_events
)
from test_file_repository import BASE_DIRECTORY

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
ASSOCIATIONS_FILE = (
    "base_dir/section=1/section-associations/2020-11-19-04-05-06.csv"
)
GRADES_FILE = "base_dir/section=1/grades/2020-11-19-04-05-06.csv"
SUBMISSIONS_FILE = (
    "base_dir/section=1/assignment=2/submissions/2020-11-19-04-05-06.csv"
)
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


def describe_given_files_exist():
    @pytest.fixture
    def system(mocker):

        mocker.patch("lms_file_utils.file_repository.get_users_file", lambda _: USERS_FILE)
        mocker.patch("lms_file_utils.file_repository.get_sections_file", lambda _: SECTIONS_FILE)
        mocker.patch("lms_file_utils.file_repository.get_system_activities_files", lambda _: [SYSTEM_ACTIVITIES_FILE])
        mocker.patch("lms_file_utils.file_repository.get_section_associations_file", lambda _a, _b: ASSOCIATIONS_FILE)
        mocker.patch("lms_file_utils.file_repository.get_section_activities_file", lambda _a, _b: SECTION_ACTIVITIES_FILE)
        mocker.patch("lms_file_utils.file_repository.get_assignments_file", lambda _a, _b: ASSIGNMENTS_FILE)
        mocker.patch("lms_file_utils.file_repository.get_grades_file", lambda _a, _b: GRADES_FILE)
        mocker.patch("lms_file_utils.file_repository.get_submissions_file", lambda _a, _b, _c: SUBMISSIONS_FILE)
        mocker.patch("lms_file_utils.file_repository.get_attendance_events_file", lambda _a, _b: ATTENDANCE_FILE)

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
                ATTENDANCE_FILE: generate_data_frame(ATTENDANCE_EVENTS)
            }
            return switcher.get(file, pd.DataFrame())

        pd.read_csv = Mock(side_effect=_fake_reader)

    def describe_when_getting_users():
        def it_should_read_file_into_DataFrame(mocker, fixture):
            df = get_all_users(BASE_DIRECTORY)

            assert df.iloc[0][USERS] == 1

    def describe_when_getting_section():
        def it_should_read_file_into_DataFrame(mocker, fixture):
            df = get_all_sections(BASE_DIRECTORY)

            assert df.iloc[0][SECTIONS] == 1

    def describe_when_getting_system_activities():
        def it_should_read_file_into_DataFrame(mocker, fixture):
            df = get_all_system_activities(BASE_DIRECTORY)

            assert df.iloc[0][SYSTEM_ACTIVITIES] == 1

    def describe_when_getting_section_associations():
        def it_should_read_file_into_DataFrame(mocker, fixture):

            df = get_all_section_associations(BASE_DIRECTORY, INPUT_DF)

            assert df.iloc[0][SECTION_ASSOCIATIONS] == 1

        def given_empty_section_list_it_should_return_empty_data_frame(mocker, fixture):

            df = get_all_section_associations(BASE_DIRECTORY, pd.DataFrame())

            assert df.empty

    def describe_when_getting_section_activities():
        def it_should_read_file_into_DataFrame(mocker, fixture):

            df = get_all_section_activities(BASE_DIRECTORY, INPUT_DF)

            assert df.iloc[0][SECTION_ACTIVITIES] == 1

        def given_empty_section_list_it_should_return_empty_data_frame(mocker, fixture):

            df = get_all_section_activities(BASE_DIRECTORY, pd.DataFrame())

            assert df.empty

    def describe_when_getting_assignments():
        def it_should_read_file_into_DataFrame(mocker, fixture):

            df = get_all_assignments(BASE_DIRECTORY, INPUT_DF)

            assert df.iloc[0][ASSIGNMENTS] == 1

        def given_empty_section_list_it_should_return_empty_data_frame(mocker, fixture):

            df = get_all_assignments(BASE_DIRECTORY, pd.DataFrame())

            assert df.empty

    def describe_when_getting_submissions():
        def it_should_read_file_into_DataFrame(mocker, fixture):

            df = get_all_submissions(BASE_DIRECTORY, INPUT_DF)

            assert df.iloc[0][SUBMISSIONS] == 1

        def given_empty_assignments_list_it_should_return_empty_data_frame(mocker, fixture):

            df = get_all_submissions(BASE_DIRECTORY, pd.DataFrame())

            assert df.empty

    def describe_when_getting_grades():
        def it_should_read_file_into_DataFrame(mocker, fixture):

            df = get_all_grades(BASE_DIRECTORY, INPUT_DF)

            assert df.iloc[0][GRADES] == 1

        def given_empty_section_list_it_should_return_empty_data_frame(mocker, fixture):

            df = get_all_grades(BASE_DIRECTORY, pd.DataFrame())

            assert df.empty

    def describe_when_getting_attendance_events():
        def it_should_read_file_into_DataFrame(mocker, fixture):

            df = get_all_attendance_events(BASE_DIRECTORY, INPUT_DF)

            assert df.iloc[0][ATTENDANCE_EVENTS] == 1

        def given_empty_section_list_it_should_return_empty_data_frame(mocker, fixture):

            df = get_all_attendance_events(BASE_DIRECTORY, pd.DataFrame())

            assert df.empty


def describe_given_there_are_no_files_to_read():
    @pytest.fixture
    def fixture(mocker):

        mocker.patch("lms_file_utils.file_repository.get_users_file", lambda _: None)
        mocker.patch("lms_file_utils.file_repository.get_sections_file", lambda _: None)
        mocker.patch("lms_file_utils.file_repository.get_system_activities_files", lambda _: None)
        mocker.patch("lms_file_utils.file_repository.get_section_associations_file", lambda _a, _b: None)
        mocker.patch("lms_file_utils.file_repository.get_section_activities_file", lambda _a, _b: None)
        mocker.patch("lms_file_utils.file_repository.get_assignments_file", lambda _a, _b: None)
        mocker.patch("lms_file_utils.file_repository.get_grades_file", lambda _a, _b: None)
        mocker.patch("lms_file_utils.file_repository.get_submissions_file", lambda _a, _b, _c: None)
        mocker.patch("lms_file_utils.file_repository.get_attendance_events_file", lambda _a, _b: None)

    def describe_when_getting_users():
        def it_should_return_an_empty_DataFrame(mocker, fixture):
            df = get_all_users(BASE_DIRECTORY)

            assert df.empty

    def describe_when_getting_section():
        def it_should_return_an_empty_DataFrame(mocker, fixture):
            df = get_all_sections(BASE_DIRECTORY)

            assert df.empty

    def describe_when_getting_system_activities():
        def it_should_return_an_empty_DataFrame(mocker, fixture):
            df = get_all_system_activities(BASE_DIRECTORY)

            assert df.empty

    def describe_when_getting_section_associations():
        def it_should_return_an_empty_DataFrame(mocker, fixture):

            df = get_all_section_associations(BASE_DIRECTORY, INPUT_DF)

            assert df.empty

    def describe_when_getting_section_activities():
        def it_should_return_an_empty_DataFrame(mocker, fixture):

            df = get_all_section_activities(BASE_DIRECTORY, INPUT_DF)

            assert df.empty

    def describe_when_getting_assignments():
        def it_should_return_an_empty_DataFrame(mocker, fixture):

            df = get_all_assignments(BASE_DIRECTORY, INPUT_DF)

            assert df.empty

    def describe_when_getting_submissions():
        def it_should_return_an_empty_DataFrame(mocker, fixture):

            df = get_all_submissions(BASE_DIRECTORY, INPUT_DF)

            assert df.empty

    def describe_when_getting_grades():
        def it_should_return_an_empty_DataFrame(mocker, fixture):

            df = get_all_grades(BASE_DIRECTORY, INPUT_DF)

            assert df.empty

    def describe_when_getting_attendance_events():
        def it_should_return_an_empty_DataFrame(mocker, fixture):

            df = get_all_attendance_events(BASE_DIRECTORY, INPUT_DF)

            assert df.empty
