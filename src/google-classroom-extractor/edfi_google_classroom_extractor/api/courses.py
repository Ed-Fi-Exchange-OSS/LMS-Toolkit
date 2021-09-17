# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import List, Dict, cast
from pandas import DataFrame, Series, json_normalize
import sqlalchemy
from googleapiclient.discovery import Resource
from edfi_google_classroom_extractor.api.api_caller import call_api, ResourceType
from edfi_lms_extractor_lib.api.resource_sync import (
    cleanup_after_sync,
    sync_to_db_without_cleanup,
)


COURSES_RESOURCE_NAME = "Courses"
EDFI_LMS_PREFIX = "EdFiLMS."

logger = logging.getLogger(__name__)


def request_course_aliases(resource: Resource, course_id: str) -> List[Dict[str, str]]:
    """
    Fetch CourseAlias API data for the given course id

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource
    course_id: str
        a Google Classroom course id

    Returns
    -------
    List[Dict[str, str]]
        a list of Google Classroom CourseAliases for the given course id,
            see https://developers.google.com/classroom/reference/rest/v1/courses.aliases
    """
    return call_api(
        cast(ResourceType, resource).courses().aliases().list,
        {"courseId": course_id},
        "aliases",
    )


def _alias_names_for_scope(aliases: List[str], scope: str) -> List[str]:
    """
    Returns a list of alias names from a list of aliases with the given scope.
    Aliases from the API are scoped with a prefix character followed by a colon
    and then the alias name. For example "d:alias_name_1".

    Parameters
    ----------
    aliases: List[str]
        a list of course alias strings from the API
    scope: str
        the scope to filter by

    Returns
    -------
    List[str]
        a list of alias names (scope omitted) filtered by the given scope
    """
    result: List[str] = []
    try:
        result = [
            alias.split(":")[1] for alias in aliases if alias.split(":")[0] == scope
        ]
    except (ValueError, IndexError):
        pass
    return result


def _find_first_with_edfilms_prefix(alias_names: List[str]) -> str:
    """
    Returns the first alias name in the list prefixed with the
    Ed-Fi LMS indicator, with the prefix removed, or an empty string if none are found.

    Parameters
    ----------
    alias_names: List[str]
        a list of alias names

    Returns
    -------
    str
        The first alias name in the list prefixed with the
        Ed-Fi LMS indicator, with the prefix removed, or an empty string if none are found.
    """
    return next(
        (
            alias_name.removeprefix(EDFI_LMS_PREFIX)  # type: ignore
            for alias_name in alias_names
            if alias_name.startswith(EDFI_LMS_PREFIX)
        ),
        "",
    )


def _select_alias(aliases: List[str]) -> str:
    """
    Selects the most relevant course alias from a list of course aliases returned by the API

    Parameters
    ----------
    aliases: List[str]
        a list of course alias strings from the API, including the "d:" (domain scope) prefix

    Returns
    -------
    str
        a (possibly empty) string representing the most relevant alias for the course.

    Notes
    -----
    How to find the correct SISSectionIdentifier from CourseAlias results:

    If there are no aliases:
    SISSectionIdentifier = ""

    Else if there is exactly one alias:
    SISSectionIdentifier = alias

    Else if there is a domain alias prefixed with "EdFiLMS.":
    SISSectionIdentifier = first domain alias prefixed with "EdFiLMS.", prefix excluded

    Else if there are domain aliases:
    SISSectionIdentifier = first domain alias

    Else:
    SISSectionIdentifier = ""
    """
    if len(aliases) == 0:
        return ""

    if len(aliases) == 1:
        try:
            _, alias_name = aliases[0].split(":")
            return alias_name.removeprefix(EDFI_LMS_PREFIX)  # type: ignore
        except ValueError:
            return ""

    domain_alias_names: List[str] = _alias_names_for_scope(aliases, "d")
    edfilms_domain_alias = _find_first_with_edfilms_prefix(domain_alias_names)
    if edfilms_domain_alias != "":
        return edfilms_domain_alias

    if len(domain_alias_names) > 0:
        return domain_alias_names[0]

    return ""


def _derive_alias(resource: Resource, row: Series) -> str:
    """
    Derives a single alias for a course dataframe row, from a fetch of CourseAliases

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource
    row: Series
        a Pandas Series row for a single Google Classroom course

    Returns
    -------
    str
        a (possibly empty) string representing the most relevant alias for the course.
    """
    course_aliases: List[Dict[str, str]] = request_course_aliases(resource, row["id"])
    alias_strings: List[str] = [
        course_alias["alias"] for course_alias in course_aliases
    ]
    return _select_alias(alias_strings)


def request_courses(resource: Resource) -> List[Dict[str, str]]:
    """
    Fetch Course API data for all courses and return a list of course data

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource

    Returns
    -------
    List[Dict[str, str]]
        a list of Google Classroom Course resources,
            see https://developers.google.com/classroom/reference/rest/v1/courses
    """
    return call_api(
        cast(ResourceType, resource).courses().list,
        {"courseStates": "ACTIVE"},
        "courses",
    )


def request_latest_courses_as_df(resource: Resource) -> DataFrame:
    """
    Fetch Course API data for all courses and return a Courses API DataFrame

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource

    Returns
    -------
    DataFrame
        a Courses API DataFrame with the fetched data

    Notes
    -----
    DataFrame columns are:
        id: Identifier for this course assigned by Classroom
        name: Name of the course
        section: Section of the course
        descriptionHeading: Optional heading for the description
        description: Optional description
        room: Optional room location
        ownerId: The identifier of the owner of a course
        creationTime: Creation time of the course
        updateTime: Time of the most recent update to this course
        enrollmentCode: Enrollment code to use when joining this course
        courseState: State of the course
        alternateLink: Absolute link to this course in the Classroom web UI
        teacherGroupEmail: The email address of a Google group containing all teachers of the course
        courseGroupEmail: The email address of a Google group containing all members of the course
        guardiansEnabled: Whether or not guardian notifications are enabled for this course
        calendarId: The Calendar ID for a calendar that all course members can see
        alias: A course alias selected from the available aliases for the course
    """

    logger.info("Pulling course data")
    courses: List[Dict[str, str]] = request_courses(resource)
    courses_df: DataFrame = json_normalize(courses)
    courses_df["alias"] = courses_df.apply(
        lambda row: _derive_alias(resource, row), axis=1
    )
    return courses_df


def request_all_courses_as_df(
    resource: Resource, sync_db: sqlalchemy.engine.base.Engine
) -> DataFrame:
    """
    Fetch Course API data for all courses and return a Courses API DataFrame

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections

    Returns
    -------
    DataFrame
        a Courses API DataFrame with the current and previously fetched data

    Notes
    -----
    DataFrame columns are:
        id: Identifier for this course assigned by Classroom
        name: Name of the course
        section: Section of the course
        descriptionHeading: Optional heading for the description
        description: Optional description
        room: Optional room location
        ownerId: The identifier of the owner of a course
        creationTime: Creation time of the course
        updateTime: Time of the most recent update to this course
        enrollmentCode: Enrollment code to use when joining this course
        courseState: State of the course
        alternateLink: Absolute link to this course in the Classroom web UI
        teacherGroupEmail: The email address of a Google group containing all teachers of the course
        courseGroupEmail: The email address of a Google group containing all members of the course
        teacherFolder.id: The identifier of the teacher folder
        teacherFolder.title: The identifier of the teacher folder,
        teacherFolder.alternateLink: Absolute link to the teacher folder in the Classroom web UI
        guardiansEnabled: Whether or not guardian notifications are enabled for this course
        calendarId: The Calendar ID for a calendar that all course members can see
        alias: A course alias selected from the available aliases for the course
        CreateDate: Date this record was created by the extractor
        LastModifiedDate: Date this record was last updated by the extractor
    """

    courses_df = request_latest_courses_as_df(resource)
    courses_df = _sync_without_cleanup(courses_df, sync_db)
    cleanup_after_sync(COURSES_RESOURCE_NAME, sync_db)

    return courses_df


def _sync_without_cleanup(
    resource_df: DataFrame, sync_db: sqlalchemy.engine.base.Engine
) -> DataFrame:
    """
    Take fetched API data and sync with database. Creates tables when necessary,
    but ok if temporary tables are there to start. Doesn't delete temporary tables when finished.

    Parameters
    ----------
    resource_df: DataFrame
        a Courses API DataFrame with the current fetched data which
        will be mutated, adding Hash and CreateDate/LastModifiedDate
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections

    Returns
    -------
    DataFrame
        a DataFrame with current fetched data and reconciled CreateDate/LastModifiedDate
    """
    return sync_to_db_without_cleanup(
        resource_df=resource_df,
        identity_columns=["id"],
        resource_name=COURSES_RESOURCE_NAME,
        sync_db=sync_db,
    )
