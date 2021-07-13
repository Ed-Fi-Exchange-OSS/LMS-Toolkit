# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

Feature: AssignmentDim View
    As a data analyst,
    I want to denormalize LMS Assignment data,
    so that I can build reports on student engagement.

    Scenario: Ensure the view exists
        Given Analytics Middle Tier has been installed

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
        Given Analytics Middle Tier has been installed

          # TODO: Loading descriptors is now done once for the entire session so
          # that we don't have re-insertion attempts. Let's discuss the value of
          # having given statements like the one above and, possibly, the one below,
          # which explain the conditions but don't actually do anything.

        # And the default LMS descriptors have been loaded

          And there is a school with id 53

          And the school year is 1053

          And school 53 has a session called "Summer-1053" in year 1053

            # TODO: think about making some parts of these records more
            # unique to the scenario, because of the brittleness of
            # these tests that will be assuming there are unique
            # records just for the given test.

        # I wonder if we should prep the database with just one school, school year, session, etc?
        # instead of inserting new values every time.

          And there is a section
              | LocalCourseCode   | abc-1053    |
              | SchoolId          | 53          |
              | SchoolYear        | 1053        |
              | SectionIdentifier | si-1053     |
              | SessionName       | Summer-1053 |

        #   And there is a grading period
        #       | Descriptor     | First summer session 1053 |
        #       | PeriodSequence | 3                         |
        #       | SchoolId       | 53                        |
        #       | SchoolYear     | 1053                      |
        #       | BeginDate      | 1053-07-01 01:23:45       |

            # In the following, note the very last row, establishing
            # that this is a _discussion_ category of Assignment,
            # rather than a _assignment_ category of Assignment.
        #   And there is one Assignment
        #       | AssignmentIdentifier | assigndim-happy-path  |
        #       | SchoolId             | 53                    |
        #       | SourceSystem         | Schoology             |
        #       | Title                | A discussion for 1053 |
        #       | Description          | The description       |
        #       | StartDateTime        | 1053-07-08 09:00      |
        #       | EndDateTime          | 1053-07-09 10:00      |
        #       | DueDateTime          | 1053-07-09 10:11      |
        #       | MaxPoints            | 99                    |
        #       | SectionIdentifier    | si-1053               |
        #       | LastModifiedDate     | 1053-07-07 09:01      |
        #       | AssignmentCategory   | discussion            |

         When I query for assignments with identifier "assigndim-happy-path"

        #  Then there should be 1 records

          Then the AssignmentDim record should have these values:
              | AssignmentKey    | assigndim-happy-path                 |
              | SchoolKey        | 53                                   |
              | SourceSystem     | Schoology                            |
              | Title            | A discussion for 1053                |
              | Description      | The description                      |
              | StartDateKey     | 1053-07-08                           |
              | EndDateKey       | 1053-07-09                           |
              | DueDateKey       | 1053-07-09                           |
              | MaxPoints        | 99                                   |
              | SectionKey       | 53-abc-1053-1053-si-1503-Summer-1053 |
              | GradingPeriodKey | r"[0-9]+-53-1053-07-01"              |
              | LastModifiedDate | r"\d{4}-\d{2}-\d{2}"                 |


    Scenario: Ignores discussions
        Given Analytics Middle Tier has been installed

          # TODO: Loading descriptors is now done once for the entire session so
          # that we don't have re-insertion attempts. Let's discuss the value of
          # having given statements like the one above and, possibly, the one below,
          # which explain the conditions but don't actually do anything.

        # And the default LMS descriptors have been loaded

          And there is a school with id 54

          And the school year is 1054

          And school 54 has a session called "Summer-1054" in year 1054

            # TODO: think about making some parts of these records more
            # unique to the scenario, because of the brittleness of
            # these tests that will be assuming there are unique
            # records just for the given test.

          And there is a section
              | LocalCourseCode   | abc-1054    |
              | SchoolId          | 54          |
              | SchoolYear        | 1054        |
              | SectionIdentifier | si-1054     |
              | SessionName       | Summer-1054 |

        #   And there is a grading period
        #       | Descriptor     | First summer session 1054 |
        #       | PeriodSequence | 3                         |
        #       | SchoolId       | 54                        |
        #       | SchoolYear     | 1054                      |

            # In the following, note the very last row, establishing
            # that this is a _discussion_ category of Assignment,
            # rather than a _assignment_ category of Assignment.
        #   And there is one Assignment
        #       | AssignmentIdentifier | assigndim-happy-path  |
        #       | SchoolId             | 54                    |
        #       | SourceSystem         | Schoology             |
        #       | Title                | A discussion for 1054 |
        #       | Description          | The description       |
        #       | StartDateTime        | 1054-07-08 09:00      |
        #       | EndDateTime          | 1054-07-09 10:00      |
        #       | DueDateTime          | 1054-07-09 10:11      |
        #       | MaxPoints            | 99                    |
        #       | SectionIdentifier    | si-1054               |
        #       | LastModifiedDate     | 1054-07-07 09:01      |
        #       | AssignmentCategory   | discussion            |


         When I query for assignments with identifier "ignore-discussion"

         Then there should be 0 records






