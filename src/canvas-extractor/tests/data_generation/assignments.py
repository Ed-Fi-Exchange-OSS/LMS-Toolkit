# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from canvasapi.course import Course
from canvasapi.assignment import Assignment
from typing import Dict, List
from faker import Faker

fake = Faker("en_US")
logger = logging.getLogger(__name__)


def generate_assignments(record_count: int) -> List[Dict]:
    """
    Generate a list of Canvas assignments.

    Parameters
    ----------
    record_count : int
        The number of assignments to generate.

    Returns
    -------
    List[Dict]
        A list of JSON-like section objects in a form suitable for submission to the
        Canvas assignment create endpoint.
    """
    assert record_count > 0, "Number of assignments to generate must be greater than zero"

    logging.info(f"Generating {record_count} assignments")
    assignments = []
    for i in range(1, record_count + 1):
        if i % 1000 == 0:
            logging.info(f"{i} assignments...")
        assignments.append(
            {
                "name": fake.catch_phrase(),
            }
        )
    return assignments


def rollback_loaded_assignments(assignments: List[Assignment]):
    """
    Delete already loaded assignments via the Canvas API.
    **** Used during testing of the load functionality ****

    Parameters
    ----------
    assignments: List[Assignment]
        A list of Assignment SDK objects from a successful load operation
    """
    logger.info(
        "**** Rolling back %s assignments via Canvas API - for testing purposes",
        len(assignments),
    )

    for assignment in assignments:
        assignment.delete()

    logger.info("**** Successfully deleted %s assignments", len(assignments))


def load_assignments(course: Course, assignments: List[Dict]) -> List[Assignment]:
    """
    Load a list of assignments via the Canvas API.

    Parameters
    ----------
    course: Course
        A Course SDK object
    assignments: List[Dict]
        A list of JSON-like assignment objects in a form suitable for submission to the
        Canvas assignment creation endpoint.

    Returns
    -------
    List[Assignment]
        A list of Canvas SDK Assignment objects representing the created assignments
    """
    logger.info("Creating %s assignments via Canvas API", len(assignments))

    result: List[Assignment] = []
    for assignment in assignments:
        result.append(course.create_assignment(assignment))

    logger.info("Successfully created %s assignments", len(assignments))
    return result


def generate_and_load_assignments(
    courses: List[Course], record_count: int
) -> Dict[Course, List[Assignment]]:
    """
    Generate and load a number of assignments into the Canvas API.

    Parameters
    ----------
    courses: List[Course]
        A list of Course SDK object already initialized
    record_count : int
        The number of sections to generate per course.

    Returns
    -------
    Dict[Course, List[Assignment]]
        A list of Canvas SDK Assignment objects representing the created assignments,
        grouped by Course SDK object
    """
    assert (
        record_count > 0
    ), "Number of assignments per course to generate must be greater than zero"

    result: Dict[Course, List[Assignment]] = {}

    for course in courses:
        try:
            assignments_dict: List[Dict] = generate_assignments(record_count)
            assignments_list: List[Assignment] = load_assignments(course, assignments_dict)
            result[course] = assignments_list
        except Exception as ex:
            logger.exception(ex)

    return result
