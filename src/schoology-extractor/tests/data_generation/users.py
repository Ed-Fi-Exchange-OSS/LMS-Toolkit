# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import Dict, List
from http import HTTPStatus
from faker import Faker
from schoology_extractor.api.request_client import RequestClient

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
                "primary_email": f"{first_name}{fake.random_number(digits=3)}@{VALID_EMAIL_DOMAIN}",
                "role_id": VALID_ROLE_ID,
            }
        )
    return users


def _validate_multi_status(multi_response: List[Dict]):
    """
    Confirm response codes for all elements of a bulk response.

    Parameters
    ----------
    multi_response : List[Dict]
        A list of JSON-like responses to each individual request.

    Raises
    -------
    RuntimeError
        If any individual operation had a non-OK response code.
    """
    for response in multi_response:
        if response["response_code"] != HTTPStatus.OK:
            raise RuntimeError(str(multi_response))


def _rollback_loaded_users(request_client: RequestClient, creation_response: List[Dict]):
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
    logger.info("**** Rolling back %s users via Schoology API - for testing purposes", len(creation_response))

    ids: str = ",".join(map(lambda user: str(user["id"]), creation_response))

    delete_response = request_client.bulk_delete("users", ids)["user"]

    _validate_multi_status(delete_response)
    logger.info("**** Successfully deleted %s users", len(delete_response))


def load_users(request_client: RequestClient, users: List[Dict]):
    """
    Load a list of users via the Schoology API.

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    users: List[Dict]
        A list of JSON-like user objects in a form suitable for submission to the
        Schoology user creation endpoint.
    """
    assert len(users) > 0 and len(users) < 51, "Number of users must be between 1 and 50"

    logger.info("Creating %s users via Schoology API", len(users))

    users_json = {
        "users": {
            "user": users
        }
    }
    post_response: List[Dict] = request_client.bulk_post("users", users_json)["user"]
    _validate_multi_status(post_response)
    logger.info("Successfully created %s users", len(post_response))

    # **** Used during testing of the load functionality ****
    _rollback_loaded_users(request_client, post_response)


def generate_and_load_users(request_client: RequestClient, record_count: int):
    """
    Generate and load a number of users into the Schoology API.

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    record_count : int
        The number of users to generate.
    """
    assert record_count > 0, "Number of users to generate must be greater than zero"

    total_users: List[Dict] = generate_users(record_count)

    MAX_CHUNK_SIZE = 50
    chunked_users: List[List[Dict]] = [total_users[x:x+MAX_CHUNK_SIZE] for x in range(0, len(total_users), MAX_CHUNK_SIZE)]

    for user_chunk in chunked_users:
        load_users(request_client, user_chunk)
