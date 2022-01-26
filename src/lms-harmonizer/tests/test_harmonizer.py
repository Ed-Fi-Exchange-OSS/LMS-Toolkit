# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest
from unittest.mock import MagicMock

from edfi_sql_adapter.sql_adapter import Adapter

from edfi_lms_harmonizer.harmonizer import harmonize_assignment_submissions, harmonize_users, harmonize_assignments


def describe_when_harmonizing_users() -> None:
    @pytest.fixture
    def fixture() -> MagicMock:
        # Arrange
        adapter = MagicMock(spec=Adapter)

        # Act
        harmonize_users("mssql", adapter)

        # Prepare for assertions
        return adapter

    def it_makes_one_call_to_the_adapter(fixture) -> None:
        adapter = fixture

        assert adapter.execute.call_count == 1

    def it_runs_user_harmonization_for_canvas(fixture) -> None:
        adapter = fixture

        args = adapter.execute.call_args[0]

        found = False
        for call in args[0]:
            found = found or "harmonize_lmsuser_canvas" in call.sql

        assert found

    def it_runs_user_harmonization_for_google(fixture) -> None:
        adapter = fixture

        args = adapter.execute.call_args[0]

        found = False
        for call in args[0]:
            found = found or "harmonize_lmsuser_google_classroom" in call.sql

        assert found

    def it_runs_user_harmonization_for_schoology(fixture) -> None:
        adapter = fixture

        args = adapter.execute.call_args[0]

        found = False
        for call in args[0]:
            found = found or "harmonize_lmsuser_schoology" in call.sql

        assert found


def describe_when_harmonizing_assignments() -> None:
    @pytest.fixture
    def fixture() -> MagicMock:
        # Arrange
        adapter = MagicMock(spec=Adapter)

        # Act
        harmonize_assignments("postgresql", adapter)

        # Prepare for assertions
        return adapter

    def it_makes_one_call_to_the_adapter(fixture) -> None:
        adapter = fixture

        assert adapter.execute.call_count == 1

    def it_runs_assignments_harmonization(fixture) -> None:
        adapter = fixture

        args = adapter.execute.call_args[0]

        found = False
        for call in args[0]:
            found = found or "harmonize_assignment" in call.sql

        assert found


def describe_when_harmonizing_assignment_submissions() -> None:
    @pytest.fixture
    def fixture() -> MagicMock:
        # Arrange
        adapter = MagicMock(spec=Adapter)

        # Act
        harmonize_assignment_submissions("postgresql", adapter)

        # Prepare for assertions
        return adapter

    def it_runs_assignment_submission_harmonization(fixture) -> None:
        adapter = fixture

        args = adapter.execute.call_args[0]

        found = False
        for call in args[0]:
            found = found or "harmonize_assignment_submissions" in call.sql

        assert found
