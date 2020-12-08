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

IS_STUDENT = "0"
IS_ACTIVE = "1"


def rollback_loaded_enrollments(
    request_client: RequestClient, response_dict: Dict[str, List[Dict]]
):
    """
    Delete already loaded enrollments via the Schoology API.
    **** Used during testing of the load functionality ****

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    response_dict: Dict[str, List[Dict]]
        A Dict of mappings from Schoology section id to a list of JSON-like response objects
        from a successful enrollment load operation
    """
    logger.info("**** Rolling back enrollments via Schoology API - for testing purposes")
    for section_id, creation_response in response_dict.items():
        logger.info("**** Deleting %s enrollments for section %s", len(creation_response), section_id)
        ids: str = ",".join(
            map(lambda enrollment: str(enrollment["id"]), creation_response)
        )

        delete_response = request_client.bulk_delete(
            "enrollments", f"enrollment_ids={ids}"
        )["enrollments"]["enrollment"]

        validate_multi_status(delete_response)
        logger.info("**** Successfully deleted %s enrollments", len(delete_response))


def load_enrollments(
    request_client: RequestClient, section_id: str, enrollments: List[Dict]
) -> List[Dict]:
    """
    Load a list of enrollments for a course via the Schoology API.

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    section_id : str
        The Schoolgy internal section id the enrollments are to be associated with
    enrollments: List[Dict]
        A list of JSON-like enrollment objects in a form suitable for submission to the
        Schoology enrollment creation endpoint.

    Returns
    -------
    List[Dict]
        A list of JSON-like enrollment objects incorporating the response values from the
        Schoology API, e.g. resource ids and status from individual POSTing
    """
    assert (
        len(enrollments) > 0 and len(enrollments) < 51
    ), "Number of enrollments must be between 1 and 50"

    logger.info("Creating %s enrollments via Schoology API", len(enrollments))

    enrollments_json = {"enrollments": {"enrollment": enrollments}}
    post_response: List[Dict] = request_client.bulk_post(
        f"sections/{section_id}/enrollments", enrollments_json
    )["enrollments"]["enrollment"]
    validate_multi_status(post_response)
    logger.info("Successfully created %s enrollments", len(post_response))

    with_schoology_response_df: DataFrame = merge(
        json_normalize(enrollments),
        json_normalize(post_response).drop(["uid"], axis=1),
        left_index=True,
        right_index=True,
    )

    return with_schoology_response_df.to_dict("records")


def generate_and_load_enrollments(
    request_client: RequestClient,
    users_per_section_count: int,
    sections: List[Dict],
    users: List[Dict],
) -> Dict[str, List[Dict]]:
    """
    Generate and load a number of enrollments into the Schoology API.

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    users_per_section_count : int
        The number of users to be in each section
    sections: List[Dict]
        A list of JSON-like section objects from a bulk create response
    users: List[Dict]
        A list of JSON-like user objects from a bulk create response

    Returns
    -------
    Dict[str, List[Dict]]
        A Dict of mappings from Schoology section id to a list of JSON-like enrollment
        objects incorporating the response values from the Schoology API,
        e.g. resource ids and status from individual POSTing
    """
    result: Dict[str, List[Dict]] = {}

    for section in sections:
        users_in_section = fake.random_sample(
            elements=users, length=users_per_section_count
        )
        enrollments = list(
            map(
                lambda user: {
                    "uid": user["id"],
                    "admin": IS_STUDENT,
                    "status": IS_ACTIVE,
                },
                users_in_section,
            )
        )

        enrollment_result = load_enrollments(request_client, section["id"], enrollments)
        result[section["id"]] = enrollment_result

    return result
