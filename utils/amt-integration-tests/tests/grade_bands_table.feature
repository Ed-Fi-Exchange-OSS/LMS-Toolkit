# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

Feature: Grade Bands
    The Grade Bands table

    Scenario: Checking for the Table
        Given Analytics Middle Tier has been installed

         When I query the Grade Band Table

         Then Grade Band has the following default records
              | BandName      | LowerBound | UpperBound |
              | Less than 50% | 0          | 50         |
              | 50% to 65%    | 50         | 65         |
              | 65% to 70%    | 65         | 70         |
              | 70% to 80%    | 70         | 80         |
              | 80% to 90%    | 80         | 90         |
              | 90% to 100%   | 90         | 100        |
