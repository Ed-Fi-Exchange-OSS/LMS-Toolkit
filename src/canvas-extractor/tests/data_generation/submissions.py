# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from canvasapi.enrollment import Enrollment
from canvasapi.submission import Submission
from canvasapi.course import Course
from canvasapi.assignment import Assignment
from typing import Dict, List
from faker import Faker

fake = Faker("en_US")
logger = logging.getLogger(__name__)


# Note: couldn't find a way to rollback submissions


def load_submissions(assignment: Assignment, submissions: List[Dict]) -> List[Submission]:
    """
    Load a list of submissions for an assignment via the Canvas API.

    Parameters
    ----------
    assignment: Assignment
        An Assignment SDK object
    submissions: List[Dict]
        A list of JSON-like submission object in a form suitable for submission to the
        Canvas submission creation endpoint.

    Returns
    -------
    List[Submission]
        A list of Canvas SDK Submission objects representing the created submissions
    """
    logger.info("Creating %s submissions via Canvas API", len(submissions))

    result: List[Submission] = []
    for submission in submissions:
        result.append(
            assignment.submit(submission)
        )

    logger.info("Successfully created %s submissions", len(submissions))

    return result


def generate_and_load_submissions(
    enrollments_by_course: Dict[Course, List[Enrollment]],
    assignments_by_course: Dict[Course, List[Assignment]],
) -> Dict[Assignment, List[Submission]]:
    """
    Generate and load a number of submissions into the Canvas API.

    Parameters
    ----------
    enrollments_by_course: Dict[Course, List[Enrollment]]
        A list of Canvas SDK Enrollment objects, grouped by Course SDK object
    assignments_by_course: Dict[Course, List[Assignment]]
        A list of Assignment SDK Section objects, grouped by Course SDK object

    Returns
    -------
    Dict[Assignment, List[Submission]]
        A list of Canvas SDK Submission objects representing the created submissions,
        grouped by Assignment SDK object
    """
    result: Dict[Assignment, List[Submission]] = {}

    for course, assignment_list in assignments_by_course.items():
        try:
            enrollments_in_course: List[Enrollment] = enrollments_by_course.get(course, [])
            for assignment in assignment_list:
                submissions = list(
                    map(
                        lambda enrollment: {
                            "submission_type": "online_url",
                            "url": fake.url(),
                            "user_id": enrollment.user_id,
                        },
                        enrollments_in_course,
                    )
                )

                submissions_list: List[Submission] = load_submissions(assignment, submissions)
                result[assignment] = submissions_list
        except Exception as ex:
            logger.exception(ex)

    return result
