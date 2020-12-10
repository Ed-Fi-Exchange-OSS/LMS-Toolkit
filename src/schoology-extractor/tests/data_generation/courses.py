# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from pandas import DataFrame, json_normalize, merge
from typing import Dict, List
from faker import Faker
from tests.data_generation.generation_helper import validate_multi_status
from schoology_extractor.api.request_client import RequestClient

fake = Faker("en_US")
logger = logging.getLogger(__name__)


def generate_courses(record_count: int) -> List[Dict]:
    """
    Generate a list of Schoology courses.

    Parameters
    ----------
    record_count : int
        The number of courses to generate.

    Returns
    -------
    List[Dict]
        A list of JSON-like course objects in a form suitable for submission to the
        Schoology course create endpoint.
    """
    assert record_count > 0, "Number of courses to generate must be greater than zero"

    logging.info(f"Generating {record_count} courses")
    courses = []
    for i in range(1, record_count + 1):
        if i % 1000 == 0:
            logging.info(f"{i} courses...")
        courses.append(
            {
                "title": fake.catch_phrase(),
                "description": fake.sentence(),
                "course_code": fake.bothify("?###"),
                "department": " ".join(fake.words(2)),
            }
        )
    return courses


def rollback_loaded_courses(
    request_client: RequestClient, creation_response: List[Dict]
):
    """
    Delete already loaded courses via the Schoology API.
    **** Used during testing of the load functionality ****

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    creation_response: List[Dict]
        A list of JSON-like response objects from a successful course load operation
    """
    logger.info(
        "**** Rolling back %s courses via Schoology API - for testing purposes",
        len(creation_response),
    )

    ids: List[str] = list(map(lambda course: str(course["id"]), creation_response))

    for id in ids:
        request_client.delete("courses", id)
        logger.info("**** Deleted course with id %s", id)

    logger.info("**** Successfully deleted %s courses", len(ids))


def load_courses(request_client: RequestClient, courses: List[Dict]) -> List[Dict]:
    """
    Load a list of courses via the Schoology API.

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    courses: List[Dict]
        A list of JSON-like course objects in a form suitable for submission to the
        Schoology course creation endpoint.

    Returns
    -------
    List[Dict]
        A list of JSON-like course objects incorporating the response values from the
        Schoology API, e.g. resource ids and status from individual POSTing
    """
    assert (
        len(courses) > 0 and len(courses) < 51
    ), "Number of courses must be between 1 and 50"

    logger.info("Creating %s courses via Schoology API", len(courses))

    courses_json = {"courses": {"course": courses}}
    post_response: List[Dict] = request_client.bulk_post("courses", courses_json)[
        "course"
    ]
    validate_multi_status(post_response)
    logger.info("Successfully created %s courses", len(post_response))

    with_schoology_response_df: DataFrame = merge(
        json_normalize(courses),
        json_normalize(post_response).drop("course_code", axis=1),
        left_index=True,
        right_index=True,
    )

    return with_schoology_response_df.to_dict("records")


def generate_and_load_courses(
    request_client: RequestClient, record_count: int
) -> List[Dict]:
    """
    Generate and load a number of courses into the Schoology API.

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    record_count : int
        The number of courses to generate.

    Returns
    -------
    List[Dict]
        A list of JSON-like course objects incorporating the response values from the
        Schoology API, e.g. resource ids and status from individual POSTing
    """
    assert record_count > 0, "Number of courses to generate must be greater than zero"

    total_courses: List[Dict] = generate_courses(record_count)

    MAX_CHUNK_SIZE = 50
    chunked_courses: List[List[Dict]] = [
        total_courses[x : x + MAX_CHUNK_SIZE]
        for x in range(0, len(total_courses), MAX_CHUNK_SIZE)
    ]

    result: List[Dict] = []
    for course_chunk in chunked_courses:
        chunked_result = load_courses(request_client, course_chunk)
        result.extend(chunked_result)
    return result
