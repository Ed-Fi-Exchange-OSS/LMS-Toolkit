# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

# Resources
class Resources:
    ASSIGNMENT = "assignment"
    ASSIGNMENTS = "assignments"
    ATTENDANCE_EVENTS = "attendance-events"
    GRADES = "grades"
    SECTION = "section"
    SECTIONS = "sections"
    SECTION_ASSOCIATIONS = "section-associations"
    SECTION_ACTIVITIES = "section-activities"
    SUBMISSIONS = "submissions"
    SYSTEM_ACTIVITIES = "system-activities"
    USERS = "users"


# Keys
class Keys:
    LMS_SECTION_SOURCE_SYSTEM_IDENTIFIER = "LMSSectionSourceSystemIdentifier"
    SOURCE_SYSTEM_IDENTIFIER = "SourceSystemIdentifier"


# Data types for dataframes

class DataTypes:
    SECTIONS = {
        "SISSectionIdentifier": "string",
        "Title": "string",
        "SectionDescription": "string",
        "Term": "string",
        "Status": "string",
    }
    USERS = {
        "UserRole": "string",
        "SISUserIdentifier": "string",
        "LocalUserIdentifier": "string",
        "Name": "string",
        "EmailAddress": "string"
    }
