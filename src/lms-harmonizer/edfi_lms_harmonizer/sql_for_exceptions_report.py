# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

QUERY_FOR_SECTIONS = "select * from lmsx.exceptions_lmssection"

QUERY_FOR_SECTION_SUMMARY = """
select
    count(1) as unmatchedcount
from
    lmsx.exceptions_lmssection
    """

QUERY_FOR_USERS = "select * from lmsx.exceptions_lmsuser"

QUERY_FOR_USERS_SUMMARY = """
select
    count(1) as unmatchedcount
from
    lmsx.exceptions_lmsuser
    """

QUERY_FOR_ASSIGNMENT_CAT_DESCRIPTORS_MSSQL = """
select
    distinct assignmentcategory as missingvalue,
    'assignmentcategorydescriptor' as descriptor,
    'uri://ed-fi.org/edfilms/assignmentcategorydescriptor/' + sourcesystem as namespace
from lmsx.missing_assignment_category_descriptors
"""

QUERY_FOR_ASSIGNMENT_CAT_DESCRIPTORS_POSTGRESQL = """
select
    distinct assignmentcategory as missingvalue,
    'assignmentcategorydescriptor' as descriptor,
    'uri://ed-fi.org/edfilms/assignmentcategorydescriptor/' || sourcesystem as namespace
from lmsx.missing_assignment_category_descriptors
"""

QUERY_FOR_ASSIGNMENT_CAT_DESCRIPTORS_SUMMARY = """
select
    count(distinct assignmentcategory)
from
    lmsx.missing_assignment_category_descriptors
    """

QUERY_FOR_SUBMISSION_STATUS_DESCRIPTORS_MSSQL = """
select
    distinct submissionstatus as missingvalue,
    'submissionstatusdescriptor' as descriptor,
    'uri://ed-fi.org/edfilms/submissionstatusdescriptor/' + sourcesystem as namespace
from lmsx.missing_assignment_submission_status_descriptors
"""

QUERY_FOR_SUBMISSION_STATUS_DESCRIPTORS_POSTGRESQL = """
select
    distinct submissionstatus as missingvalue,
    'submissionstatusdescriptor' as descriptor,
    'uri://ed-fi.org/edfilms/submissionstatusdescriptor/' || sourcesystem as namespace
from lmsx.missing_assignment_submission_status_descriptors
"""

QUERY_FOR_SUBMISSION_STATUS_DESCRIPTORS_SUMMARY = """
select
    count(distinct submissionstatus)
from
    lmsx.missing_assignment_submission_status_descriptors
    """

QUERY_FOR_ASSIGNMENT_EXCEPTIONS = """
select
    count(*)
from
    lmsx.assignments_exceptions
    """

QUERY_FOR_ASSIGNMENT_SUBMISSION_EXCEPTIONS = """
select
    count(*)
from
    lmsx.assignment_submissions_exceptions
    """
