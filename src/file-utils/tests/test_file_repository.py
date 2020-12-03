# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from lms_file_utils.file_repository import (
    get_users_file,
    get_sections_file,
    get_section_associations_file,
    get_section_activities_file,
    get_assignments_file,
    get_grades_file,
    get_attendance_events_file,
    get_submissions_file,
    get_system_activities_files,
)


BASE_DIRECTORY = "base_dir"
SECTION_ID = 1
ASSIGNMENT_ID = 2

SECTION_FILE_OLD = f"{BASE_DIRECTORY}/sections/2020-11-18-04-05-06.csv"
SECTION_FILE_NEW = f"{BASE_DIRECTORY}/sections/2020-11-19-04-05-06.csv"
USERS_FILE_OLD = f"{BASE_DIRECTORY}/users/2020-11-18-04-05-06.csv"
USERS_FILE_NEW = f"{BASE_DIRECTORY}/users/2020-11-19-04-05-06.csv"
ASSIGNMENTS_FILE_OLD = f"{BASE_DIRECTORY}/section=1/assignments/2020-11-18-04-05-06.csv"
ASSIGNMENTS_FILE_NEW = f"{BASE_DIRECTORY}/section=1/assignments/2020-11-19-04-05-06.csv"
ASSOCIATIONS_FILE_OLD = (
    f"{BASE_DIRECTORY}/section=1/section-associations/2020-11-18-04-05-06.csv"
)
ASSOCIATIONS_FILE_NEW = (
    f"{BASE_DIRECTORY}/section=1/section-associations/2020-11-19-04-05-06.csv"
)
GRADES_FILE_OLD = f"{BASE_DIRECTORY}/section=1/grades/2020-11-18-04-05-06.csv"
GRADES_FILE_NEW = f"{BASE_DIRECTORY}/section=1/grades/2020-11-19-04-05-06.csv"
SUBMISSIONS_FILE_OLD = (
    f"{BASE_DIRECTORY}/section=1/assignment=2/submissions/2020-11-18-04-05-06.csv"
)
SUBMISSIONS_FILE_NEW = (
    f"{BASE_DIRECTORY}/section=1/assignment=2/submissions/2020-11-19-04-05-06.csv"
)
ATTENDANCE_FILE_OLD = f"{BASE_DIRECTORY}/section=1/attendance-events/2020-11-18-04-05-06.csv"
ATTENDANCE_FILE_NEW = f"{BASE_DIRECTORY}/section=1/attendance-events/2020-11-19-04-05-06.csv"
SECTION_ACTIVITIES_FILE_OLD = (
    f"{BASE_DIRECTORY}/section=1/section-activities/2020-11-18-04-05-06.csv"
)
SECTION_ACTIVITIES_FILE_NEW = (
    f"{BASE_DIRECTORY}/section=1/section-activities/2020-11-19-04-05-06.csv"
)
SYSTEM_ACTIVITIES_FILE_OLD = f"{BASE_DIRECTORY}/system-activities/date=2020-11-17/2020-11-18-04-05-06.csv"
SYSTEM_ACTIVITIES_FILE_NEW_1 = f"{BASE_DIRECTORY}/system-activities/date=2020-11-17/2020-11-19-04-05-06.csv"
SYSTEM_ACTIVITIES_FILE_NEW_2 = f"{BASE_DIRECTORY}/system-activities/date=2020-11-18/2020-11-19-04-05-06.csv"

files = [
    SECTION_FILE_OLD,
    SECTION_FILE_NEW,
    USERS_FILE_OLD,
    USERS_FILE_NEW,
    ASSIGNMENTS_FILE_OLD,
    ASSIGNMENTS_FILE_NEW,
    ASSOCIATIONS_FILE_OLD,
    ASSOCIATIONS_FILE_NEW,
    GRADES_FILE_OLD,
    GRADES_FILE_NEW,
    SUBMISSIONS_FILE_OLD,
    SUBMISSIONS_FILE_NEW,
    ATTENDANCE_FILE_OLD,
    ATTENDANCE_FILE_NEW,
    SECTION_ACTIVITIES_FILE_OLD,
    SECTION_ACTIVITIES_FILE_NEW,
    SYSTEM_ACTIVITIES_FILE_OLD,
    SYSTEM_ACTIVITIES_FILE_NEW_1,
    SYSTEM_ACTIVITIES_FILE_NEW_2,
]


def describe_given_filesystem_does_not_exist():
    @pytest.fixture
    def init_fs():

        # Manually creating this to avoid a strange error: when TeamCity calls
        # the pyfakefs setUp function, it tries to create a base directory entry
        # for C: and encounters a failure. Unable to reproduce manually.
        fs = FakeFilesystem(path_separator='/')
        fs.os = "linux"

    def describe_when_getting_sections_file_file():
        def it_should_return_None(init_fs):
            file = get_sections_file(BASE_DIRECTORY)
            assert file is None

    def describe_when_getting_users_file_file():
        def it_should_return_None(init_fs):
            file = get_users_file(BASE_DIRECTORY)
            assert file is None

    def describe_when_getting_assignments_file():
        def it_should_return_None(init_fs):
            file = get_assignments_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_section_associations_file():
        def it_should_return_None(init_fs):
            file = get_section_associations_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_grades_file():
        def it_should_return_None(init_fs):
            file = get_grades_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_submissions_file():
        def it_should_return_None(init_fs):
            file = get_submissions_file(BASE_DIRECTORY, SECTION_ID, ASSIGNMENT_ID)
            assert file is None

    def describe_when_getting_attendance_events_file():
        def it_should_return_None(init_fs):
            file = get_attendance_events_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_section_activities_file():
        def it_should_return_None(init_fs):
            file = get_section_activities_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_system_activities_files():
        def it_should_return_an_empty_list(init_fs):
            files = get_system_activities_files(BASE_DIRECTORY)
            assert len(files) == 0


def describe_given_filesystem_exists_with_no_files():
    @pytest.fixture
    def init_fs():

        # Manually creating this to avoid a strange error: when TeamCity calls
        # the pyfakefs setUp function, it tries to create a base directory entry
        # for C: and encounters a failure. Unable to reproduce manually.
        fs = FakeFilesystem(path_separator='/')
        fs.os = "linux"

        fs.create_dir(f"{BASE_DIRECTORY}/section={SECTION_ID}/assignments")
        f = f"{BASE_DIRECTORY}/section={SECTION_ID}/ASSIGNMENT={ASSIGNMENT_ID}/submissions"
        fs.create_dir(f)
        fs.create_dir(f"{BASE_DIRECTORY}/section={SECTION_ID}/attendance-events")
        fs.create_dir(f"{BASE_DIRECTORY}/section={SECTION_ID}/grades")
        fs.create_dir(f"{BASE_DIRECTORY}/section={SECTION_ID}/section-associations")
        fs.create_dir(f"{BASE_DIRECTORY}/section={SECTION_ID}/section-activities")
        fs.create_dir(f"{BASE_DIRECTORY}/system-activities/date=2020-11-17")
        fs.create_dir(f"{BASE_DIRECTORY}/system-activities/date=2020-11-18")
        fs.create_dir(f"{BASE_DIRECTORY}/users")

    def describe_when_getting_sections_file_file():
        def it_should_return_None(init_fs):
            file = get_sections_file(BASE_DIRECTORY)
            assert file is None

    def describe_when_getting_users_file_file():
        def it_should_return_None(init_fs):
            file = get_users_file(BASE_DIRECTORY)
            assert file is None

    def describe_when_getting_assignments_file():
        def it_should_return_None(init_fs):
            file = get_assignments_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_section_associations_file():
        def it_should_return_None(init_fs):
            file = get_section_associations_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_grades_file():
        def it_should_return_None(init_fs):
            file = get_grades_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_submissions_file():
        def it_should_return_None(init_fs):
            file = get_submissions_file(BASE_DIRECTORY, SECTION_ID, ASSIGNMENT_ID)
            assert file is None

    def describe_when_getting_attendance_events_file():
        def it_should_return_None(init_fs):
            file = get_attendance_events_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_section_activities_file():
        def it_should_return_None(init_fs):
            file = get_section_activities_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_system_activities_file():
        def it_should_return_an_empty_list(init_fs):
            file = get_system_activities_files(BASE_DIRECTORY)
            assert len(file) == 0


def describe_given_files_exist():
    @pytest.fixture
    def init_fs():

        # Manually creating this to avoid a strange error: when TeamCity calls
        # the pyfakefs setUp function, it tries to create a base directory entry
        # for C: and encounters a failure. Unable to reproduce manually.
        fs = FakeFilesystem(path_separator='/')
        fs.os = "linux"

        for f in files:
            fs.create_file(f)

    def describe_when_getting_sections_file_file():
        def it_should_return_newest_file(init_fs):
            file = get_sections_file(BASE_DIRECTORY)
            assert file == SECTION_FILE_NEW

    def describe_when_getting_users_file_file():
        def it_should_return_newest_file(init_fs):
            file = get_users_file(BASE_DIRECTORY)
            assert file == USERS_FILE_NEW

    def describe_when_getting_assignments_file():
        def it_should_return_newest_file(init_fs):
            file = get_assignments_file(BASE_DIRECTORY, SECTION_ID)
            assert file == ASSIGNMENTS_FILE_NEW

    def describe_when_getting_section_associations_file():
        def it_should_return_newest_file(init_fs):
            file = get_section_associations_file(BASE_DIRECTORY, SECTION_ID)
            assert file == ASSOCIATIONS_FILE_NEW

    def describe_when_getting_grades_file():
        def it_should_return_newest_file(init_fs):
            file = get_grades_file(BASE_DIRECTORY, SECTION_ID)
            assert file == GRADES_FILE_NEW

    def describe_when_getting_submissions_file():
        def it_should_return_newest_file(init_fs):
            file = get_submissions_file(BASE_DIRECTORY, SECTION_ID, ASSIGNMENT_ID)
            assert file == SUBMISSIONS_FILE_NEW

    def describe_when_getting_attendance_events_file():
        def it_should_return_newest_file(init_fs):
            file = get_attendance_events_file(BASE_DIRECTORY, SECTION_ID)
            assert file == ATTENDANCE_FILE_NEW

    def describe_when_getting_section_activities_file():
        def it_should_return_newest_file(init_fs):
            file = get_section_activities_file(BASE_DIRECTORY, SECTION_ID)
            assert file == SECTION_ACTIVITIES_FILE_NEW

    def describe_when_getting_system_activities_files():
        def it_return_newest_file_from_day_one(init_fs):
            files = get_system_activities_files(BASE_DIRECTORY)
            assert SYSTEM_ACTIVITIES_FILE_NEW_1 in files

        def it_return_newest_file_from_day_two(init_fs):
            files = get_system_activities_files(BASE_DIRECTORY)
            assert SYSTEM_ACTIVITIES_FILE_NEW_2 in files
