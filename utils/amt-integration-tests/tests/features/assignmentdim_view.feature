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

         When I query the AssignmentsDim view

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

    Scenario: Ignores discussions
        Given Analytics Middle Tier has been installed

          # TODO: Loading descriptors is now done once for the entire session so
          # that we don't have re-insertion attempts. Let's discuss the value of
          # having given statements like the one above and, possibly, the one below,
          # which explain the conditions but don't actually do anything.

        # And the default LMS descriptors have been loaded

          And there is a school with id 54

          And the school year is 2021

          And school 54 has a session called "Fall" in year 2021

            # TODO: think about making some parts of these records more
            # unique to the scenario, because of the brittleness of
            # these tests that will be assuming there are unique
            # records just for the given test.

        #   And there is a section
        #       | LocalCourseCode   | abc    |
        #       | SchoolId          | 54     |
        #       | Schoolyear        | 2021   |
        #       | SectionIdentifier | qwerty |
        #       | SessionName       | Fall   |

        #   And there is a grading period
        #       | Descriptor     | First summer session |
        #       | PeriodSequence | 3                    |
        #       | SchoolId       | 54                   |
        #       | SchoolYear     | 2021                 |

            # In the following, note the very last row, establishing
            # that this is a _discussion_ category of Assignment,
            # rather than a _assignment_ category of Assignment.
        #   And there is one Assignment
        #       | AssignmentIdentifier | ignore-discussion |
        #       | SchoolId             | 54                |
        #       | SourceSystem         | Schoology         |
        #       | Title                | A discussion      |
        #       | Description          | The description   |
        #       | StartDateTime        | 2021-07-08 09:00  |
        #       | EndDateTime          | 2021-07-09 10:00  |
        #       | DueDateTime          | 2021-07-09 10:11  |
        #       | MaxPoints            | 99                |
        #       | SectionIdentifier    | qwerty            |
        #       | LastModifiedDate     | 2021-07-07 09:01  |
        #       | AssignmentCategory   | discussion        |

         When I query for assignments with identifier "ignore-discussion"

         Then there should be 0 records






