# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


import pytest

from edfi_lms_file_utils.file_repository import (
    get_users_file,
    get_sections_file,
    get_section_associations_file,
    get_section_activities_file,
    get_assignments_file,
    get_grades_file,
    get_attendance_events_file,
    get_submissions_file,
    get_system_activities_files,
    _get_newest_file,
)


BASE_DIRECTORY = "base_dir"
SECTION_ID = 1
ASSIGNMENT_ID = 2

SECTION_FILE_OLD = "base_dir/sections/2020-11-18-04-05-06.csv"
SECTION_FILE_NEW = "base_dir/sections/2020-11-19-04-05-06.csv"
USERS_FILE_OLD = "base_dir/users/2020-11-18-04-05-06.csv"
USERS_FILE_NEW = "base_dir/users/2020-11-19-04-05-06.csv"
ASSIGNMENTS_FILE_OLD = "base_dir/section=1/assignments/2020-11-18-04-05-06.csv"
ASSIGNMENTS_FILE_NEW = "base_dir/section=1/assignments/2020-11-19-04-05-06.csv"
ASSOCIATIONS_FILE_OLD = (
    "base_dir/section=1/section-associations/2020-11-18-04-05-06.csv"
)
ASSOCIATIONS_FILE_NEW = (
    "base_dir/section=1/section-associations/2020-11-19-04-05-06.csv"
)
GRADES_FILE_OLD = "base_dir/section=1/grades/2020-11-18-04-05-06.csv"
GRADES_FILE_NEW = "base_dir/section=1/grades/2020-11-19-04-05-06.csv"
SUBMISSIONS_FILE_OLD = (
    "base_dir/section=1/assignment=2/submissions/2020-11-18-04-05-06.csv"
)
SUBMISSIONS_FILE_NEW = (
    "base_dir/section=1/assignment=2/submissions/2020-11-19-04-05-06.csv"
)
ATTENDANCE_FILE_OLD = "base_dir/section=1/attendance-events/2020-11-18-04-05-06.csv"
ATTENDANCE_FILE_NEW = "base_dir/section=1/attendance-events/2020-11-19-04-05-06.csv"
SECTION_ACTIVITIES_FILE_OLD = (
    "base_dir/section=1/section-activities/2020-11-18-04-05-06.csv"
)
SECTION_ACTIVITIES_FILE_NEW = (
    "base_dir/section=1/section-activities/2020-11-19-04-05-06.csv"
)
SYSTEM_ACTIVITIES_FILE_OLD = "base_dir/system-activities/date=2020-11-17/2020-11-18-04-05-06.csv"
SYSTEM_ACTIVITIES_FILE_NEW_1 = "base_dir/system-activities/date=2020-11-17/2020-11-19-04-05-06.csv"
SYSTEM_ACTIVITIES_FILE_NEW_2 = "base_dir/system-activities/date=2020-11-18/2020-11-19-04-05-06.csv"

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


@pytest.fixture
def init_fs(fs):
    # Fake as Linux so that all slashes in these test are forward
    fs.os = "linux"
    fs.path_separator = "/"
    fs.is_windows_fs = False
    fs.is_macos = False


def describe_given_filesystem_does_not_exist():

    def describe_when_getting_sections_file_file():
        def it_should_return_None(fs, init_fs):
            file = get_sections_file(BASE_DIRECTORY)
            assert file is None

    def describe_when_getting_users_file_file():
        def it_should_return_None(fs, init_fs):
            file = get_users_file(BASE_DIRECTORY)
            assert file is None

    def describe_when_getting_assignments_file():
        def it_should_return_None(fs, init_fs):
            file = get_assignments_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_section_associations_file():
        def it_should_return_None(fs, init_fs):
            file = get_section_associations_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_grades_file():
        def it_should_return_None(fs, init_fs):
            file = get_grades_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_submissions_file():
        def it_should_return_None(fs, init_fs):
            file = get_submissions_file(BASE_DIRECTORY, SECTION_ID, ASSIGNMENT_ID)
            assert file is None

    def describe_when_getting_attendance_events_file():
        def it_should_return_None(fs, init_fs):
            file = get_attendance_events_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_section_activities_file():
        def it_should_return_None(fs, init_fs):
            file = get_section_activities_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_system_activities_files():
        def it_should_return_an_empty_list(fs, init_fs):
            files = get_system_activities_files(BASE_DIRECTORY)
            assert len(files) == 0


def describe_given_filesystem_exists_with_no_files():
    @pytest.fixture
    def init_fs(init_fs, fs):
        fs.create_dir(f"{BASE_DIRECTORY}/sections")
        fs.create_dir(f"{BASE_DIRECTORY}/sections/section={SECTION_ID}/assignments")
        fs.create_dir(f"{BASE_DIRECTORY}/sections/section={SECTION_ID}/assignments/ASSIGNMENT={ASSIGNMENT_ID}/submissions")
        fs.create_dir(f"{BASE_DIRECTORY}/sections/section={SECTION_ID}/attendance-events")
        fs.create_dir(f"{BASE_DIRECTORY}/sections/section={SECTION_ID}/grades")
        fs.create_dir(f"{BASE_DIRECTORY}/sections/section={SECTION_ID}/section-associations")
        fs.create_dir(f"{BASE_DIRECTORY}/sections/section={SECTION_ID}/section-activities")
        fs.create_dir(f"{BASE_DIRECTORY}/system-activities/date=2020-11-17")
        fs.create_dir(f"{BASE_DIRECTORY}/system-activities/date=2020-11-18")
        fs.create_dir(f"{BASE_DIRECTORY}/users")

    def describe_when_getting_sections_file_file():
        def it_should_return_None(fs, init_fs):
            file = get_sections_file(BASE_DIRECTORY)
            assert file is None

    def describe_when_getting_users_file_file():
        def it_should_return_None(fs, init_fs):
            file = get_users_file(BASE_DIRECTORY)
            assert file is None

    def describe_when_getting_assignments_file():
        def it_should_return_None(fs, init_fs):
            file = get_assignments_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_section_associations_file():
        def it_should_return_None(fs, init_fs):
            file = get_section_associations_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_grades_file():
        def it_should_return_None(fs, init_fs):
            file = get_grades_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_submissions_file():
        def it_should_return_None(fs, init_fs):
            file = get_submissions_file(BASE_DIRECTORY, SECTION_ID, ASSIGNMENT_ID)
            assert file is None

    def describe_when_getting_attendance_events_file():
        def it_should_return_None(fs, init_fs):
            file = get_attendance_events_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_section_activities_file():
        def it_should_return_None(fs, init_fs):
            file = get_section_activities_file(BASE_DIRECTORY, SECTION_ID)
            assert file is None

    def describe_when_getting_system_activities_file():
        def it_should_return_an_empty_list(fs, init_fs):
            file = get_system_activities_files(BASE_DIRECTORY)
            assert len(file) == 0


def describe_given_files_exist():
    @pytest.fixture
    def init_fs(init_fs, fs):
        # Fake as Linux so that all slashes in these test are forward
        # fs.path_separator = "/"
        # fs.is_windows_fs = False
        # fs.is_macos = False

        for f in files:
            fs.create_file(f, contents="content")

    def describe_when_getting_sections_file_file():
        def it_should_return_newest_file(fs, init_fs):
            file = get_sections_file(BASE_DIRECTORY)
            assert file == SECTION_FILE_NEW

    def describe_when_getting_users_file_file():
        def it_should_return_newest_file(fs, init_fs):
            file = get_users_file(BASE_DIRECTORY)
            assert file == USERS_FILE_NEW

    def describe_when_getting_assignments_file():
        def it_should_return_newest_file(fs, init_fs):
            file = get_assignments_file(BASE_DIRECTORY, SECTION_ID)
            assert file == ASSIGNMENTS_FILE_NEW

    def describe_when_getting_section_associations_file():
        def it_should_return_newest_file(fs, init_fs):
            file = get_section_associations_file(BASE_DIRECTORY, SECTION_ID)
            assert file == ASSOCIATIONS_FILE_NEW

    def describe_when_getting_grades_file():
        def it_should_return_newest_file(fs, init_fs):
            file = get_grades_file(BASE_DIRECTORY, SECTION_ID)
            assert file == GRADES_FILE_NEW

    def describe_when_getting_submissions_file():
        def it_should_return_newest_file(fs, init_fs):
            file = get_submissions_file(BASE_DIRECTORY, SECTION_ID, ASSIGNMENT_ID)
            assert file == SUBMISSIONS_FILE_NEW

    def describe_when_getting_attendance_events_file():
        def it_should_return_newest_file(fs, init_fs):
            file = get_attendance_events_file(BASE_DIRECTORY, SECTION_ID)
            assert file == ATTENDANCE_FILE_NEW

    def describe_when_getting_section_activities_file():
        def it_should_return_newest_file(fs, init_fs):
            file = get_section_activities_file(BASE_DIRECTORY, SECTION_ID)
            assert file == SECTION_ACTIVITIES_FILE_NEW

    def describe_when_getting_system_activities_files():
        def it_return_newest_file_from_day_one(fs, init_fs):
            files = get_system_activities_files(BASE_DIRECTORY)
            assert SYSTEM_ACTIVITIES_FILE_NEW_1 in files

        def it_return_newest_file_from_day_two(fs, init_fs):
            files = get_system_activities_files(BASE_DIRECTORY)
            assert SYSTEM_ACTIVITIES_FILE_NEW_2 in files


def describe_when_getting_newest_file_by_name():
    def describe_given_there_are_no_files():
        def it_returns_None(fs, init_fs):
            directory = "./a"
            fs.create_dir(directory)

            result = _get_newest_file(directory)

            assert result is None

    def describe_given_the_directory_does_not_exist():
        def it_returns_None(fs, init_fs):
            directory = "./a"

            result = _get_newest_file(directory)

            assert result is None

    def describe_given_three_files():
        def describe_given_all_have_contents():
            def it_returns_first_sorted_ascending(fs, init_fs):
                # Arrange
                directory = "./a"
                oldest = "./a/1234-56-78-90-12-34.csv"
                middle = "./a/1234-56-78-90-12-35.csv"
                newest = "./a/1234-56-78-90-13-34.csv"

                fs.create_dir(directory)
                fs.create_file(oldest, contents="content")
                fs.create_file(middle, contents="content")
                fs.create_file(newest, contents="content")

                # Act
                result = _get_newest_file(directory)

                # Assert
                assert result == newest

        def describe_given_only_oldest_has_content():
            def it_returns_oldest_sorted_ascending(fs, init_fs):
                # Arrange
                directory = "./a"
                oldest = "./a/1234-56-78-90-12-34.csv"
                middle = "./a/1234-56-78-90-12-35.csv"
                newest = "./a/1234-56-78-90-13-34.csv"

                fs.create_dir(directory)
                fs.create_file(oldest, contents="content")
                fs.create_file(middle, contents="")
                fs.create_file(newest, contents="")

                # Act
                result = _get_newest_file(directory)

                # Assert
                assert oldest == result

        def describe_given_none_have_content():
            def it_returns_None(fs, init_fs):
                # Arrange
                directory = "./a"
                oldest = "./a/1234-56-78-90-12-34.csv"
                middle = "./a/1234-56-78-90-12-35.csv"
                newest = "./a/1234-56-78-90-13-34.csv"

                fs.create_dir(directory)
                fs.create_file(oldest, contents="")
                fs.create_file(middle, contents="")
                fs.create_file(newest, contents="")

                # Act
                result = _get_newest_file(directory)

                # Assert
                assert result is None

        def describe_given_all_have_only_a_line_break():
            def it_returns_None(fs, init_fs):
                # Arrange
                directory = "./a"
                oldest = "./a/1234-56-78-90-12-34.csv"
                middle = "./a/1234-56-78-90-12-35.csv"
                newest = "./a/1234-56-78-90-13-34.csv"

                fs.create_dir(directory)
                fs.create_file(oldest, contents="\n")
                fs.create_file(middle, contents="\n")
                fs.create_file(newest, contents="\n")

                # Act
                result = _get_newest_file(directory)

                # Assert
                assert result is None

        # Not coding or testing beyond this, because this example represents how
        # Schoology (via pandas write to CSV) is outputting "empty" files.
        def describe_given_all_have_only_two_line_breaks():
            def it_returns_None(fs, init_fs):
                # Arrange
                directory = "./a"
                oldest = "./a/1234-56-78-90-12-34.csv"
                middle = "./a/1234-56-78-90-12-35.csv"
                newest = "./a/1234-56-78-90-13-34.csv"

                fs.create_dir(directory)
                fs.create_file(oldest, contents="\n\n")
                fs.create_file(middle, contents="\n\n")
                fs.create_file(newest, contents="\n\n")

                # Act
                result = _get_newest_file(directory)

                # Assert
                assert result is None
