# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import sqlalchemy

from pandas import DataFrame
from typing import Dict, List, Tuple

from edfi_canvas_extractor.graphql.extractor import GraphQLExtractor
from edfi_canvas_extractor.graphql import (
    assignments as assignmentsGQL,
    courses as coursesGQL,
    enrollments as enrollmentsGQL,
    sections as sectionsGQL,
    submissions as submissionsGQL,
    students as studentsGQL,
)
from edfi_canvas_extractor.mapping import (
    assignments as assignmentsMap,
    grades as gradesMap,
    sections as sectionsMap,
    section_associations as section_associationsMap,
    submissions as submissionsMap,
    users as usersMap,
)


logger = logging.getLogger(__name__)


def extract_courses(
    gql: GraphQLExtractor,
    sync_db: sqlalchemy.engine.base.Engine,
) -> Tuple[List[Dict[str, str]], DataFrame]:
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
    Tuple[List[Dict[str, str]], DataFrame]
        A tuple with the list of Canvas Course objects and the udm_courses dataframe.
    """
    courses: List[Dict[str, str]] = gql.courses
    courses_df: DataFrame = coursesGQL.courses_synced_as_df(courses, sync_db)

    return (courses, courses_df)


def extract_sections(
    gql: GraphQLExtractor,
    sync_db: sqlalchemy.engine.base.Engine
) -> Tuple[List[Dict[str, str]], DataFrame, List[str]]:
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
    Tuple[List[Dict[str, str]], DataFrame, List[str]]
        A tuple with the list of Canvas Section objects, the udm_sections dataframe,
        and a list of all section ids as strings.
    """
    sections: List[Dict[str, str]] = gql.get_sections()
    sections_df: DataFrame = sectionsGQL.sections_synced_as_df(sections, sync_db)
    udm_sections_df: DataFrame = sectionsMap.map_to_udm_sections(sections_df)
    section_ids = udm_sections_df["SourceSystemIdentifier"].astype("string").tolist()
    return (sections, udm_sections_df, section_ids)


def extract_students(
    gql: GraphQLExtractor,
    sync_db: sqlalchemy.engine.base.Engine
) -> Tuple[List[Dict[str, str]], DataFrame]:
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
    Tuple[List[Dict[str, str]], DataFrame]
        A tuple with the list of Canvas User objects and the udm_users dataframe.
    """
    students: List[Dict[str, str]] = gql.get_students()
    students_df: DataFrame = studentsGQL.students_synced_as_df(students, sync_db)
    udm_students_df: DataFrame = usersMap.map_to_udm_users(students_df)

    return (students, udm_students_df)


def extract_enrollments(
    gql: GraphQLExtractor,
    sections: List,
    sync_db: sqlalchemy.engine.base.Engine
) -> Tuple[List[Dict[str, str]], Dict[str, DataFrame]]:
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
    enrollments = gql.get_enrollments()

    for section in sections:
        local_enrollments = [
            enrollment
            for enrollment in enrollments
            if enrollment["course_section_id"] == section
            and enrollment["enrollment_state"] in ["active", "invited"]
        ]
        if len(list(local_enrollments)) < 1:
            logger.info(
                f"There are no active section associations for section id {section}."
            )
            continue
        enrollments_df: DataFrame = enrollmentsGQL.enrollments_synced_as_df(
            local_enrollments, sync_db
        )
        enrollments_df = section_associationsMap.map_to_udm_section_associations(
            enrollments_df
        )
        udm_enrollments[str(section)] = enrollments_df

    return (enrollments, udm_enrollments)


def extract_assignments(
    sections_df: DataFrame,
    gql: GraphQLExtractor,
    sync_db: sqlalchemy.engine.base.Engine,
) -> Tuple[List[Dict[str, str]], Dict[str, DataFrame]]:
    """
    Gets all Canvas assignments, in the Ed-Fi UDM format.
    Parameters
    ----------
    sections_df: DataFrame
        A DataFrame of Section dictionaries.
    gql: GraphQLExtractor
        Adapter for running GraphQL commands on Canvas.
    sync_db: sqlalchemy.engine.base.Engine
        Sync database connection.
    Returns
    -------
    Tuple[List[Dict[str, str]], DataFrame]
        A tuple with the list of Canvas Assignment objects and the udm_assignments dataframe.
    """
    assignments: List[Dict[str, str]] = gql.get_assignments()
    if len(list(assignments)) < 1:
        logger.info("Skipping assignments - No data returned by API")
        return ([], {})
    assignments_df: DataFrame = assignmentsGQL.assignments_synced_as_df(
        assignments, sync_db
    )
    udm_assignments_dfs: Dict[str, DataFrame] = assignmentsMap.map_to_udm_assignments(
        assignments_df, sections_df
    )

    return (assignments, udm_assignments_dfs)


def extract_submissions(
    gql: GraphQLExtractor,
    sync_db: sqlalchemy.engine.base.Engine,
) -> Dict[Tuple[str, str], DataFrame]:
    """
    Gets all Canvas submissions for sections, in the Ed-Fi UDM format.
    Parameters
    ----------
    sections: List[Dict[str, str]]
        A List of Section dictionaries.
    sync_db: sqlalchemy.engine.base.Engine
        Sync database connection.
    Returns
    -------
    Dict[Tuple[str, str], DataFrame]
        A dict with (section_id, assignment_id) as key and udm_submissions
        as value.
    """
    export: Dict[Tuple[str, str], DataFrame] = {}
    submissions: List[Dict[str, str]] = gql.get_submissions()
    if len(list(submissions)) < 1:
        logger.info(
            "Skipping submissions for section - No data returned by API",
        )
    else:
        submissions_for_section_df: DataFrame = submissionsGQL.submissions_synced_as_df(
            submissions, sync_db
        )
        submissions_dfs_by_assignment_id = {
            assignment_id: submissions_for_section_df.loc[submissions_df]
            for assignment_id, submissions_df in submissions_for_section_df.groupby(
                "assignment_id"
            ).groups.items()
        }

        for assignment_id, submissions_df in submissions_dfs_by_assignment_id.items():
            section_id = str(submissions_df.iloc[0]['section_id'])
            assignment_source_system_identifier = f"{section_id}-{str(assignment_id)}"
            submissions_df["assignment_id"] = assignment_source_system_identifier
            submissions_df = submissionsMap.map_to_udm_submissions(submissions_df, section_id)
            export[(section_id, f"{assignment_source_system_identifier}")] = submissions_df
    return (export)


def extract_grades(
    enrollments: List[Dict[str, str]],
    udm_enrollments: Dict[str, DataFrame],
    sections: List[Dict[str, str]],
) -> Dict[str, DataFrame]:
    """
    Gets all Canvas grades, in the Ed-Fi UDM format.
    Parameters
    ----------
    enrollments: List[Dict[str, str]]
        A list of Canvas Enrollment.
    udm_enrollments: Dict[str, DataFrame]
        A dict of udm enrollments with section_id as the key and DataFrame as value.
    sections: List[Dict[str, str]]
        A list of Canvas Section.
    Returns
    -------
    Dict[str, DataFrame]
        A dict with section_id as key and UDM Grades DataFrame as value.
    """
    output: Dict[str, DataFrame] = {}

    for section in sections:
        current_grades: List[dict] = []
        section_id: str = str(section["id"])
        if section_id not in udm_enrollments:
            logger.info(
                f"Skipping enrollments for section id {section_id} - None found"
            )
            continue
        udm_enrollments_list: List[dict] = udm_enrollments[section_id].to_dict(
            "records"
        )
        for enrollment in [
            enrollment
            for enrollment in enrollments
            if enrollment["type"] == "StudentEnrollment"
            and enrollment["course_section_id"] == section["id"]
        ]:
            if "grades" not in enrollment.keys():
                continue

            find_enrollment_for_id = [
                first_enrollment
                for first_enrollment in udm_enrollments_list
                if first_enrollment["SourceSystemIdentifier"] == str(enrollment["id"])
            ]

            if len(find_enrollment_for_id) == 0:
                continue

            current_udm_enrollment = find_enrollment_for_id[0]

            grade: dict = enrollment["grades"]  # type: ignore
            enrollment_id = enrollment["id"]
            grade["SourceSystemIdentifier"] = f"g#{enrollment_id}"
            grade["LMSUserLMSSectionAssociationSourceSystemIdentifier"] = str(
                enrollment_id
            )
            grade["LMSSectionIdentifier"] = section_id
            grade["CreateDate"] = current_udm_enrollment["CreateDate"]
            grade["LastModifiedDate"] = current_udm_enrollment["LastModifiedDate"]
            current_grades.append(grade)

        output[section_id] = gradesMap.map_to_udm_grades(DataFrame(current_grades))

    return output
