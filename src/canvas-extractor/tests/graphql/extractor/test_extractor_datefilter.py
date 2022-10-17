# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from edfi_canvas_extractor.graphql.utils import validate_date


def test_graphql_request(api):
    # start = "2021-01-01"
    # end = "2030-01-01"

    courses = api["data"]["account"]["coursesConnection"]["nodes"][0]

    for course in courses["term"]["coursesConnection"]["nodes"]:
        if course["state"] not in ["available", "completed"]:
            continue

        start_term = courses["term"]["startAt"]
        end_term = courses["term"]["endAt"]

        assert start_term is None
        assert end_term is None


@pytest.mark.xfail
@pytest.mark.parametrize("date", ["", None, False])
def test_validate_date_value(date):
    assert date is True


@pytest.mark.xfail
@pytest.mark.parametrize("start_a, end_a, start_b, end_b", [
    (None, None, None, None),
    ("2021-01-01", "2030-01-01", None, None),
])
def test_validate_date(start_a, end_a, start_b, end_b):
    assert validate_date(start_a, end_a, start_b, end_b) is True
