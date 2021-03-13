# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from datetime import datetime
from typing import Dict, List
from faker import Faker
from edfi_schoology_extractor.api.request_client import RequestClient

fake = Faker("en_US")
logger = logging.getLogger(__name__)


def generate_assignments(
    assignment_per_section_count: int, enrollments: Dict[str, List[Dict]]
) -> Dict[str, List[Dict]]:
    """
    Generate a list of Schoology assignments.

    Parameters
    ----------
    assignments_per_section : int
        The number of assignments per section to generate.
    enrollments: List[Dict]
        A list of JSON-like section objects from a bulk create response    Returns
    -------
    Dict[str, List[Dict]]
        A Dict of mappings from Schoology section id to a list of JSON-like assignment objects
        in a form suitable for submission to the Schoology assignment create endpoint.
    """
    assert (
        assignment_per_section_count > 0
    ), "Number of assignments per section to generate must be greater than zero"

    logging.info(f"Generating {assignment_per_section_count} assignments per section")
    assignments: Dict[str, List[Dict]] = {}
    for section_id, enrollments_for_section in enrollments.items():
        assignments_per_section: List[Dict] = []
        for i in range(1, assignment_per_section_count + 1):
            if i % 100 == 0:
                logging.info(f"{i} assignments...")
            assignments_per_section.append(
                {
                    "title": fake.catch_phrase(),
                    "description": fake.sentence(),
                    "due": datetime.strftime(
                        fake.future_datetime(), "%Y-%m-%d %H:%M:%S"
                    ),
                    "type": "assignment",
                    "assignees": list(
                        map(
                            lambda enrollment: enrollment["uid"],
                            enrollments_for_section,
                        )
                    ),
                }
            )
        assignments[section_id] = assignments_per_section
    return assignments


def generate_extra_assignments_without_enrollments(
    request_client: RequestClient,
    sections: List[Dict]
) -> Dict[str, List[Dict]]:
    """
    Generate assignments without any enrollments, with random content size. One per section.

    Parameters
    ----------
    assignments_per_section : int
        The number of assignments per section to generate.
    sections: List[Dict]
        A list of JSON-like section objects from a bulk create response    Returns
    -------
    Dict[str, List[Dict]]
        A Dict of mappings from Schoology section id to a list of JSON-like assignment objects
        in a form suitable for submission to the Schoology assignment create endpoint.
    """

    logging.info("Generating extra assignment per section")

    result: Dict[str, List[Dict]] = {}
    for s in sections:
        section_id = str(s["id"])
        assignment = {
            "title": fake.catch_phrase(),
            "description": fake.paragraph(variable_nb_sentences=True, nb_sentences=40),
            "due": datetime.strftime(
                fake.future_datetime(), "%Y-%m-%d %H:%M:%S"
            ),
            "type": "assignment",
            "assignees": list(),
        }
        result[section_id] = (load_assignments(
            request_client, section_id, [assignment]
        ))

    return result


def rollback_loaded_assignments(
    request_client: RequestClient, response_dict: Dict[str, List[Dict]]
):
    """
    Delete already loaded assignments via the Schoology API.
    **** Used during testing of the load functionality ****

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    response_dict: Dict[str, List[Dict]]
        A Dict of mappings from Schoology section id to a list of JSON-like response objects
        from a successful assignment load operation
    """
    logger.info(
        "**** Rolling back assignments via Schoology API - for testing purposes"
    )
    for section_id, creation_response in response_dict.items():
        logger.info(
            "**** Deleting %s assignments for section %s",
            len(creation_response),
            section_id,
        )

        ids: List[str] = list(
            map(lambda assignment: str(assignment["id"]), creation_response)
        )

        for id in ids:
            request_client.delete(f"sections/{section_id}/assignments", id)
            logger.info("**** Deleted assignment with id %s", id)

        logger.info("**** Successfully deleted %s assignments", len(ids))


def load_assignments(
    request_client: RequestClient, section_id: str, assignments: List[Dict]
) -> List[Dict]:
    """
    Load a list of assignments via the Schoology API.

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    section_id: str
        The Schoology id of the section that the assignments are associated with
    assignments: List[Dict]
        A list of JSON-like assignment objects in a form suitable for submission to the
        Schoology assignment creation endpoint.

    Returns
    -------
    List[Dict]
        A list of JSON-like assignment objects incorporating the response values from the
        Schoology API, e.g. resource ids and status from individual POSTing
    """
    assert (
        len(assignments) > 0 and len(assignments) < 51
    ), "Number of assignments must be between 1 and 50"

    logger.info("Creating %s assignments via Schoology API", len(assignments))

    post_responses: List[Dict] = []
    for assignment in assignments:
        response: Dict = request_client.post(
            f"sections/{section_id}/assignments", assignment
        )
        post_responses.append(response)

    logger.info("Successfully created %s assignments", len(post_responses))
    return post_responses


def generate_and_load_assignments(
    request_client: RequestClient,
    assignment_per_section_count: int,
    enrollments: Dict[str, List[Dict]],
) -> Dict[str, List[Dict]]:
    """
     Generate and load a number of assignments into the Schoology API.

     Parameters
     ----------
     request_client : RequestClient
         A RequestClient initialized for access to the Schoology API
     assignment_per_section_count : int
         The number of assignments per section to generate
     enrollments: Dict[str, List[Dict]]
         A Dict of mappings from Schoology section id to a list of JSON-like
         enrollment objects

     Returns
     -------
    Dict[str, List[Dict]]
         A Dict of mappings from Schoology section id to a list of JSON-like assignment
         objects incorporating the response values from the Schoology API,
         e.g. resource ids and status from individual POSTing
    """
    assert (
        assignment_per_section_count > 0
    ), "Number of assignments per section to generate must be greater than zero"

    assignment_per_section: Dict[str, List[Dict]] = generate_assignments(
        assignment_per_section_count, enrollments
    )

    result: Dict[str, List[Dict]] = {}
    for section_id, total_assignments_per_section in assignment_per_section.items():
        MAX_CHUNK_SIZE = 50
        chunked_assignments: List[List[Dict]] = [
            total_assignments_per_section[x : x + MAX_CHUNK_SIZE]
            for x in range(0, len(total_assignments_per_section), MAX_CHUNK_SIZE)
        ]

        result[section_id] = []
        for assignment_chunk in chunked_assignments:
            try:
                chunked_result = load_assignments(
                    request_client, section_id, assignment_chunk
                )
                result[section_id].extend(chunked_result)
            except Exception as ex:
                logger.exception(ex)

    return result
