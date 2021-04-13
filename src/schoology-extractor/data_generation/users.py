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

VALID_SCHOOL_ID = "2908525646"
VALID_ROLE_ID = "796380"
VALID_EMAIL_DOMAIN = "studentgps.org"


def generate_users(record_count: int) -> List[Dict]:
    """
    Generate a list of Schoology users.

    Parameters
    ----------
    record_count : int
        The number of users to generate.

    Returns
    -------
    List[Dict]
        A list of JSON-like user objects in a form suitable for submission to the
        Schoology user create endpoint.
    """
    assert record_count > 0, "Number of users to generate must be greater than zero"

    logging.info(f"Generating {record_count} users")
    users = []
    for i in range(1, record_count + 1):
        if i % 1000 == 0:
            logging.info(f"{i} users...")
        first_name = fake.first_name()
        users.append(
            {
                "school_id": VALID_SCHOOL_ID,
                "school_uid": str(fake.random_number(digits=8)),
                "name_first": first_name,
                "name_last": fake.last_name(),
                "primary_email": f"{first_name}.{fake.random_number(digits=8)}@{VALID_EMAIL_DOMAIN}",
                "role_id": VALID_ROLE_ID,
            }
        )
    return users


def rollback_loaded_users(request_client: RequestClient, creation_response: List[Dict]):
    """
    Delete already loaded users via the Schoology API.
    **** Used during testing of the load functionality ****

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    creation_response: List[Dict]
        A list of JSON-like response objects from a successful user load operation
    """
    logger.info(
        "**** Rolling back %s users via Schoology API - for testing purposes",
        len(creation_response),
    )

    ids: str = ",".join(map(lambda user: str(user["id"]), creation_response))

    delete_response = request_client.bulk_delete(
        "users", f"uids={ids}&email_notification=0"
    )["user"]

    validate_multi_status(delete_response)
    logger.info("**** Successfully deleted %s users", len(delete_response))


def load_users(request_client: RequestClient, users: List[Dict]) -> List[Dict]:
    """
    Load a list of users via the Schoology API.

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    users: List[Dict]
        A list of JSON-like user objects in a form suitable for submission to the
        Schoology user creation endpoint.

    Returns
    -------
    List[Dict]
        A list of JSON-like user objects incorporating the response values from the
        Schoology API, e.g. resource ids and status from individual POSTing
    """
    assert (
        len(users) > 0 and len(users) < 51
    ), "Number of users must be between 1 and 50"

    logger.info("Creating %s users via Schoology API", len(users))

    users_json = {"users": {"user": users}}
    post_response: List[Dict] = request_client.bulk_post("users", users_json)["user"]
    validate_multi_status(post_response)
    logger.info("Successfully created %s users", len(post_response))

    with_schoology_response_df: DataFrame = merge(
        json_normalize(users),
        json_normalize(post_response).drop("school_uid", axis=1),
        left_index=True,
        right_index=True,
    )

    return with_schoology_response_df.to_dict("records")


def generate_and_load_users(
    request_client: RequestClient, record_count: int
) -> List[Dict]:
    """
    Generate and load a number of users into the Schoology API.

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    record_count : int
        The number of users to generate.

    Returns
    -------
    List[Dict]
        A list of JSON-like user objects incorporating the response values from the
        Schoology API, e.g. resource ids and status from individual POSTing
    """
    assert record_count > 0, "Number of users to generate must be greater than zero"

    total_users: List[Dict] = generate_users(record_count)

    MAX_CHUNK_SIZE = 50
    chunked_users: List[List[Dict]] = [
        total_users[x : x + MAX_CHUNK_SIZE]
        for x in range(0, len(total_users), MAX_CHUNK_SIZE)
    ]

    result: List[Dict] = []
    for user_chunk in chunked_users:
        try:
            chunked_result = load_users(request_client, user_chunk)
            result.extend(chunked_result)
        except Exception as ex:
            logger.exception(ex)

    return result
