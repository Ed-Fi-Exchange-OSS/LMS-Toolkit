# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

Feature: AssignmentDim View
    As a data analyst,
    I want to denormalize LMS Assignment data,
    so that I can build reports on student engagement.

    Background:
        Given Analytics Middle Tier has been installed
        And there is a school with id 53
        And the school year is 1053
        And school 53 has a session called "Summer-1053" in year 1053
        And there is a section
            | LocalCourseCode   | abc-1053    |
            | SchoolId          | 53          |
            | SchoolYear        | 1053        |
            | SectionIdentifier | si-1053     |
            | SessionName       | Summer-1053 |
        And there is a grading period
            | Descriptor             | First summer session 1053 |
            | PeriodSequence         | 3                         |
            | SchoolId               | 53                        |
            | SchoolYear             | 1053                      |
            | TotalInstructionalDays | 1053                      |
            | BeginDate              | 1053-07-01 01:23:45       |
            | EndDate                | 1053-07-29 01:23:45       |
        And edfi.SessionGradingPeriod table is populated


    Scenario: Ensure the view exists
        When I query for assignments with identifier "this-row-doesnt-exist"
        Then it has these columns:
            | Columns          |
            | AssignmentKey    |
            | SchoolKey        |
            | SourceSystem     |
            | Title            |
            | Description      |
            | StartDateKey     |
            | EndDateKey       |
            | DueDateKey       |
            | MaxPoints        |
            | SectionKey       |
            | GradingPeriodKey |
            | LastModifiedDate |

    Scenario: Happy Path
        Given there is one Assignment
            | AssignmentIdentifier  | assigndim-happy-path  |
            | Namespace             | test-namespace        |
            | SchoolId              | 53                    |
            | SourceSystem          | Schoology             |
            | Title                 | A discussion for 1053 |
            | AssignmentDescription | The description       |
            | StartDateTime         | 1053-07-08 09:00      |
            | EndDateTime           | 1053-07-09 10:00      |
            | DueDateTime           | 1053-07-09 10:11      |
            | MaxPoints             | 99                    |
            | SectionIdentifier     | si-1053               |
            | LastModifiedDate      | 1053-07-07 09:01      |
            | AssignmentCategory    | Assignment            |
            | LocalCourseCode       | abc-1053              |
            | SessionName           | Summer-1053           |
            | SchoolYear            | 1053                  |
        When I query for assignments with identifier "assigndim-happy-path"
        Then there should be 1 records
        And the AssignmentDim record should have these values:
            | AssignmentKey    | assigndim-happy-path                 |
            | SchoolKey        | 53                                   |
            | SourceSystem     | Schoology                            |
            | Title            | A discussion for 1053                |
            | Description      | The description                      |
            | StartDateKey     | 10530708                             |
            | EndDateKey       | 10530709                             |
            | DueDateKey       | 10530709                             |
            | MaxPoints        | 99                                   |
            | SectionKey       | 53-abc-1053-1053-si-1053-Summer-1053 |
            | GradingPeriodKey | r"[0-9]+-53-10530701"                |
            | LastModifiedDate | r"\d{4}-\d{2}-\d{2}"                 |


    Scenario: Ignores discussions
        Given there is one Assignment
            | AssignmentIdentifier  | ignore-discussion     |
            | Namespace             | test-namespace        |
            | SchoolId              | 53                    |
            | SourceSystem          | Schoology             |
            | Title                 | A discussion for 1053 |
            | AssignmentDescription | The description       |
            | StartDateTime         | 1053-07-08 09:00      |
            | EndDateTime           | 1053-07-09 10:00      |
            | DueDateTime           | 1053-07-09 10:11      |
            | MaxPoints             | 99                    |
            | SectionIdentifier     | si-1053               |
            | LastModifiedDate      | 1053-07-07 09:01      |
            | AssignmentCategory    | discussion            |
            | LocalCourseCode       | abc-1053              |
            | SessionName           | Summer-1053           |
            | SchoolYear            | 1053                  |
        And there is one Assignment
            | AssignmentIdentifier  | ignore-2                                |
            | Namespace             | test-namespace                          |
            | SchoolId              | 53                                      |
            | SourceSystem          | Schoology                               |
            | Title                 | A COURSE_WORK_TYPE_UNSPECIFIED for 1053 |
            | AssignmentDescription | The description                         |
            | StartDateTime         | 1053-07-08 09:00                        |
            | EndDateTime           | 1053-07-09 10:00                        |
            | DueDateTime           | 1053-07-09 10:11                        |
            | MaxPoints             | 99                                      |
            | SectionIdentifier     | si-1053                                 |
            | LastModifiedDate      | 1053-07-07 09:01                        |
            | AssignmentCategory    | COURSE_WORK_TYPE_UNSPECIFIED            |
            | LocalCourseCode       | abc-1053                                |
            | SessionName           | Summer-1053                             |
            | SchoolYear            | 1053                                    |
        And there is one Assignment
            | AssignmentIdentifier  | ignore-3                |
            | Namespace             | test-namespace          |
            | SchoolId              | 53                      |
            | SourceSystem          | Schoology               |
            | Title                 | A discussion for 1053   |
            | AssignmentDescription | The description         |
            | StartDateTime         | 1053-07-08 09:00        |
            | EndDateTime           | 1053-07-09 10:00        |
            | DueDateTime           | 1053-07-09 10:11        |
            | MaxPoints             | 99                      |
            | SectionIdentifier     | si-1053                 |
            | LastModifiedDate      | 1053-07-07 09:01        |
            | AssignmentCategory    | SHORT_ANSWER_QUESTION   |
            | LocalCourseCode       | abc-1053                |
            | SessionName           | Summer-1053             |
            | SchoolYear            | 1053                    |
        And there is one Assignment
            | AssignmentIdentifier  | ignore-4                 |
            | Namespace             | test-namespace           |
            | SchoolId              | 53                       |
            | SourceSystem          | Schoology                |
            | Title                 | A discussion for 1053    |
            | AssignmentDescription | The description          |
            | StartDateTime         | 1053-07-08 09:00         |
            | EndDateTime           | 1053-07-09 10:00         |
            | DueDateTime           | 1053-07-09 10:11         |
            | MaxPoints             | 99                       |
            | SectionIdentifier     | si-1053                  |
            | LastModifiedDate      | 1053-07-07 09:01         |
            | AssignmentCategory    | MULTIPLE_CHOICE_QUESTION |
            | LocalCourseCode       | abc-1053                 |
            | SessionName           | Summer-1053              |
            | SchoolYear            | 1053                     |
        When I query for assignments with identifier "ignore-discussion"
        Then there should be 0 records
        When I query for assignments with identifier "ignore-2"
        Then there should be 0 records
        When I query for assignments with identifier "ignore-3"
        Then there should be 0 records
        When I query for assignments with identifier "ignore-4"
        Then there should be 0 records
