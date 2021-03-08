# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from canvasapi.course import Course
from canvasapi.section import Section
from typing import Dict, List
from faker import Faker

fake = Faker("en_US")
logger = logging.getLogger(__name__)


def generate_sections(record_count: int) -> List[Dict]:
    """
    Generate a list of Canvas sections.

    Parameters
    ----------
    record_count : int
        The number of sections to generate.

    Returns
    -------
    List[Dict]
        A list of JSON-like section objects in a form suitable for submission to the
        Canvas section create endpoint.
    """
    assert record_count > 0, "Number of sections to generate must be greater than zero"

    logging.info(f"Generating {record_count} sections")
    sections = []
    for i in range(1, record_count + 1):
        if i % 1000 == 0:
            logging.info(f"{i} sections...")
        sections.append(
            {
                "course_section[name]": fake.catch_phrase(),
            }
        )
    return sections


def rollback_loaded_sections(sections: List[Section]):
    """
    Delete already loaded sections via the Canvas API.
    **** Used during testing of the load functionality ****

    Parameters
    ----------
    sections: List[Section]
        A list of Section SDK objects from a successful load operation
    """
    logger.info(
        "**** Rolling back %s sections via Canvas API - for testing purposes",
        len(sections),
    )

    for section in sections:
        section.delete()

    logger.info("**** Successfully deleted %s sections", len(sections))


def load_sections(course: Course, sections: List[Dict]) -> List[Section]:
    """
    Load a list of sections for a course via the Canvas API.

    Parameters
    ----------
    course: Course
        A Course SDK object
    sections: List[Dict]
        A list of JSON-like section objects in a form suitable for submission to the
        Canvas section creation endpoint.

    Returns
    -------
    List[Section]
        A list of Canvas SDK Section objects representing the created sections
    """
    logger.info("Creating %s sections via Canvas API", len(sections))

    result: List[Section] = []
    for section in sections:
        result.append(course.create_course_section(**section))

    logger.info("Successfully created %s sections", len(sections))

    return result


def generate_and_load_sections(
    courses: List[Course], record_count: int
) -> Dict[Course, List[Section]]:
    """
    Generate and load a number of sections into the Canvas API.

    Parameters
    ----------
    courses: List[Course]
        A list of Course SDK object already initialized
    record_count : int
        The number of sections to generate per course.

    Returns
    -------
    Dict[Course, List[Section]]
        A list of Canvas SDK Section objects representing the created sections,
        grouped by Course SDK object
    """
    assert (
        record_count > 0
    ), "Number of sections to generate per course must be greater than zero"

    result: Dict[Course, List[Section]] = {}
    for course in courses:
        try:
            sections_dict: List[Dict] = generate_sections(record_count)
            section_list: List[Section] = load_sections(course, sections_dict)
            result[course] = section_list
        except Exception as ex:
            logger.exception(ex)

    return result
