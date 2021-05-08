# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Features:
    Activities = "activities"
    Attendance = "attendance"
    Assignments = "assignments"
    Grades = "grades"  # not implemented yet


VALID_FEATURES = [
    Features.Activities,
    Features.Attendance,
    Features.Assignments,
    Features.Grades,
]
