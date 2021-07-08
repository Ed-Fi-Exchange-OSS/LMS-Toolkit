# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

Feature: AssignmentDim View
    Test to confirm the output of the AssignmentsDim View

    Scenario: Ensuring the view exists
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


