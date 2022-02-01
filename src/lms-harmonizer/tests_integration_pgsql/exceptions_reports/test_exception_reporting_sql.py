# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from edfi_sql_adapter.sql_adapter import create_postgresql_adapter

from edfi_lms_harmonizer.helpers.constants import DB_ENGINE
from edfi_lms_harmonizer.sql_for_exceptions_report import (
    QUERY_FOR_ASSIGNMENT_CAT_DESCRIPTORS_POSTGRESQL,
    QUERY_FOR_ASSIGNMENT_CAT_DESCRIPTORS_SUMMARY,
    QUERY_FOR_ASSIGNMENT_EXCEPTIONS,
    QUERY_FOR_ASSIGNMENT_SUBMISSION_EXCEPTIONS,
    QUERY_FOR_SECTION_SUMMARY,
    QUERY_FOR_SECTIONS,
    QUERY_FOR_SUBMISSION_STATUS_DESCRIPTORS_POSTGRESQL,
    QUERY_FOR_SUBMISSION_STATUS_DESCRIPTORS_SUMMARY,
    QUERY_FOR_USERS_SUMMARY,
)
from edfi_lms_harmonizer.migrator import Adapter, migrate
from tests_integration_pgsql.pgsql_server_config import PgsqlServerConfig
from tests_integration_pgsql.pgsql_connection import PgsqlConnection, query


def describe_when_printing_summary_report():
    """
    These are quick-and-dirty tests of the SQL statements used for the console
    exception reporting. They directly test the SQL statements instead of trying
    to capture the standard output.
    """

    @pytest.fixture()
    def setup_harmonizer(test_db_config: PgsqlServerConfig):
        adapter = create_postgresql_adapter(
            test_db_config.username,
            test_db_config.password,
            test_db_config.server,
            test_db_config.db_name,
            int(test_db_config.port),
        )

        # In order to test summary printing, must first run the database
        # migrations - otherwise there will not be a view to query.
        migrate(DB_ENGINE.POSTGRESQL, adapter)

        return adapter

    def it_runs_query_for_sections_without_error(
        test_db_config: PgsqlServerConfig, setup_harmonizer: Adapter
    ):
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            query(connection, QUERY_FOR_SECTIONS)

    def it_runs_query_for_section_summary_without_error(
        test_db_config: PgsqlServerConfig, setup_harmonizer: Adapter
    ):
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            query(connection, QUERY_FOR_SECTION_SUMMARY)

    def it_runs_query_for_users_summary_without_error(
        test_db_config: PgsqlServerConfig, setup_harmonizer: Adapter
    ):
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            query(connection, QUERY_FOR_USERS_SUMMARY)

    def it_runs_query_for_assignment_category_descriptors_without_error(
        test_db_config: PgsqlServerConfig, setup_harmonizer: Adapter
    ):
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            query(connection, QUERY_FOR_ASSIGNMENT_CAT_DESCRIPTORS_POSTGRESQL)

    def it_runs_query_for_assignment_category_descriptors_summary_without_error(
        test_db_config: PgsqlServerConfig, setup_harmonizer: Adapter
    ):
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            query(connection, QUERY_FOR_ASSIGNMENT_CAT_DESCRIPTORS_SUMMARY)

    def it_runs_query_for_submission_status_descriptors_without_error(
        test_db_config: PgsqlServerConfig, setup_harmonizer: Adapter
    ):
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            query(connection, QUERY_FOR_SUBMISSION_STATUS_DESCRIPTORS_POSTGRESQL)

    def it_runs_query_for_submission_status_descriptors_summary_without_error(
        test_db_config: PgsqlServerConfig, setup_harmonizer: Adapter
    ):
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            query(connection, QUERY_FOR_SUBMISSION_STATUS_DESCRIPTORS_SUMMARY)

    def it_runs_query_for_assignment_exceptions_without_error(
        test_db_config: PgsqlServerConfig, setup_harmonizer: Adapter
    ):
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            query(connection, QUERY_FOR_ASSIGNMENT_EXCEPTIONS)

    def it_runs_query_for_assignment_submission_exceptions_without_error(
        test_db_config: PgsqlServerConfig, setup_harmonizer: Adapter
    ):
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            query(connection, QUERY_FOR_ASSIGNMENT_SUBMISSION_EXCEPTIONS)
