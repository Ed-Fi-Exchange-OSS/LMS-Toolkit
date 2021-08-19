# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

QUERY_FOR_SECTIONS = "SELECT * FROM lmsx.exceptions_LMSSection"

QUERY_FOR_SECTION_SUMMARY = """
SELECT
    COUNT(1) as UnmatchedCount
FROM
    lmsx.exceptions_LMSSection
    """

QUERY_FOR_USERS = "SELECT * FROM lmsx.exceptions_LMSUser"

QUERY_FOR_USERS_SUMMARY = """
SELECT
    COUNT(1) as UnmatchedCount
FROM
    lmsx.exceptions_LMSUser
    """

QUERY_FOR_ASSIGNMENT_CAT_DESCRIPTORS = """
SELECT
    distinct AssignmentCategory as MissingValue,
    'AssignmentCategoryDescriptor' as Descriptor,
    'uri://ed-fi.org/edfilms/AssignmentCategoryDescriptor/' + SourceSystem as Namespace
FROM lmsx.missing_assignment_category_descriptors
"""

QUERY_FOR_ASSIGNMENT_CAT_DESCRIPTORS_SUMMARY = """
SELECT
    count(distinct AssignmentCategory)
FROM
    lmsx.missing_assignment_category_descriptors
    """

QUERY_FOR_SUBMISSION_STATUS_DESCRIPTORS = """
SELECT
    distinct SubmissionStatus as MissingValue,
    'SubmissionStatusDescriptor' as Descriptor,
    'uri://ed-fi.org/edfilms/SubmissionStatusDescriptor/' + SourceSystem as Namespace
FROM lmsx.missing_assignment_submission_status_descriptors
"""

QUERY_FOR_SUBMISSION_STATUS_DESCRIPTORS_SUMMARY = """
SELECT
    count(distinct SubmissionStatus)
FROM
    lmsx.missing_assignment_submission_status_descriptors
    """

QUERY_FOR_ASSIGNMENT_EXCEPTIONS = """
SELECT
    count(*)
FROM
    lmsx.assignments_exceptions
    """

QUERY_FOR_ASSIGNMENT_SUBMISSION_EXCEPTIONS = """
SELECT
    count(*)
FROM
    lmsx.assignment_submissions_exceptions
    """
