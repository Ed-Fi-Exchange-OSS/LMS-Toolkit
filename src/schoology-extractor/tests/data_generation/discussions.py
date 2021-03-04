# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import Dict, List
from faker import Faker
from edfi_schoology_extractor.api.request_client import RequestClient

fake = Faker("en_US")
logger = logging.getLogger(__name__)


def generate_discussions(
    discussions_per_assignment_count: int, assignments: Dict[str, List[Dict]]
) -> Dict[str, List[Dict]]:
    """
    Generate a list of graded Schoology discussions for assignments.

    Parameters
    ----------
    discussions_per_assignment_count : int
         The number of discussions per assignment to generate
    assignments: Dict[str, List[Dict]]
        A Dict of mappings from Schoology section id to a list of JSON-like
        assignment objects from a bulk create response

    Returns
    -------
    Dict[str, List[Dict]]
        A Dict of mappings from Schoology section id to a list of JSON-like discussion objects
        in a form suitable for submission to the Schoology discussion create endpoint.
    """
    assert (
        discussions_per_assignment_count > 0
    ), "Number of discussions per section to generate must be greater than zero"

    logging.info(
        f"Generating {discussions_per_assignment_count} discussions per section"
    )
    discussions: Dict[str, List[Dict]] = {}
    for section_id, assignments_for_section in assignments.items():
        for assignment in assignments_for_section:
            discussions_per_assignment: List[Dict] = []
            for _ in range(1, discussions_per_assignment_count + 1):
                discussions_per_assignment.append(
                    {
                        "title": fake.catch_phrase(),
                        "body": fake.sentence(),
                        "graded": "0",
                    }
                )
            discussions[section_id] = discussions_per_assignment
    return discussions


def rollback_loaded_discussions(
    request_client: RequestClient, response_dict: Dict[str, List[Dict]]
):
    """
    Delete already loaded discussions via the Schoology API.
    **** Used during testing of the load functionality ****

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    response_dict: Dict[str, List[Dict]]
        A Dict of mappings from Schoology section id to a list of JSON-like response objects
        from a successful discussion load operation
    """
    logger.info(
        "**** Rolling back discussions via Schoology API - for testing purposes"
    )
    for section_id, creation_response in response_dict.items():
        logger.info(
            "**** Deleting %s discussions for section %s",
            len(creation_response),
            section_id,
        )

        ids: List[str] = list(
            map(lambda discussion: str(discussion["id"]), creation_response)
        )

        for id in ids:
            request_client.delete(f"sections/{section_id}/discussions", id)
            logger.info("**** Deleted discussion with id %s", id)

        logger.info("**** Successfully deleted %s discussions", len(ids))


def load_discussions(
    request_client: RequestClient, section_id: str, discussions: List[Dict]
) -> List[Dict]:
    """
    Load a list of discussions via the Schoology API.

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    section_id: str
        The Schoology id of the section that the discussions are associated with
    discussions: List[Dict]
        A list of JSON-like discussion objects in a form suitable for submission
        to the Schoology discussion create endpoint.

    Returns
    -------
    List[Dict]
        A list of JSON-like discussion objects incorporating the response values from the
        Schoology API, e.g. resource ids and status from individual POSTing
    """
    logger.info("Creating %s discussions via Schoology API", len(discussions))

    post_responses: List[Dict] = []
    for discussion in discussions:
        response: Dict = request_client.post(
            f"sections/{section_id}/discussions", discussion
        )
        post_responses.append(response)

    logger.info("Successfully created %s discussions", len(post_responses))
    return post_responses


def generate_and_load_discussions(
    request_client: RequestClient,
    discussions_per_assignment_count: int,
    assignments: Dict[str, List[Dict]],
) -> Dict[str, List[Dict]]:
    """
    Generate and load a number of discussions into the Schoology API.

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    discussions_per_assignment_count : int
         The number of discussions per assignment to generate
    assignments: Dict[str, List[Dict]]
        A Dict of mappings from Schoology section id to a list of JSON-like
        assignment objects from a bulk create response

    Returns
    -------
    Dict[str, List[Dict]]
         A Dict of mappings from Schoology section id to a list of JSON-like discussion
         objects incorporating the response values from the Schoology API,
         e.g. resource ids and status from individual POSTing
    """
    assert (
        discussions_per_assignment_count > 0
    ), "Number of discussions per assignment to generate must be greater than zero"

    discussion_per_section: Dict[str, List[Dict]] = generate_discussions(
        discussions_per_assignment_count, assignments
    )

    result: Dict[str, List[Dict]] = {}
    for section_id, total_discussions_per_section in discussion_per_section.items():
        MAX_CHUNK_SIZE = 50
        chunked_discussions: List[List[Dict]] = [
            total_discussions_per_section[x : x + MAX_CHUNK_SIZE]
            for x in range(0, len(total_discussions_per_section), MAX_CHUNK_SIZE)
        ]

        result[section_id] = []
        for discussion_chunk in chunked_discussions:
            try:
                chunked_result = load_discussions(
                    request_client, section_id, discussion_chunk
                )
                result[section_id].extend(chunked_result)
            except Exception as ex:
                logger.exception(ex)

    return result
