# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from os import path
from sys import platform


from edfi_lms_extractor_lib.csv_generation.write import (
    _normalized_directory_template,
    USERS_ROOT_DIRECTORY,
    ASSIGNMENT_ROOT_DIRECTORY,
    SUBMISSION_ROOT_DIRECTORY,
)

OUTPUT_DIRECTORY = "output_directory"
OUTPUT_DIRECTORY_WITH_SLASH = "output_directory/"
OUTPUT_DIRECTORY_WITH_BACKSLASH = "output_directory\\"


def describe_when_template_has_one_element():
    EXPECTED_RESULT = f"{OUTPUT_DIRECTORY}{path.sep}{USERS_ROOT_DIRECTORY[0]}"
    BACKSLASH_LINUX = f"{OUTPUT_DIRECTORY}\\{path.sep}{USERS_ROOT_DIRECTORY[0]}"

    def it_should_join_bare_output_directory_correctly():
        # arrange / act
        result = _normalized_directory_template(OUTPUT_DIRECTORY, USERS_ROOT_DIRECTORY)

        # assert
        assert result == EXPECTED_RESULT

    def it_should_join_output_directory_with_slash_correctly():
        # arrange / act
        result = _normalized_directory_template(
            OUTPUT_DIRECTORY_WITH_SLASH, USERS_ROOT_DIRECTORY
        )

        # assert
        assert result == EXPECTED_RESULT

    def it_should_join_output_directory_with_backslash_correctly():
        # arrange / act
        result = _normalized_directory_template(
            OUTPUT_DIRECTORY_WITH_BACKSLASH, USERS_ROOT_DIRECTORY
        )

        # assert
        if platform == "win32":
            assert result == EXPECTED_RESULT
        else:
            assert result == BACKSLASH_LINUX


def describe_when_template_has_two_elements():
    EXPECTED_RESULT = (
        f"{OUTPUT_DIRECTORY}{path.sep}"
        f"{ASSIGNMENT_ROOT_DIRECTORY[0]}{path.sep}"
        f"{ASSIGNMENT_ROOT_DIRECTORY[1]}"
    )

    def it_should_join_bare_output_directory_correctly():
        # arrange / act
        result = _normalized_directory_template(
            OUTPUT_DIRECTORY, ASSIGNMENT_ROOT_DIRECTORY
        )

        # assert
        assert result == EXPECTED_RESULT

    def it_should_join_output_directory_with_slash_correctly():
        # arrange / act
        result = _normalized_directory_template(
            OUTPUT_DIRECTORY_WITH_SLASH, ASSIGNMENT_ROOT_DIRECTORY
        )

        # assert
        assert result == EXPECTED_RESULT


def describe_when_template_has_three_elements():
    EXPECTED_RESULT = (
        f"{OUTPUT_DIRECTORY}{path.sep}"
        f"{SUBMISSION_ROOT_DIRECTORY[0]}{path.sep}"
        f"{SUBMISSION_ROOT_DIRECTORY[1]}{path.sep}"
        f"{SUBMISSION_ROOT_DIRECTORY[2]}"
    )

    def it_should_join_bare_output_directory_correctly():
        # arrange / act
        result = _normalized_directory_template(
            OUTPUT_DIRECTORY, SUBMISSION_ROOT_DIRECTORY
        )

        # assert
        assert result == EXPECTED_RESULT

    def it_should_join_output_directory_with_slash_correctly():
        # arrange / act
        result = _normalized_directory_template(
            OUTPUT_DIRECTORY_WITH_SLASH, SUBMISSION_ROOT_DIRECTORY
        )

        # assert
        assert result == EXPECTED_RESULT
