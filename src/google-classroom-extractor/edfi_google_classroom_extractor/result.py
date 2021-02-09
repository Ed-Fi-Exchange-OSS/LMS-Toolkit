# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from collections import namedtuple

Result = namedtuple(
    "Result",
    [
        "usage_df",
        "courses_df",
        "coursework_df",
        "submissions_df",
        "students_df",
        "teachers_df",
    ],
)
