# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


# Scaffold only for now

def _query_for_section_summary() -> str:
    return """
SELECT
    COUNT(1) as UnmatchedCount
FROM
    edfilms.exceptions_LMSSection
    """


def _query_for_section_user() -> str:
    return """
SELECT
    COUNT(1) as UnmatchedCount
FROM
    edfilms.exceptions_LMSUser
    """


def get_summary() -> None:

    pass


def create_files() -> None:
    pass
