# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

Feature: AssignmentSubmissionFact View
    As a data analyst,
    I want to know the status of student Assignment submissions,
    so that I can build reports on student engagement.

    Background:
        Given Analytics Middle Tier has been installed
        And there is a school with id 54
        And the school year is 1054
        And school 54 has a session called "Summer-1054" in year 1054
        And there is a section
            | LocalCourseCode   | abc-1054    |
            | SchoolId          | 54          |
            | SchoolYear        | 1054        |
            | SectionIdentifier | si-1054     |
            | SessionName       | Summer-1054 |
        And there is a grading period
            | Descriptor             | First summer session 1054 |
            | PeriodSequence         | 4                         |
            | SchoolId               | 54                        |
            | SchoolYear             | 1054                      |
            | TotalInstructionalDays | 1054                      |
            | BeginDate              | 1054-07-01 01:23:45       |
            | EndDate                | 1054-07-01 01:23:45       |
        And there is one Assignment
            | AssignmentIdentifier | AssignmentSubmissionFact |
            | SchoolId             | 54                       |
            | SourceSystem         | Canvas                   |
            | Title                | A discussion for 1054    |
            | Description          | The description          |
            | StartDateTime        | 1054-07-08 09:00         |
            | EndDateTime          | 1054-07-09 10:00         |
            | DueDateTime          | 1054-07-09 10:11         |
            | MaxPoints            | 98                       |
            | SectionIdentifier    | si-1054                  |
            | LastModifiedDate     | 1054-07-07 09:01         |
            | AssignmentCategory   | Assignment               |
        And there is a student
            | StudentUniqueId  | first-student |
            | FirstName        | Ebenezer      |
            | LastSurname      | Scrooge       |
            | Birthdate        | 1843-12-19    |
            | LastModifiedDate | 1843-12-20    |
        And student "first-student" is enrolled at school 54
        And student "first-student" is enrolled in section abc-1054


    Scenario: Ensure the view exists
        When I query for assignments submissions for student 1234 at school 54
        Then it has these columns:
            | Columns                 |
            | AssignmentSubmissionKey |
            | StudentSchoolKey        |
            | SchoolKey               |
            | StudentKey              |
            | SectionKey              |
            | AssignmentKey           |
            | SubmissionDateKey       |
            | EarnedPoints            |
            | NumericGrade            |
            | LetterGrade             |
            | IsPastDue               |
            | SubmittedLate           |
            | SubmittedOnTime         |
            | LastModifiedDate        |

    Scenario: On Time Happy Path
        Given student "first-student" has an assignment submission
            | AssignmentSubmissionIdentifier | on-time-happy-path       |
            | AssignmentIdentifier           | AssignmentSubmissionFact |
            | SchoolId                       | 54                       |
            | SubmissionStatus               | on-time                  |
            | SubmissionDateTime             | 1054-07-09 9:12:34       |
            | EarnedPoints                   | 90                       |
            | Grade                          | A--                      |
            | LastModifiedDate               | 1054-07-09 9:12:34       |
        When I query for assignment submission "on-time-happy-path"
        Then there should be 1 submission
        And the submission record should have these values:
            | AssignmentSubmissionKey | on-time-happy-path                   |
            | StudentSchoolKey        | first-student-54                     |
            | SchoolKey               | 54                                   |
            | StudentKey              | first-student                        |
            | SectionKey              | 54-abc-1054-1054-si-1504-Summer-1054 |
            | AssignmentKey           | AssignmentSubmissionFact             |
            | SubmissionDateKey       | 1054-07-09                           |
            | EarnedPoints            | 90                                   |
            | NumericGrade            | 91                                   |
            | LetterGrade             | A--                                  |
            | IsPastDue               | 0                                    |
            | SubmittedLate           | 0                                    |
            | SubmittedOnTime         | 1                                    |
            | LastModifiedDate        | 054-07-09 9:12:34                    |
