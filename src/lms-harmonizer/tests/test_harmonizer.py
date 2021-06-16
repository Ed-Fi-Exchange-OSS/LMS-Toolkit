# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Tuple

import pytest
from unittest.mock import MagicMock, patch, Mock
from sqlalchemy.engine.base import Engine

from edfi_lms_harmonizer.harmonizer import run
from edfi_lms_harmonizer.helpers.argparser import MainArguments


def describe_given_not_running_exception_reports() -> None:
    @pytest.fixture
    @patch(
        "edfi_sql_adapter.sql_adapter.Adapter.execute"
    )
    def when_running_the_harmonizer(mock_executor) -> Mock:
        # Arrange
        args = MainArguments("DEBUG", None, "server", "dbname", 2)
        args.build_mssql_adapter_with_integrated_security()

        # Act
        run(args)

        # Prepare for assertions
        return mock_executor

    def it_opens_a_database_connection(when_running_the_harmonizer) -> None:
        mock_executor = when_running_the_harmonizer

        assert mock_executor.called_once()

    # def it_runs_user_harmonization_for_canvas(when_running_the_harmonizer) -> None:
    #     _, mock_execute = when_running_the_harmonizer

    #     print("------------------")
    #     print(mock_execute)
    #     print(mock_execute.return_value)
    #     print(mock_execute.call_args)
    #     print(mock_execute.return_value.call_args)
    #     print(mock_execute.return_value.execute.return_value.call_list)
    #     print("------------------")

    #     # assert mock_connection.return_value.execute.assert_called_once()
