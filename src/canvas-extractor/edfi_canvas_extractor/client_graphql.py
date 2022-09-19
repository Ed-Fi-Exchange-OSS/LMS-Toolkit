# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import sqlalchemy

from pandas import DataFrame
from typing import Dict, List, Tuple

from canvasapi.course import Course
from canvasapi.enrollment import Enrollment
from canvasapi.section import Section
from canvasapi.user import User

from edfi_canvas_extractor.graphql.extractor import GraphQLExtractor
from edfi_canvas_extractor.graphql import (
    courses as coursesGQL,
    enrollments as enrollmentsGQL,
    sections as sectionsGQL,
    students as studentsGQL,
)
from edfi_canvas_extractor.mapping import (
    sections as sectionsMap,
    section_associations as section_associationsMap,
    users as usersMap,
)


logger = logging.getLogger(__name__)


def extract_courses(
    gql: GraphQLExtractor,
    sync_db: sqlalchemy.engine.base.Engine,
) -> Tuple[List[Course], DataFrame]:
    """
    Gets all Canvas courses in the Ed-Fi UDM format.

    Parameters
    ----------
    gql: GraphQLExtractor
        Adapter for running GraphQL commands on Canvas.
    sync_db: sqlalchemy.engine.base.Engine
        Sync database connection.

    Returns
    -------
    Tuple[List[Course], DataFrame]
        A tuple with the list of Canvas Course objects and the udm_courses dataframe.
    """
    courses: List[Course] = gql.courses
    courses_df: DataFrame = coursesGQL.courses_synced_as_df(courses, sync_db)

    return (courses, courses_df)


def extract_sections(
    gql: GraphQLExtractor,
    sync_db: sqlalchemy.engine.base.Engine
) -> Tuple[List[Section], DataFrame, List[str]]:
    """
    Gets all Canvas sections, in the Ed-Fi UDM format.

    Parameters
    ----------
    gql: GraphQLExtractor
        Adapter for running GraphQL commands on Canvas.
    sync_db: sqlalchemy.engine.base.Engine
        Sync database connection.

    Returns
    -------
    Tuple[List[Section], DataFrame, List[str]]
        A tuple with the list of Canvas Section objects, the udm_sections dataframe,
        and a list of all section ids as strings.
    """
    sections: List[Section] = gql.get_sections()
    sections_df: DataFrame = sectionsGQL.sections_synced_as_df(sections, sync_db)
    udm_sections_df: DataFrame = sectionsMap.map_to_udm_sections(sections_df)
    section_ids = udm_sections_df["SourceSystemIdentifier"].astype("string").tolist()
    return (sections, udm_sections_df, section_ids)


def extract_students(
    gql: GraphQLExtractor,
    sync_db: sqlalchemy.engine.base.Engine
) -> Tuple[List[User], DataFrame]:
    """
    Gets all Canvas students, in the Ed-Fi UDM format.

    Parameters
    ----------
    gql: GraphQLExtractor
        Adapter for running GraphQL commands on Canvas.
    sync_db: sqlalchemy.engine.base.Engine
        Sync database connection.

    Returns
    -------
    Tuple[List[User], DataFrame]
        A tuple with the list of Canvas User objects and the udm_users dataframe.
    """
    students: List[User] = gql.get_students()
    students_df: DataFrame = studentsGQL.students_synced_as_df(students, sync_db)
    udm_students_df: DataFrame = usersMap.map_to_udm_users(students_df)

    return (students, udm_students_df)


def extract_enrollments(
    gql: GraphQLExtractor,
    sections: List,
    sync_db: sqlalchemy.engine.base.Engine
) -> Tuple[List[Enrollment], Dict[str, DataFrame]]:
    """
    Gets all Canvas enrollments, in the Ed-Fi UDM format.

    Parameters
    ----------
    gql: GraphQLExtractor
        Adapter for running GraphQL commands on Canvas.
    sync_db: sqlalchemy.engine.base.Engine
        Sync database connection.

    Returns
    -------
    Dict[str, DataFrame]
        A dict with section_id as key and udm_enrollments as value.
    """
    udm_enrollments: Dict[str, DataFrame] = dict()
    enrollments: List[Enrollment] = []
    enrollments = gql.get_enrollments()
    for section in sections:
        local_enrollments = [
            enrollment for enrollment in enrollments if enrollment["course_section_id"] == section
        ]
        filtered_enrollments = [
            enrollment
            for enrollment in local_enrollments
            if enrollment["enrollment_state"] == "active"
            ]
        if len(list(filtered_enrollments)) < 1:
            logger.info(
                "There are no active section associations for section id %s.",
                section,
            )
            continue
    enrollments_df: DataFrame = enrollmentsGQL.enrollments_synced_as_df(
        local_enrollments, sync_db
    )
    enrollments_df = section_associationsMap.map_to_udm_section_associations(
        enrollments_df
    )
    enrollments = enrollments + filtered_enrollments
    udm_enrollments[str(section)] = enrollments_df

    return (enrollments, udm_enrollments)
