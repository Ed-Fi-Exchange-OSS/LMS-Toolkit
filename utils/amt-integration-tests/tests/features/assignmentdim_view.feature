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
