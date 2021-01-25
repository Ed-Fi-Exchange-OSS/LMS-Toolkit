# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict, List, Tuple

from canvasapi import Canvas
from canvasapi.enrollment import Enrollment
import sqlalchemy
from canvasapi.course import Course
from canvasapi.section import Section
from canvasapi.user import User
from canvasapi.assignment import Assignment
from canvasapi.submission import Submission
from pandas import DataFrame

from canvas_extractor.api import (
    courses as coursesApi,
    sections as sectionsApi,
    students as studentsApi,
    assignments as assignmentsApi,
    submissions as submissionsApi,
    enrollments as enrollmentsApi,
    authentication_events as authEventsApi
)
from canvas_extractor.mapping import (
    sections as sectionsMap,
    users as usersMap,
    assignments as assignmentsMap,
    submissions as submissionsMap,
    section_associations as section_associationsMap,
    grades as gradesMap,
)


def extract_courses(
    canvas: Canvas,
    start_date: str,
    end_date: str,
    sync_db: sqlalchemy.engine.base.Engine,
) -> Tuple[List[Course], DataFrame]:
    """
    Gets all Canvas courses, in the Ed-Fi UDM format.

    Parameters
    ----------
    canvas: Canvas
        Canvas object.
    sync_db: sqlalchemy.engine.base.Engine
        sync db.

    Returns
    -------
    Tuple[List[Course], DataFrame]
        A tuple with the list of Canvas Course objects and the udm_courses dataframe.
    """
    courses: List[Course] = coursesApi.request_courses(canvas, start_date, end_date)
    courses_df: DataFrame = coursesApi.courses_synced_as_df(courses, sync_db)

    return (courses, courses_df)


def extract_sections(
    courses: List[Course], sync_db: sqlalchemy.engine.base.Engine
) -> Tuple[List[Section], DataFrame]:
    """
    Gets all Canvas sections, in the Ed-Fi UDM format.

    Parameters
    ----------
    courses: List[Course]
        A list of Canvas Course objects.
    sync_db: sqlalchemy.engine.base.Engine
        sync db.

    Returns
    -------
    Tuple[List[Section], DataFrame]
        A tuple with the list of Canvas Section objects and the udm_sections dataframe.
    """
    sections: List[Section] = sectionsApi.request_sections(courses)
    sections_df: DataFrame = sectionsApi.sections_synced_as_df(sections, sync_db)
    udm_sections_df: DataFrame = sectionsMap.map_to_udm_sections(sections_df)

    return (sections, udm_sections_df)


def extract_students(
    courses: List[Course], sync_db: sqlalchemy.engine.base.Engine
) -> Tuple[List[User], DataFrame]:
    """
    Gets all Canvas students, in the Ed-Fi UDM format.

    Parameters
    ----------
    courses: List[Course]
        A list of Canvas Course objects.
    sync_db: sqlalchemy.engine.base.Engine
        sync db.

    Returns
    -------
    Tuple[List[User], DataFrame]
        A tuple with the list of Canvas User objects and the udm_users dataframe.
    """
    students: List[User] = studentsApi.request_students(courses)
    students_df: DataFrame = studentsApi.students_synced_as_df(students, sync_db)
    udm_students_df: DataFrame = usersMap.map_to_udm_users(students_df)

    return (students, udm_students_df)


def extract_assignments(
    courses: List[Course],
    sections_df: DataFrame,
    sync_db: sqlalchemy.engine.base.Engine,
) -> Tuple[List[Assignment], Dict[str, DataFrame]]:
    """
    Gets all Canvas assignments, in the Ed-Fi UDM format.

    Parameters
    ----------
    courses: List[Course]
        A list of Canvas Course objects.
    sections_df: DataFrame
        A DataFrame of Canvas Section objects.
    sync_db: sqlalchemy.engine.base.Engine
        sync db.

    Returns
    -------
    Tuple[List[Assignment], DataFrame]
        A tuple with the list of Canvas Assignment objects and the udm_assignments dataframe.
    """
    assignments: List[Assignment] = assignmentsApi.request_assignments(courses)
    assignments_df: DataFrame = assignmentsApi.assignments_synced_as_df(
        assignments, sync_db
    )
    udm_assignments_dfs: Dict[str, DataFrame] = assignmentsMap.map_to_udm_assignments(
        assignments_df, sections_df
    )

    return (assignments, udm_assignments_dfs)


def extract_submissions(
    assignments: List[Assignment],
    sections: List[Section],
    sync_db: sqlalchemy.engine.base.Engine,
) -> Dict[Tuple[str, str], DataFrame]:
    """
    Gets all Canvas submissions, in the Ed-Fi UDM format.

    Parameters
    ----------
    assignments: List[Assignment]
        A list of Canvas Assignment objects.
    sections: List[Section]
        A List of Canvas Section objects.
    sync_db: sqlalchemy.engine.base.Engine
        sync db.

    Returns
    -------
    Dict[Tuple[str, str], DataFrame]
        A dict with (section_id, assignment_id) as key and udm_submissions
        as value.
    """
    export: Dict[Tuple[str, str], DataFrame] = {}
    for section in sections:
        for assignment in [
            assignment
            for assignment in assignments
            if assignment.course_id == section.course_id
        ]:
            submissions: List[Submission] = submissionsApi.request_submissions(
                assignment
            )
            submissions_df: DataFrame = submissionsApi.submissions_synced_as_df(
                submissions, sync_db
            )
            submissions_df = submissionsMap.map_to_udm_submissions(submissions_df)
            export[(section.id, assignment.id)] = submissions_df
    return export


def extract_enrollments(
    sections: List[Section], sync_db: sqlalchemy.engine.base.Engine
) -> Tuple[List[Enrollment], Dict[str, DataFrame]]:
    """
    Gets all Canvas enrollments, in the Ed-Fi UDM format.

    Parameters
    ----------
    sections: List[Section]
        A list of Canvas Section objects.
    sync_db: sqlalchemy.engine.base.Engine
        sync db.

    Returns
    -------
    Dict[str, DataFrame]
        A dict with section_id as key and udm_enrollments as value.
    """
    udm_enrollments: Dict[str, DataFrame] = dict()
    enrollments: List[Enrollment] = []
    for section in sections:
        local_enrollments: List[Enrollment] = list(
            enrollmentsApi.request_enrollments_for_section(section)
        )
        enrollments_df: DataFrame = enrollmentsApi.enrollments_synced_as_df(
            local_enrollments, sync_db
        )
        enrollments_df = section_associationsMap.map_to_udm_section_associations(
            enrollments_df
        )
        enrollments = enrollments + local_enrollments
        udm_enrollments[section.id] = enrollments_df

    return (enrollments, udm_enrollments)


def extract_grades(
    enrollments: List[Enrollment],
    udm_enrollments: Dict[str, DataFrame],
    sections: List[Section],
) -> Dict[str, DataFrame]:
    """
    Gets all Canvas enrollments, in the Ed-Fi UDM format.

    Parameters
    ----------
    enrollments: List[Enrollment]
        A list of Canvas Enrollment objects.
    udm_enrollments: Dict[str, DataFrame]
        A dict of udm enrollments with section_id as the key and DartaFrame as value.
    sections: List[Section]
        A list of Canvas Section objects.

    Returns
    -------
    Dict[str, DataFrame]
        A dict with section_id as key and DataFrame as value.
    """
    output: Dict[str, DataFrame] = {}

    for section in sections:
        current_grades: List[dict] = []
        udm_enrollments_list: List[dict] = udm_enrollments[section.id].to_dict(
            "records"
        )

        for enrollment in [
            enrollment
            for enrollment in enrollments
            if enrollment.type == "StudentEnrollment"
            and enrollment.course_section_id == section.id
        ]:
            grade: dict = enrollment.grades
            current_udm_enrollment = [
                first_enrollment
                for first_enrollment in udm_enrollments_list
                if first_enrollment["SourceSystemIdentifier"] == str(enrollment.id)
            ][0]
            grade["SourceSystemIdentifier"] = f"g#{enrollment.id}"
            grade["LMSUserIdentifier"] = current_udm_enrollment[
                "LMSUserSourceSystemIdentifier"
            ]
            grade["LMSSectionIdentifier"] = section.id
            grade["LMSGradeIdentifier"] = grade["SourceSystemIdentifier"]
            grade["CreateDate"] = current_udm_enrollment["CreateDate"]
            grade["LastModifiedDate"] = current_udm_enrollment["LastModifiedDate"]
            current_grades.append(grade)

        output[section.id] = gradesMap.map_to_udm_grades(DataFrame(current_grades))

    return output


def extract_system_activities(
    users: List[User],
    start_date: str,
    end_date: str,
    sync_db: sqlalchemy.engine.base.Engine,
) -> DataFrame:
    """
    Gets all Canvas students, in the Ed-Fi UDM format.

    Parameters
    ----------
    users: List[User]
        A list of Canvas User objects.
    start_date: str
        The start date for the events.
    end_date: str
        The end date for the events.
    sync_db: sqlalchemy.engine.base.Engine,
        sync db.

    Returns
    -------
    DataFrame
        A Dataframe with udm_system_activities.
    """
    def _get_authentication_events():
        auth_events: List[User] = authEventsApi.request_events(users, start_date, end_date)
        for event in auth_events:
            user_id = event.links['user']
            event.id = f"{user_id}#{event.created_at}"
        auth_events = authEventsApi.authentication_events_synced_as_df(auth_events, sync_db)
        #  TODO: add mapping
        return auth_events

    return _get_authentication_events()
