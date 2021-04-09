# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from pandas import DataFrame, json_normalize, merge
from typing import Dict, List
from faker import Faker
from tests.data_generation.generation_helper import validate_multi_status
from edfi_schoology_extractor.api.request_client import RequestClient

fake = Faker("en_US")
logger = logging.getLogger(__name__)


def generate_sections(record_count: int, grading_period_ids: List[int]) -> List[Dict]:
    """
    Generate a list of Schoology sections.

    Parameters
    ----------
    record_count : int
        The number of sections to generate.

    grading_periods : List[int]
        All valid grading period ids.


    Returns
    -------
    List[Dict]
        A list of JSON-like section objects in a form suitable for submission to the
        Schoology section create endpoint.
    """
    assert record_count > 0, "Number of sections to generate must be greater than zero"

    logging.info(f"Generating {record_count} sections")
    sections = []
    for i in range(1, record_count + 1):
        if i % 1000 == 0:
            logging.info(f"{i} sections...")
        sections.append(
            {
                "title": fake.catch_phrase(),
                "description": fake.sentence(),
                "section_school_code": str(fake.random_number(digits=8)),
                "grading_periods": grading_period_ids,
            }
        )
    return sections


def rollback_loaded_sections(
    request_client: RequestClient, creation_response: List[Dict]
):
    """
    Delete already loaded sections via the Schoology API.
    **** Used during testing of the load functionality ****

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    creation_response: List[Dict]
        A list of JSON-like response objects from a successful section load operation
    """
    logger.info(
        "**** Rolling back %s sections via Schoology API - for testing purposes",
        len(creation_response),
    )

    ids: str = ",".join(map(lambda section: str(section["id"]), creation_response))

    delete_response = request_client.bulk_delete("sections", f"section_ids={ids}")[
        "section"
    ]

    validate_multi_status(delete_response)
    logger.info("**** Successfully deleted %s sections", len(delete_response))


def load_sections(
    request_client: RequestClient, course_id: str, sections: List[Dict]
) -> List[Dict]:
    """
    Load a list of sections for a course via the Schoology API.

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    course_id : str
        The Schoolgy internal course id the sections are to be associated with
    sections: List[Dict]
        A list of JSON-like section objects in a form suitable for submission to the
        Schoology section creation endpoint.

    Returns
    -------
    List[Dict]
        A list of JSON-like section objects incorporating the response values from the
        Schoology API, e.g. resource ids and status from individual POSTing
    """
    assert (
        len(sections) > 0 and len(sections) < 51
    ), "Number of sections must be between 1 and 50"

    logger.info("Creating %s sections via Schoology API", len(sections))

    sections_json = {"sections": {"section": sections}}
    post_response: List[Dict] = request_client.bulk_post(
        f"courses/{course_id}/sections", sections_json
    )["section"]
    validate_multi_status(post_response)
    logger.info("Successfully created %s sections", len(post_response))

    with_schoology_response_df: DataFrame = merge(
        json_normalize(sections),
        json_normalize(post_response).drop(
            ["section_school_code", "grading_periods"], axis=1
        ),
        left_index=True,
        right_index=True,
    )

    return with_schoology_response_df.to_dict("records")


def generate_and_load_sections(
    request_client: RequestClient,
    record_count: int,
    courses: List[Dict],
    grading_periods: List[Dict],
) -> List[Dict]:
    """
    Generate and load a number of sections into the Schoology API.

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    record_count : int
        The number of sections to generate per course.

    Returns
    -------
    List[Dict]
        A list of JSON-like section objects incorporating the response values from the
        Schoology API, e.g. resource ids and status from individual POSTing
    """
    assert (
        record_count > 0
    ), "Number of sections to generate per course must be greater than zero"
    assert (
        record_count < 51
    ), "Number of sections to generate per course must be less then 51"

    course_ids: List[str] = list(map(lambda course: str(course["id"]), courses))
    grading_period_ids: List[int] = list(map(lambda gp: int(gp["id"]), grading_periods))

    result: List[Dict] = []
    for course_id in course_ids:
        try:
            course_sections: List[Dict] = generate_sections(
                record_count, grading_period_ids
            )
            section_result = load_sections(request_client, course_id, course_sections)
            result.extend(section_result)
        except Exception as ex:
            logger.exception(ex)

    return result
