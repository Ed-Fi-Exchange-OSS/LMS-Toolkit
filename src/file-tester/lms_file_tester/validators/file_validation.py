# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os
import sys
from typing import List

# The following is a hack to load a local package above this package's base
# directory, so that this test utility does not need to rely on downloading a
# published version of the LMS file utils.
sys.path.append(os.path.join("..", "file-utils"))
from lms_file_utils import file_reader as fread  # type: ignore # noqa: E402


def validate_users_file(input_directory: str) -> List[str]:
    # Get the latest file
    # Read only the top 1 row
    # Check that only the expected columns are present

    df = fread.get_all_users(input_directory, nrows=1)

    expected = set(
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "UserRole",
            "LocalUserIdentifier",
            "SISUserIdentifier",
            "Name",
            "EmailAddress",
            "EntityStatus",
            "CreateDate",
            "LastModifiedDate",
        ]
    )

    actual = set(df.columns)

    if actual == expected:
        return list()

    extra = actual.difference(expected)
    missing = expected.difference(extra)

    return [
        f"Users file contains extra columns {extra} and is missing columns {missing}"
    ]
