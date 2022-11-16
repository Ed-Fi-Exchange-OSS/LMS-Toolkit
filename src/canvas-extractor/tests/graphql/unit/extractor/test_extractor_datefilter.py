# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from edfi_canvas_extractor.graphql.utils import validate_date


def test_validate_date():
    with pytest.raises(TypeError):
        validate_date("2021-01-01", "2030-01-01", None, None)
        validate_date(None, None, None, None)
        validate_date("", "", "", "")
