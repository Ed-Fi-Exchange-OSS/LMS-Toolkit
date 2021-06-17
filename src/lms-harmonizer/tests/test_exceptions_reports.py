# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os

import pandas as pd
import pytest
from unittest.mock import Mock
from unittest import TestCase

from edfi_sql_adapter.sql_adapter import Adapter

from edfi_lms_harmonizer import exceptions_reports


class When_getting_the_summary_report(TestCase):
    # Typically we do not see log messages as critical for unit testing. In this
    # case, the log messages are the entire point and therefore they should be
    # unit tested. Not using pytest-describe here because we need the log
    # context manager in regular pytest.
    def test_given_there_are_no_exceptions_then_it_should_only_log_to_info(
        self,
    ) -> None:
        # Arrange
        adapter = Mock(spec=Adapter)
        adapter.get_int.return_value = 0

        # Act
        with self.assertLogs(level="INFO") as log:
            exceptions_reports.print_summary(adapter)

        assert "There are no unmatched" in str(log.output)

    def test_given_there_is_one_unmatched_section_then_it_should_report_a_warning(
        self,
    ) -> None:
        # Arrange
        adapter = Mock(spec=Adapter)
        adapter.get_int.side_effect = [1, 0]

        # Act
        with self.assertLogs() as log:
            exceptions_reports.print_summary(adapter)

        assert "There are 1 unmatched sections and 0 unmatched users" in str(log.output)

    def test_given_there_is_one_unmatched_user_then_it_should_report_a_warning(
        self,
    ) -> None:
        # Arrange
        adapter = Mock(spec=Adapter)
        adapter.get_int.side_effect = [0, 1]

        # Act
        with self.assertLogs() as log:
            exceptions_reports.print_summary(adapter)

        assert "There are 0 unmatched sections and 1 unmatched users" in str(log.output)


@pytest.fixture
def init_fs(fs):
    # Fake as Linux so that all slashes in these test are forward
    fs.os = "linux"
    fs.path_separator = "/"
    fs.is_windows_fs = False
    fs.is_macos = False


def describe_when_writing_exception_reports() -> None:
    OUTPUT_DIR = "/output_directory"

    @pytest.fixture
    def given_there_are_exceptions(init_fs, fs) -> None:
        # Arrange
        df_users = pd.DataFrame([{"a": 1}])
        df_sections = pd.DataFrame([{"b": 2}])
        pd.read_sql = Mock(side_effect=[df_sections, df_users])

        # Act
        exceptions_reports.create_exception_reports(Mock(), OUTPUT_DIR)

    def it_should_create_the_output_directory(given_there_are_exceptions, fs) -> None:
        assert os.path.exists(OUTPUT_DIR)

    def it_should_create_the_users_directory(given_there_are_exceptions, fs) -> None:
        assert os.path.exists(os.path.join(OUTPUT_DIR, "users"))

    def it_should_have_created_a_users_csv_file(given_there_are_exceptions, fs) -> None:
        files = os.listdir(os.path.join(OUTPUT_DIR, "users"))
        assert len(files) == 1

    def it_should_have_written_the_users_to_the_csv_file(
        given_there_are_exceptions, fs
    ) -> None:
        dir = os.path.join(OUTPUT_DIR, "users")
        files = os.listdir(dir)

        with open(os.path.join(dir, files[0])) as f:
            contents = f.read()
            assert contents == "a\n1\n"

    def it_should_create_the_sections_directory(given_there_are_exceptions, fs) -> None:
        assert os.path.exists(os.path.join(OUTPUT_DIR, "sections"))

    def it_should_have_created_a_sections_csv_file(
        given_there_are_exceptions, fs
    ) -> None:
        files = os.listdir(os.path.join(OUTPUT_DIR, "sections"))
        assert len(files) == 1

    def it_should_have_written_the_sections_to_the_csv_file(
        given_there_are_exceptions, fs
    ) -> None:
        dir = os.path.join(OUTPUT_DIR, "sections")
        files = os.listdir(dir)

        with open(os.path.join(dir, files[0])) as f:
            contents = f.read()
            assert contents == "b\n2\n"
