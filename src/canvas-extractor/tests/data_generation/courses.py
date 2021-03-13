# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from canvasapi.course import Course
from canvasapi.account import Account
from typing import Dict, List
from faker import Faker

fake = Faker("en_US")
logger = logging.getLogger(__name__)


def generate_courses(record_count: int) -> List[Dict]:
    """
    Generate a list of Canvas courses.

    Parameters
    ----------
    record_count : int
        The number of courses to generate.

    Returns
    -------
    List[Dict]
        A list of JSON-like course objects in a form suitable for submission to the
        Canvas course create endpoint.
    """
    assert record_count > 0, "Number of courses to generate must be greater than zero"

    logging.info(f"Generating {record_count} courses")
    courses = []
    for i in range(1, record_count + 1):
        if i % 1000 == 0:
            logging.info(f"{i} courses...")
        courses.append(
            {
                "course[name]": fake.catch_phrase(),
                "course[course_code]": fake.bothify("?#######"),
                "offer": "true",
            }
        )
    return courses


def rollback_loaded_courses(courses: List[Course]):
    """
    Delete already loaded courses via the Canvas API.
    **** Used during testing of the load functionality ****

    Parameters
    ----------
    courses: List[Course]
        A list of Course SDK objects from a successful load operation
    """
    logger.info(
        "**** Rolling back %s courses via Canvas API - for testing purposes",
        len(courses),
    )

    for course in courses:
        course.delete()

    logger.info("**** Successfully deleted %s courses", len(courses))


def load_courses(account: Account, courses: List[Dict]) -> List[Course]:
    """
    Load a list of courses via the Canvas API.

    Parameters
    ----------
    account : Account
        An Account SDK object
    courses: List[Dict]
        A list of JSON-like course objects in a form suitable for submission to the
        Canvas course creation endpoint.

    Returns
    -------
    List[Course]
        A list of Canvas SDK Course objects representing the created courses
    """
    logger.info("Creating %s courses via Canvas API", len(courses))

    result: List[Course] = []
    for course in courses:
        result.append(account.create_course(**course))

    logger.info("Successfully created %s courses", len(courses))

    return result


def generate_and_load_courses(account: Account, record_count: int) -> List[Course]:
    """
    Generate and load a number of courses into the Canvas API.

    Parameters
    ----------
    canvas : Canvas
        A Canvas SDK object
    record_count : int
        The number of courses to generate.

    Returns
    -------
    List[Course]
        A list of Canvas SDK Course objects representing the created courses
    """
    assert record_count > 0, "Number of courses to generate must be greater than zero"

    courses: List[Dict] = generate_courses(record_count)

    result: List[Course] = []
    try:
        section_result = load_courses(account, courses)
        result.extend(section_result)
    except Exception as ex:
        logger.exception(ex)

    return result
