# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Tuple

import pytest
from unittest.mock import patch, MagicMock

from edfi_sql_adapter.sql_adapter import Adapter

from edfi_lms_harmonizer.harmonizer import harmonize_users


def describe_when_harmonizing_users() -> None:
    @pytest.fixture
    def fixture() -> MagicMock:
        # Arrange
        adapter = MagicMock(spec=Adapter)

        # Act
        harmonize_users(adapter)

        # Prepare for assertions
        return adapter

    def it_makes_one_call_to_the_adapter(fixture) -> None:
        adapter = fixture

        assert adapter.execute.call_count == 1

    def it_runs_user_harmonization_for_canvas(fixture) -> None:
        adapter = fixture

        args = adapter.execute.call_args[0]

        found = False
        for a in args[0]:
            found = found or "harmonize_lmsuser_canvas" in a.sql

        assert found

    def it_runs_user_harmonization_for_google(fixture) -> None:
        adapter = fixture

        args = adapter.execute.call_args[0]

        found = False
        for a in args[0]:
            found = found or "harmonize_lmsuser_google_classroom" in a.sql

        assert found

    def it_runs_user_harmonization_for_schoology(fixture) -> None:
        adapter = fixture

        args = adapter.execute.call_args[0]

        found = False
        for a in args[0]:
            found = found or "harmonize_lmsuser_schoology" in a.sql

        assert found
