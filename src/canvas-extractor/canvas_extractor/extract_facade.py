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

from canvas_extractor.api.courses import courses_synced_as_df, request_courses
from canvas_extractor.api.sections import sections_synced_as_df, request_sections
from canvas_extractor.mapping.sections import map_to_udm_sections
from canvas_extractor.api.students import request_students, students_synced_as_df
from canvas_extractor.mapping.users import map_to_udm_users
from canvas_extractor.api.assignments import (
    assignments_synced_as_df,
    request_assignments,
)
from canvas_extractor.mapping.assignments import map_to_udm_assignments
from canvas_extractor.api.submissions import (
    request_submissions,
    submissions_synced_as_df,
)
from canvas_extractor.mapping.submissions import map_to_udm_submissions
from canvas_extractor.api.enrollments import (
    enrollments_synced_as_df,
    request_enrollments_for_section,
)
from canvas_extractor.mapping.section_associations import (
    map_to_udm_section_associations,
)


def extract_courses(
    canvas: Canvas, sync_db: sqlalchemy.engine.base.Engine
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
    courses: List[Course] = request_courses(canvas)
    courses_df: DataFrame = courses_synced_as_df(courses, sync_db)

    return (courses, courses_df)


def extract_sections(
    courses: List[Course],
    sync_db: sqlalchemy.engine.base.Engine
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
    sections: List[Section] = request_sections(courses)
    sections_df: DataFrame = sections_synced_as_df(sections, sync_db)
    udm_sections_df: DataFrame = map_to_udm_sections(sections_df)

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
    students: List[User] = request_students(courses)
    students_df: DataFrame = students_synced_as_df(students, sync_db)
    udm_students_df: DataFrame = map_to_udm_users(students_df)

    return (students, udm_students_df)


def extract_assignments(
    courses: List[Course],
    sections_df: DataFrame,
    sync_db: sqlalchemy.engine.base.Engine,
) -> Tuple[List[Assignment], DataFrame]:
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
    assignments: List[Assignment] = request_assignments(courses)
    assignments_df: DataFrame = assignments_synced_as_df(assignments, sync_db)
    udm_assignments_dfs: Dict[str, DataFrame] = map_to_udm_assignments(
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
            submissions: List[Submission] = request_submissions(assignment)
            submissions_df: DataFrame = submissions_synced_as_df(submissions, sync_db)
            submissions_df = map_to_udm_submissions(submissions_df)
            export[(section.id, assignment.id)] = submissions_df
    return export


def extract_enrollments(
    sections: List[Section], sync_db: sqlalchemy.engine.base.Engine
) -> Dict[str, DataFrame]:
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
    output: Dict[str, DataFrame] = dict()
    for section in sections:
        enrollments: List[Enrollment] = request_enrollments_for_section(section)
        enrollments_df: DataFrame = enrollments_synced_as_df(enrollments, sync_db)
        enrollments_df = map_to_udm_section_associations(enrollments_df)
        output[section.id] = enrollments_df

    return output
