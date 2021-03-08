# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from canvasapi.enrollment import Enrollment
from canvasapi.course import Course
from canvasapi.section import Section
from canvasapi.user import User
from typing import Dict, List
from faker import Faker

fake = Faker("en_US")
logger = logging.getLogger(__name__)


def rollback_loaded_enrollments(enrollments: List[Enrollment]):
    """
    Delete already loaded enrollments via the Canvas API.
    **** Used during testing of the load functionality ****

    Parameters
    ----------
    enrollments: List[Enrollment]
        A list of Enrollment SDK objects from a successful load operation
    """
    logger.info(
        "**** Rolling back %s enrollments via Canvas API - for testing purposes",
        len(enrollments),
    )

    for enrollment in enrollments:
        enrollment.deactivate("delete")

    logger.info("**** Successfully deleted %s enrollments", len(enrollments))


def load_enrollments(course: Course, enrollments: List[Dict]) -> List[Enrollment]:
    """
    Load a list of enrollments for a course via the Canvas API.

    Parameters
    ----------
    course: Course
        A Course SDK object
    enrollments: List[Dict]
        A list of JSON-like enrollment objects in a form suitable for submission to the
        Canvas enrollment creation endpoint.

    Returns
    -------
    List[Enrollment]
        A list of Canvas SDK Enrollment objects representing the created enrollments
    """
    logger.info("Creating %s enrollments via Canvas API", len(enrollments))

    result: List[Enrollment] = []
    for enrollment in enrollments:
        result.append(
            course.enroll_user(
                enrollment["user"],
                enrollment["enrollment_type"],
                **enrollment["enrollment"]
            )
        )

    logger.info("Successfully created %s enrollments", len(enrollments))

    return result


def generate_and_load_enrollments(
    users: List[User],
    sections_by_course: Dict[Course, List[Section]],
    users_per_section_count: int,
) -> Dict[Course, List[Enrollment]]:
    """
    Generate and load a number of enrollments into the Canvas API.

    Parameters
    ----------
    users: List[User]
        A list of User SDK objects
    users_per_section_count : int
        The number of users to be in each section
    sections_by_course: Dict[Course, List[Section]]
        A list of Canvas SDK Section objects, grouped by Course SDK object

    Returns
    -------
    Dict[Course, List[Enrollment]]
        A list of Canvas SDK Enrollment objects representing the created enrollments,
        grouped by Course SDK object
    """
    result: Dict[Course, List[Enrollment]] = {}

    for course, section_list in sections_by_course.items():
        for section in section_list:
            try:
                users_in_section = fake.random_sample(
                    elements=users, length=users_per_section_count
                )
                enrollments = list(
                    map(
                        lambda user: {
                            "user": user,
                            "enrollment_type": "StudentEnrollment",
                            "enrollment": {
                                "enrollment[course_section_id]": section.id,
                                "enrollment[enrollment_state]": "active",
                            },
                        },
                        users_in_section,
                    )
                )

                enrollments_list: List[Enrollment] = load_enrollments(course, enrollments)
                result[course] = enrollments_list
            except Exception as ex:
                logger.exception(ex)

    return result
