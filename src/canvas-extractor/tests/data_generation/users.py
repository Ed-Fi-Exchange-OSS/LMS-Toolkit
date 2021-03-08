# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import time
from canvasapi.account import Account
from canvasapi.user import User
from typing import Dict, List
from faker import Faker

fake = Faker("en_US")
logger = logging.getLogger(__name__)


def generate_users(record_count: int) -> List[Dict]:
    """
    Generate a list of Canvas users.

    Parameters
    ----------
    record_count : int
        The number of users to generate.

    Returns
    -------
    List[Dict]
        A list of JSON-like user objects in a form suitable for submission to the
        Canvas user create endpoint.
    """
    assert record_count > 0, "Number of users to generate must be greater than zero"

    logging.info(f"Generating {record_count} users")
    users = []
    for i in range(1, record_count + 1):
        if i % 1000 == 0:
            logging.info(f"{i} users...")
        email = fake.email()
        users.append(
            {
                "unique_id": email,
                "sys_user_id": email,
            }
        )
    return users


def rollback_loaded_users(account: Account, users: List[User]):
    """
    Delete already loaded users via the Canvas API.
    **** Used during testing of the load functionality ****

    Parameters
    ----------
    account : Account
        An Account SDK object
    users: List[User]
        A list of User SDK objects from a successful user load operation
    """
    logger.info(
        "**** Rolling back %s users via Canvas API - for testing purposes",
        len(users),
    )

    for user in users:
        account.delete_user(user)

    logger.info("**** Successfully deleted %s users", len(users))


def load_users(account: Account, users: List[Dict]) -> List[User]:
    """
    Load a list of users via the Canvas API.

    Parameters
    ----------
    account : Account
        An Account SDK object
    users: List[Dict]
        A list of JSON-like user objects in a form suitable for submission to the
        Canvas user creation endpoint.

    Returns
    -------
    List[User]
        A list of Canvas SDK User objects representing the created users
    """
    logger.info("Creating %s users via Canvas API", len(users))

    result: List[User] = []
    for user in users:
        try:
            result.append(account.create_user(user))
        except Exception as ex:
            logger.exception(ex)
            time.sleep(10)

    logger.info("Successfully created %s users", len(result))

    return result


def generate_and_load_users(account: Account, record_count: int) -> List[User]:
    """
    Generate and load a number of users into the Canvas API.

    Parameters
    ----------
    canvas : Canvas
        A Canvas SDK object
    record_count : int
        The number of users to generate.

    Returns
    -------
    List[User]
        A list Canvas SDK User objects representing the created users
    """
    assert record_count > 0, "Number of users to generate must be greater than zero"

    users: List[Dict] = generate_users(record_count)

    result: List[User] = []
    try:
        result = load_users(account, users)
    except Exception as ex:
        logger.exception(ex)

    return result
