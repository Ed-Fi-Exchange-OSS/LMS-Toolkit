# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest


from lms_file_tester.validators import directory_validation as drval


INPUT_DIR = "input_dir"
SECTION_ID = "1234"
ASSIGNMENT_ID = "2346"


@pytest.fixture
def fixture(fs):
    # Fake as Linux so that all slashes in these test are forward
    fs.path_separator = "/"
    fs.is_windows_fs = False
    fs.is_macos = False


def describe_when_validating_basic_directories():
    def describe_given_input_directory_does_not_exist():
        def it_should_report_an_error():
            result = drval.validate_base_directory_structure(INPUT_DIR)

            assert result[0] == f"Missing directory: {INPUT_DIR}"

    def describe_given_the_input_dir_exists():
        @pytest.fixture
        def inner_fixture(fs, fixture):
            # Create all of the base directories. Will remove them one-by-one to
            # test the response for when the dir is missing.
            fs.create_dir(INPUT_DIR)
            fs.create_dir(f"{INPUT_DIR}/users")
            fs.create_dir(f"{INPUT_DIR}/sections")

        def describe_given_all_directories_exist():
            def it_should_not_return_any_errors(fs, fixture, inner_fixture):
                result = drval.validate_base_directory_structure(INPUT_DIR)

                assert len(result) == 0

        def describe_given_users_is_missing():
            def it_should_report_one_error(fs, fixture, inner_fixture):
                fs.remove_object(f"{INPUT_DIR}/users")

                result = drval.validate_base_directory_structure(INPUT_DIR)

                assert result[0] == f"Missing directory: {INPUT_DIR}/users"

        def describe_given_sections_is_missing():
            def it_should_report_one_error(fs, fixture, inner_fixture):
                fs.remove_object(f"{INPUT_DIR}/sections")

                result = drval.validate_base_directory_structure(INPUT_DIR)

                assert result[0] == f"Missing directory: {INPUT_DIR}/sections"


def describe_when_validating_section_directories():
    def describe_given_input_directory_does_not_exist():
        def it_should_report_an_error():
            result = drval.validate_section_directory_structure(INPUT_DIR, SECTION_ID)

            assert result[0] == f"Missing directory: {INPUT_DIR}"

    def describe_given_the_input_dir_exists():
        @pytest.fixture
        def inner_fixture(fs, fixture):
            # Create all of the base directories. Will remove them one-by-one to
            # test the response for when the dir is missing.
            fs.create_dir(INPUT_DIR)
            fs.create_dir(f"{INPUT_DIR}/section={SECTION_ID}")
            fs.create_dir(f"{INPUT_DIR}/section={SECTION_ID}/assignments")
            fs.create_dir(f"{INPUT_DIR}/section={SECTION_ID}/assignment=2345/submissions")
            fs.create_dir(f"{INPUT_DIR}/section={SECTION_ID}/attendance-events")
            fs.create_dir(f"{INPUT_DIR}/section={SECTION_ID}/grades")
            fs.create_dir(f"{INPUT_DIR}/section={SECTION_ID}/section-activities")
            fs.create_dir(f"{INPUT_DIR}/section={SECTION_ID}/section-associations")

        def describe_given_all_directories_exist():
            def it_should_not_return_any_errors(fs, fixture, inner_fixture):
                result = drval.validate_section_directory_structure(INPUT_DIR, SECTION_ID)

                assert len(result) == 0

        def describe_given_assignments_is_missing():
            def it_should_report_one_error(fs, fixture, inner_fixture):
                dir = f"{INPUT_DIR}/section={SECTION_ID}/assignments"
                fs.remove_object(dir)

                result = drval.validate_section_directory_structure(INPUT_DIR, SECTION_ID)

                assert result[0] == f"Missing directory: {dir}"

        def describe_given_attendance_is_missing():
            # This one is non-standard because only Schoology writes out an attendance record
            def it_should_not_report_an_error(fs, fixture, inner_fixture):
                dir = f"{INPUT_DIR}/section={SECTION_ID}/attendance-events"
                fs.remove_object(dir)

                result = drval.validate_section_directory_structure(INPUT_DIR, SECTION_ID)

                assert len(result) == 0

        def describe_given_section_activities_is_missing():
            def it_should_report_one_error(fs, fixture, inner_fixture):
                dir = f"{INPUT_DIR}/section={SECTION_ID}/section-activities"
                fs.remove_object(dir)

                result = drval.validate_section_directory_structure(INPUT_DIR, SECTION_ID)

                assert result[0] == f"Missing directory: {dir}"

        def describe_given_grades_is_missing():
            def it_should_report_one_error(fs, fixture, inner_fixture):
                dir = f"{INPUT_DIR}/section={SECTION_ID}/grades"
                fs.remove_object(dir)

                result = drval.validate_section_directory_structure(INPUT_DIR, SECTION_ID)

                assert result[0] == f"Missing directory: {dir}"

        def describe_given_section_associations_is_missing():
            def it_should_report_one_error(fs, fixture, inner_fixture):
                dir = f"{INPUT_DIR}/section={SECTION_ID}/section-associations"
                fs.remove_object(dir)

                result = drval.validate_section_directory_structure(INPUT_DIR, SECTION_ID)

                assert result[0] == f"Missing directory: {dir}"


def describe_when_validating_assignment_directories():
    def describe_given_assignment_directory_does_not_exist():
        def it_should_report_an_error(fs, fixture):
            result = drval.validate_assignment_directory_structure(INPUT_DIR, SECTION_ID, ASSIGNMENT_ID)

            exp = f"Missing directory: {INPUT_DIR}/section={SECTION_ID}"
            assert result[0] == exp

    def describe_given_the_assignment_dir_exists():
        def describe_given_submissions_dir_does_not_exists():
            def it_should_report_an_error(fs, fixture):
                # Arrange
                exp = f"{INPUT_DIR}/section={SECTION_ID}/assignment={ASSIGNMENT_ID}"
                fs.create_dir(exp)

                # Act
                result = drval.validate_assignment_directory_structure(INPUT_DIR, SECTION_ID, ASSIGNMENT_ID)

                # Assert
                exp = f"Missing directory: {exp}/submissions"
                assert result[0] == exp

        def describe_given_submissions_dir_exists():
            def it_should_not_return_any_errors(fs, fixture):
                # Arrange
                fs.create_dir(f"{INPUT_DIR}/section={SECTION_ID}/assignment={ASSIGNMENT_ID}/submissions")

                # Act
                result = drval.validate_assignment_directory_structure(INPUT_DIR, SECTION_ID, ASSIGNMENT_ID)

                # Assert
                assert len(result) == 0


def describe_when_validating_system_activities():
    def describe_given_system_activities_directory_does_not_exist():
        def it_should_report_an_error(fs, fixture):
            result = drval.validate_system_activities_directory_structure(INPUT_DIR)

            assert result[0] == f"Missing directory: {INPUT_DIR}/system-activities"

    def describe_given_contains_valid_sub_directory():
        def it_should_not_report_any_errors(fs, fixture):
            fs.create_dir(f"{INPUT_DIR}/system-activities")
            fs.create_dir(f"{INPUT_DIR}/system-activities/date=2020-12-01")

            result = drval.validate_system_activities_directory_structure(INPUT_DIR)

            assert len(result) == 0

    def describe_given_contains_no_sub_directories():
        def it_should_report_an_error(fs, fixture):
            fs.create_dir(f"{INPUT_DIR}/system-activities")

            result = drval.validate_system_activities_directory_structure(INPUT_DIR)

            assert len(result) == 1
            assert result[0] == "System activities directory does not contain any date-based sub-directories"

    def describe_given_contains_only_invalid_sub_directories():
        def it_should_report_an_error(fs, fixture):
            fs.create_dir(f"{INPUT_DIR}/system-activities")
            fs.create_dir(f"{INPUT_DIR}/system-activities/something")
            fs.create_dir(f"{INPUT_DIR}/system-activities/date=")
            fs.create_dir(f"{INPUT_DIR}/system-activities/ate=2020-12-01")

            result = drval.validate_system_activities_directory_structure(INPUT_DIR)

            assert len(result) == 1
            assert result[0] == "System activities directory does not contain any date-based sub-directories"
