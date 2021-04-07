# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class DbEngine:
    MSSQL = "mssql"
    POSTGRESQL = "postgresql"


class Table:
    USER = "LMSUser"
    SECTION = "LMSSection"
    ASSIGNMENT = "Assignment"
    ASSIGNMENT_SUBMISSION_TYPES = "AssignmentSubmissionType"
    ASSIGNMENT_SUBMISSION = "AssignmentSubmission"
    SECTION_ASSOCIATION = "LMSUserLMSSectionAssociation"
    SECTION_ACTIVITY = "LMSSectionActivity"
    SYSTEM_ACTIVITY = "LMSSystemActivity"
    ATTENDANCE = "LMSUserAttendanceEvent"
