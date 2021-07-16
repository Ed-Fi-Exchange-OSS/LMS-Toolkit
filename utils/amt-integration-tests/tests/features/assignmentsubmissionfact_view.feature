# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

Feature: AssignmentSubmissionFact-C View
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
        # Assignment for Canvas
        And there is one Assignment
            | AssignmentIdentifier | AssignmentSubmissionFact-C |
            | SchoolId             | 54                         |
            | SourceSystem         | Canvas                     |
            | Title                | A discussion for 1054      |
            | Description          | The description            |
            | StartDateTime        | 1054-07-08 09:00           |
            | EndDateTime          | 1054-07-09 10:00           |
            | DueDateTime          | 1054-07-09 10:11           |
            | MaxPoints            | 98                         |
            | SectionIdentifier    | si-1054                    |
            | LastModifiedDate     | 1054-07-07 09:01           |
            | AssignmentCategory   | Assignment                 |
        # Assignment for Schoology
        And there is one Assignment
            | AssignmentIdentifier | AssignmentSubmissionFact-S |
            | SchoolId             | 54                         |
            | SourceSystem         | Schoology                  |
            | Title                | A discussion for 1054      |
            | Description          | The description            |
            | StartDateTime        | 1054-07-08 09:00           |
            | EndDateTime          | 1054-07-09 10:00           |
            | DueDateTime          | 1054-07-09 10:11           |
            | MaxPoints            | 98                         |
            | SectionIdentifier    | si-1054                    |
            | LastModifiedDate     | 1054-07-07 09:01           |
            | AssignmentCategory   | Assignment                 |
        # Assignment for Google Classroom
        And there is one Assignment
            | AssignmentIdentifier | AssignmentSubmissionFact-G |
            | SchoolId             | 54                         |
            | SourceSystem         | Google                     |
            | Title                | A discussion for 1054      |
            | Description          | The description            |
            | StartDateTime        | 1054-07-08 09:00           |
            | EndDateTime          | 1054-07-09 10:00           |
            | DueDateTime          | 1054-07-09 10:11           |
            | MaxPoints            | 98                         |
            | SectionIdentifier    | si-1054                    |
            | LastModifiedDate     | 1054-07-07 09:01           |
            | AssignmentCategory   | Assignment                 |
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

    Scenario: On Time Happy Path (Canvas - on-time)
        Given student "first-student" has an assignment submission
            | AssignmentSubmissionIdentifier | on-time-happy-path-c       |
            | AssignmentIdentifier           | AssignmentSubmissionFact-C |
            | SchoolId                       | 54                         |
            | SubmissionStatus               | on-time                    |
            | SubmissionDateTime             | 1054-07-09 9:12:34         |
            | EarnedPoints                   | 90                         |
            | Grade                          | A--                        |
            | LastModifiedDate               | 1054-07-09 9:12:34         |
        When I query for assignment submission "on-time-happy-path-c"
        Then there should be 1 submission records
        And the submission record should have these values:
            | AssignmentSubmissionKey | on-time-happy-path-c                 |
            | StudentSchoolKey        | first-student-54                     |
            | SchoolKey               | 54                                   |
            | StudentKey              | first-student                        |
            | SectionKey              | 54-abc-1054-1054-si-1504-Summer-1054 |
            | AssignmentKey           | AssignmentSubmissionFact-C           |
            | SubmissionDateKey       | 1054-07-09                           |
            | EarnedPoints            | 90                                   |
            | NumericGrade            | 91                                   |
            | LetterGrade             | A--                                  |
            | IsPastDue               | 0                                    |
            | SubmittedLate           | 0                                    |
            | SubmittedOnTime         | 1                                    |
            | LastModifiedDate        | 054-07-09 9:12:34                    |


    Scenario: On Time Happy Path (Canvas - graded)
        Given student "first-student" has an assignment submission
            | AssignmentSubmissionIdentifier | graded-happy-path-c        |
            | AssignmentIdentifier           | AssignmentSubmissionFact-C |
            | SchoolId                       | 54                         |
            | SubmissionStatus               | graded                     |
            | SubmissionDateTime             | 1054-07-09 9:12:34         |
            | EarnedPoints                   | 90                         |
            | Grade                          | A--                        |
            | LastModifiedDate               | 1054-07-09 9:12:34         |
        When I query for assignment submission "graded-happy-path-c"
        Then there should be 1 submission records
        And the submission record should have these values:
            | AssignmentSubmissionKey | graded-happy-path-c                  |
            | StudentSchoolKey        | first-student-54                     |
            | SchoolKey               | 54                                   |
            | StudentKey              | first-student                        |
            | SectionKey              | 54-abc-1054-1054-si-1504-Summer-1054 |
            | AssignmentKey           | AssignmentSubmissionFact-C           |
            | SubmissionDateKey       | 1054-07-09                           |
            | EarnedPoints            | 90                                   |
            | NumericGrade            | 91                                   |
            | LetterGrade             | A--                                  |
            | IsPastDue               | 0                                    |
            | SubmittedLate           | 0                                    |
            | SubmittedOnTime         | 1                                    |
            | LastModifiedDate        | 054-07-09 9:12:34                    |

    Scenario: Late Happy Path (Canvas)
        Given student "first-student" has an assignment submission
            | AssignmentSubmissionIdentifier | late-happy-path-c          |
            | AssignmentIdentifier           | AssignmentSubmissionFact-C |
            | SchoolId                       | 54                         |
            | SubmissionStatus               | late                       |
            | SubmissionDateTime             | 2054-07-09 9:12:34         |
            | EarnedPoints                   | 80                         |
            | Grade                          | B--                        |
            | LastModifiedDate               | 1054-07-09 9:12:34         |
        When I query for assignment submission "late-happy-path-c"
        Then there should be 1 submission records
        And the submission record should have these values:
            | AssignmentSubmissionKey | on-time-happy-path-c                 |
            | StudentSchoolKey        | first-student-54                     |
            | SchoolKey               | 54                                   |
            | StudentKey              | first-student                        |
            | SectionKey              | 54-abc-1054-1054-si-1504-Summer-1054 |
            | AssignmentKey           | AssignmentSubmissionFact-C           |
            | SubmissionDateKey       | 1054-07-09                           |
            | EarnedPoints            | 80                                   |
            | NumericGrade            | 81                                   |
            | LetterGrade             | B--                                  |
            | IsPastDue               | 0                                    |
            | SubmittedLate           | 1                                    |
            | SubmittedOnTime         | 0                                    |
            | LastModifiedDate        | 054-07-09 9:12:34                    |

    Scenario: Missing or Past Due Happy Path (Canvas)
        Given student "first-student" has an assignment submission
            | AssignmentSubmissionIdentifier | pastdue-happy-path-c       |
            | AssignmentIdentifier           | AssignmentSubmissionFact-C |
            | SchoolId                       | 54                         |
            | SubmissionStatus               | missing                    |
            | SubmissionDateTime             |                            |
            | EarnedPoints                   |                            |
            | Grade                          |                            |
            | LastModifiedDate               | 1054-07-09 9:12:34         |
        When I query for assignment submission "pastdue-happy-path-c"
        Then there should be 1 submission records
        And the submission record should have these values:
            | AssignmentSubmissionKey | pastdue-happy-path-c                 |
            | StudentSchoolKey        | first-student-54                     |
            | SchoolKey               | 54                                   |
            | StudentKey              | first-student                        |
            | SectionKey              | 54-abc-1054-1054-si-1504-Summer-1054 |
            | AssignmentKey           | AssignmentSubmissionFact-C           |
            | SubmissionDateKey       |                                      |
            | EarnedPoints            |                                      |
            | NumericGrade            |                                      |
            | LetterGrade             |                                      |
            | IsPastDue               | 1                                    |
            | SubmittedLate           | 0                                    |
            | SubmittedOnTime         | 0                                    |
            | LastModifiedDate        | 054-07-09 9:12:34                    |



    Scenario: On Time Happy Path (Schoology)
        Given student "first-student" has an assignment submission
            | AssignmentSubmissionIdentifier | on-time-happy-path-s       |
            | AssignmentIdentifier           | AssignmentSubmissionFact-s |
            | SchoolId                       | 54                         |
            | SubmissionStatus               | on-time                    |
            | SubmissionDateTime             | 1054-07-09 9:12:34         |
            | EarnedPoints                   | 90                         |
            | Grade                          | A--                        |
            | LastModifiedDate               | 1054-07-09 9:12:34         |
        When I query for assignment submission "on-time-happy-path-s"
        Then there should be 1 submission records
        And the submission record should have these values:
            | AssignmentSubmissionKey | on-time-happy-path-s                 |
            | StudentSchoolKey        | first-student-54                     |
            | SchoolKey               | 54                                   |
            | StudentKey              | first-student                        |
            | SectionKey              | 54-abc-1054-1054-si-1504-Summer-1054 |
            | AssignmentKey           | AssignmentSubmissionFact-s           |
            | SubmissionDateKey       | 1054-07-09                           |
            | EarnedPoints            | 90                                   |
            | NumericGrade            | 91                                   |
            | LetterGrade             | A--                                  |
            | IsPastDue               | 0                                    |
            | SubmittedLate           | 0                                    |
            | SubmittedOnTime         | 1                                    |
            | LastModifiedDate        | 054-07-09 9:12:34                    |

    Scenario: Late Happy Path (Schoology)
        Given student "first-student" has an assignment submission
            | AssignmentSubmissionIdentifier | late-happy-path-s          |
            | AssignmentIdentifier           | AssignmentSubmissionFact-s |
            | SchoolId                       | 54                         |
            | SubmissionStatus               | late                       |
            | SubmissionDateTime             | 2054-07-09 9:12:34         |
            | EarnedPoints                   | 80                         |
            | Grade                          | B--                        |
            | LastModifiedDate               | 1054-07-09 9:12:34         |
        When I query for assignment submission "late-happy-path-s"
        Then there should be 1 submission records
        And the submission record should have these values:
            | AssignmentSubmissionKey | on-time-happy-path-s                 |
            | StudentSchoolKey        | first-student-54                     |
            | SchoolKey               | 54                                   |
            | StudentKey              | first-student                        |
            | SectionKey              | 54-abc-1054-1054-si-1504-Summer-1054 |
            | AssignmentKey           | AssignmentSubmissionFact-s           |
            | SubmissionDateKey       | 1054-07-09                           |
            | EarnedPoints            | 80                                   |
            | NumericGrade            | 81                                   |
            | LetterGrade             | B--                                  |
            | IsPastDue               | 0                                    |
            | SubmittedLate           | 1                                    |
            | SubmittedOnTime         | 0                                    |
            | LastModifiedDate        | 054-07-09 9:12:34                    |

    #
    # TODO in LMS-354
    # We don't have a descriptor for Schoology missing right now, therefore
    # this test will never pass.
    #
    # Scenario: Missing or Past Due Happy Path (Schoology)
    #     Given student "first-student" has an assignment submission
    #         | AssignmentSubmissionIdentifier | pastdue-happy-path-s       |
    #         | AssignmentIdentifier           | AssignmentSubmissionFact-s |
    #         | SchoolId                       | 54                         |
    #         | SubmissionStatus               | missing                    |
    #         | SubmissionDateTime             |                            |
    #         | EarnedPoints                   |                            |
    #         | Grade                          |                            |
    #         | LastModifiedDate               | 1054-07-09 9:12:34         |
    #     When I query for assignment submission "pastdue-happy-path-s"
    #     Then there should be 1 submission records
    #     And the submission record should have these values:
    #         | AssignmentSubmissionKey | pastdue-happy-path-s                 |
    #         | StudentSchoolKey        | first-student-54                     |
    #         | SchoolKey               | 54                                   |
    #         | StudentKey              | first-student                        |
    #         | SectionKey              | 54-abc-1054-1054-si-1504-Summer-1054 |
    #         | AssignmentKey           | AssignmentSubmissionFact-C           |
    #         | SubmissionDateKey       |                                      |
    #         | EarnedPoints            |                                      |
    #         | NumericGrade            |                                      |
    #         | LetterGrade             |                                      |
    #         | IsPastDue               | 1                                    |
    #         | SubmittedLate           | 0                                    |
    #         | SubmittedOnTime         | 0                                    |
    #         | LastModifiedDate        | 054-07-09 9:12:34                    |

    Scenario: Do not report on Schoology drafts
        Given student "first-student" has an assignment submission
            | AssignmentSubmissionIdentifier | schoology-draft            |
            | AssignmentIdentifier           | AssignmentSubmissionFact-s |
            | SchoolId                       | 54                         |
            | SubmissionStatus               | draft                      |
            | SubmissionDateTime             | 1054-07-09 9:12:34         |
            | EarnedPoints                   | 90                         |
            | Grade                          | A--                        |
            | LastModifiedDate               | 1054-07-09 9:12:34         |
        When I query for assignment submission "schoology-draft"
        Then there should be 0 submission records


    Scenario: On Time Happy Path (Google)
        Given student "first-student" has an assignment submission
            | AssignmentSubmissionIdentifier | on-time-happy-path-g       |
            | AssignmentIdentifier           | AssignmentSubmissionFact-g |
            | SchoolId                       | 54                         |
            | SubmissionStatus               | turned_in                  |
            | SubmissionDateTime             | 1054-07-09 9:12:34         |
            | EarnedPoints                   | 90                         |
            | Grade                          | A--                        |
            | LastModifiedDate               | 1054-07-09 9:12:34         |
        When I query for assignment submission "on-time-happy-path-g"
        Then there should be 1 submission records
        And the submission record should have these values:
            | AssignmentSubmissionKey | on-time-happy-path-g                 |
            | StudentSchoolKey        | first-student-54                     |
            | SchoolKey               | 54                                   |
            | StudentKey              | first-student                        |
            | SectionKey              | 54-abc-1054-1054-si-1504-Summer-1054 |
            | AssignmentKey           | AssignmentSubmissionFact-g           |
            | SubmissionDateKey       | 1054-07-09                           |
            | EarnedPoints            | 90                                   |
            | NumericGrade            | 91                                   |
            | LetterGrade             | A--                                  |
            | IsPastDue               | 0                                    |
            | SubmittedLate           | 0                                    |
            | SubmittedOnTime         | 1                                    |
            | LastModifiedDate        | 054-07-09 9:12:34                    |

    Scenario: On Time Happy Path (Google - Returned)
        Given student "first-student" has an assignment submission
            | AssignmentSubmissionIdentifier | returned-happy-path-g      |
            | AssignmentIdentifier           | AssignmentSubmissionFact-g |
            | SchoolId                       | 54                         |
            | SubmissionStatus               | returned                   |
            | SubmissionDateTime             | 1054-07-09 9:12:34         |
            | EarnedPoints                   | 90                         |
            | Grade                          | A--                        |
            | LastModifiedDate               | 1054-07-09 9:12:34         |
        When I query for assignment submission "on-time-happy-path-g"
        Then there should be 1 submission records
        And the submission record should have these values:
            | AssignmentSubmissionKey | on-time-happy-path-g                 |
            | StudentSchoolKey        | first-student-54                     |
            | SchoolKey               | 54                                   |
            | StudentKey              | first-student                        |
            | SectionKey              | 54-abc-1054-1054-si-1504-Summer-1054 |
            | AssignmentKey           | AssignmentSubmissionFact-g           |
            | SubmissionDateKey       | 1054-07-09                           |
            | EarnedPoints            | 90                                   |
            | NumericGrade            | 91                                   |
            | LetterGrade             | A--                                  |
            | IsPastDue               | 0                                    |
            | SubmittedLate           | 0                                    |
            | SubmittedOnTime         | 1                                    |
            | LastModifiedDate        | 054-07-09 9:12:34                    |

    Scenario: Late Happy Path (Google)
        Given student "first-student" has an assignment submission
            | AssignmentSubmissionIdentifier | late-happy-path-g          |
            | AssignmentIdentifier           | AssignmentSubmissionFact-g |
            | SchoolId                       | 54                         |
            | SubmissionStatus               | late                       |
            | SubmissionDateTime             | 2054-07-09 9:12:34         |
            | EarnedPoints                   | 80                         |
            | Grade                          | B--                        |
            | LastModifiedDate               | 1054-07-09 9:12:34         |
        When I query for assignment submission "late-happy-path-g"
        Then there should be 1 submission records
        And the submission record should have these values:
            | AssignmentSubmissionKey | on-time-happy-path-g                 |
            | StudentSchoolKey        | first-student-54                     |
            | SchoolKey               | 54                                   |
            | StudentKey              | first-student                        |
            | SectionKey              | 54-abc-1054-1054-si-1504-Summer-1054 |
            | AssignmentKey           | AssignmentSubmissionFact-g           |
            | SubmissionDateKey       | 1054-07-09                           |
            | EarnedPoints            | 80                                   |
            | NumericGrade            | 81                                   |
            | LetterGrade             | B--                                  |
            | IsPastDue               | 0                                    |
            | SubmittedLate           | 1                                    |
            | SubmittedOnTime         | 0                                    |
            | LastModifiedDate        | 054-07-09 9:12:34                    |

    Scenario: Missing or Past Due Happy Path (Google)
        Given student "first-student" has an assignment submission
            | AssignmentSubmissionIdentifier | pastdue-happy-path-g       |
            | AssignmentIdentifier           | AssignmentSubmissionFact-g |
            | SchoolId                       | 54                         |
            | SubmissionStatus               | missing                    |
            | SubmissionDateTime             |                            |
            | EarnedPoints                   |                            |
            | Grade                          |                            |
            | LastModifiedDate               | 1054-07-09 9:12:34         |
        When I query for assignment submission "pastdue-happy-path-g"
        Then there should be 1 submission records
        And the submission record should have these values:
            | AssignmentSubmissionKey | pastdue-happy-path-g                 |
            | StudentSchoolKey        | first-student-54                     |
            | SchoolKey               | 54                                   |
            | StudentKey              | first-student                        |
            | SectionKey              | 54-abc-1054-1054-si-1504-Summer-1054 |
            | AssignmentKey           | AssignmentSubmissionFact-g           |
            | SubmissionDateKey       |                                      |
            | EarnedPoints            |                                      |
            | NumericGrade            |                                      |
            | LetterGrade             |                                      |
            | IsPastDue               | 1                                    |
            | SubmittedLate           | 0                                    |
            | SubmittedOnTime         | 0                                    |
            | LastModifiedDate        | 054-07-09 9:12:34                    |

    Scenario: Do not report on Google New submissions
        Given student "first-student" has an assignment submission
            | AssignmentSubmissionIdentifier | google-new                 |
            | AssignmentIdentifier           | AssignmentSubmissionFact-g |
            | SchoolId                       | 54                         |
            | SubmissionStatus               | new                        |
            | SubmissionDateTime             |                            |
            | EarnedPoints                   |                            |
            | Grade                          |                            |
            | LastModifiedDate               | 1054-07-09 9:12:34         |
        When I query for assignment submission "google-new"
        Then there should be 0 submission records

    Scenario: Do not report on Google Created submissions
        Given student "first-student" has an assignment submission
            | AssignmentSubmissionIdentifier | google-created             |
            | AssignmentIdentifier           | AssignmentSubmissionFact-g |
            | SchoolId                       | 54                         |
            | SubmissionStatus               | new                        |
            | SubmissionDateTime             |                            |
            | EarnedPoints                   |                            |
            | Grade                          |                            |
            | LastModifiedDate               | 1054-07-09 9:12:34         |
        When I query for assignment submission "google-created"
        Then there should be 0 submission records

    Scenario: Do not report on Google Reclaimed submissions
        Given student "first-student" has an assignment submission
            | AssignmentSubmissionIdentifier | google-reclaimed           |
            | AssignmentIdentifier           | AssignmentSubmissionFact-g |
            | SchoolId                       | 54                         |
            | SubmissionStatus               | reclaimed_by_student       |
            | SubmissionDateTime             |                            |
            | EarnedPoints                   |                            |
            | Grade                          |                            |
            | LastModifiedDate               | 1054-07-09 9:12:34         |
        When I query for assignment submission "google-reclaimed"
        Then there should be 0 submission records



# TODO: are we missing a descriptor for a Canvas submission that is in draft or
# or has not been submitted and it is not late?
