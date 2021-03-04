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


def generate_discussion_comments(
    discussion_comments_per_discussion_count: int,
    discussions: Dict[str, List[Dict]],
    enrollments: Dict[str, List[Dict]],
) -> Dict[str, Dict[str, List[Dict]]]:
    """
    Generate a list of graded Schoology discussion comments for discussions.

    Parameters
    ----------
    discussion_comments_per_discussion_count : int
         The number of discussion comments per discussion to generate
    discussions: Dict[str, List[Dict]]
        A Dict of mappings from Schoology section id to a list of JSON-like
        discussion objects from a bulk create response
    enrollments: Dict[str, List[Dict]]
        A Dict of mappings from Schoology section id to a list of JSON-like
        enrollment objects from a bulk create response

    Returns
    -------
    Dict[str, Dict[str, List[Dict]]]
        A Dict of mappings from Schoology section id to a dict of mappings
        of discussion ids to a list of JSON-like discussion comment objects
        in a form suitable for submission to the Schoology discussion comment
        create endpoint.
    """
    assert (
        discussion_comments_per_discussion_count > 0
    ), "Number of discussion comments per section to generate must be greater than zero"

    logging.info(
        f"Generating {discussion_comments_per_discussion_count} comments per discussion"
    )

    discussion_comments: Dict[str, Dict[str, List[Dict]]] = {}
    for section_id, discussions_for_section in discussions.items():
        discussion_comments[section_id] = {}
        enrollment_user_ids_for_section: List[str] = list(
            map(
                lambda enrollment: enrollment["uid"],
                enrollments[section_id],
            )
        )

        for discussion in discussions_for_section:
            user_ids_for_each_comment: List[str] = fake.random_choices(
                enrollment_user_ids_for_section,
                length=discussion_comments_per_discussion_count,
            )

            comments: List[Dict] = list(
                map(
                    lambda uid: {
                        "uid": uid,
                        "comment": fake.sentence(),
                    },
                    user_ids_for_each_comment,
                )
            )
            discussion_comments[section_id][discussion["id"]] = comments
    return discussion_comments


def rollback_loaded_discussion_comments(
    request_client: RequestClient, response_dict: Dict[str, Dict[str, List[Dict]]]
):
    """
    Delete already loaded discussion comments via the Schoology API.
    **** Used during testing of the load functionality ****

    Parameters
    ----------
    request_client: RequestClient
        A RequestClient initialized for access to the Schoology API
    response_dict: Dict[str, Dict[str, List[Dict]]]
        A Dict of mappings from Schoology section id to a dict of mappings
        of discussion ids to a list of JSON-like response objects
        from a successful discussion comment load operation
    """
    logger.info(
        "**** Rolling back discussion_comments via Schoology API - for testing purposes"
    )
    for section_id, discussions in response_dict.items():
        logger.info(
            "**** Deleting discussion comments for section %s",
            section_id,
        )
        for discussion_id, discussion_comments in discussions.items():
            logger.info(
                "****** Deleting discussion comments for discussion %s",
                discussion_id,
            )
            ids: List[str] = list(
                map(
                    lambda discussion_comment: str(discussion_comment["id"]),
                    discussion_comments,
                )
            )

            for id in ids:
                request_client.delete(
                    f"sections/{section_id}/discussions/{discussion_id}/comments", id
                )
                logger.info("******** Deleted discussion_comment with id %s", id)


def load_discussion_comments(
    request_client: RequestClient,
    section_id: str,
    discussion_id: str,
    discussion_comments: List[Dict],
) -> List[Dict]:
    """
    Load a list of discussion_comments via the Schoology API.

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    section_id: str
        The Schoology id of the section that the discussion_comments are associated with
    discussion_id: str
        The Schoology id of the discussion that the discussion_comments are associated with
    discussion_comments: List[Dict]
        A list of JSON-like discussion comment objects in a form suitable for submission
        to the Schoology discussion comment create endpoint.
    Returns
    -------
    List[Dict]
        A list of JSON-like discussion comment objects incorporating the response values from the
        Schoology API, e.g. resource ids and status from individual POSTing
    """
    logger.info(
        "Creating %s discussion_comments via Schoology API", len(discussion_comments)
    )

    post_responses: List[Dict] = []
    for discussion_comment in discussion_comments:
        response: Dict = request_client.post(
            f"sections/{section_id}/discussions/{discussion_id}/comments",
            discussion_comment,
        )
        post_responses.append(response)

    logger.info("Successfully created %s discussion_comments", len(post_responses))
    return post_responses


def generate_and_load_discussion_comments(
    request_client: RequestClient,
    discussion_comments_per_discussion_count: int,
    discussions: Dict[str, List[Dict]],
    enrollments: Dict[str, List[Dict]],
) -> Dict[str, Dict[str, List[Dict]]]:
    """
    Generate and load a number of discussion_comments into the Schoology API.

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API
    discussion_comments_per_discussion_count : int
         The number of discussion comments per discussion to generate
    discussions: Dict[str, List[Dict]]
        A Dict of mappings from Schoology section id to a list of JSON-like
        discussion objects from a bulk create response
    enrollments: Dict[str, List[Dict]]
        A Dict of mappings from Schoology section id to a list of JSON-like
        enrollment objects from a bulk create response

    Returns
    -------
    Dict[str, Dict[str, List[Dict]]]
        A Dict of mappings from Schoology section id to a dict of mappings
        of discussion ids to a list of JSON-like discussion comment
        objects incorporating the response values from the Schoology API,
        e.g. resource ids and status from individual POSTing
    """
    assert (
        discussion_comments_per_discussion_count > 0
    ), "Number of discussion comments per discussion to generate must be greater than zero"

    discussion_comments_per_section_and_discussion: Dict[
        str, Dict[str, List[Dict]]
    ] = generate_discussion_comments(
        discussion_comments_per_discussion_count, discussions, enrollments
    )

    result: Dict[str, Dict[str, List[Dict]]] = {}
    for (
        section_id,
        discussions,
    ) in discussion_comments_per_section_and_discussion.items():
        result[section_id] = {}
        for (
            discussion_id,
            discussion_comments,
        ) in discussions.items():
            try:
                result[section_id][discussion_id] = load_discussion_comments(
                    request_client=request_client,
                    section_id=section_id,
                    discussion_id=discussion_id,
                    discussion_comments=discussion_comments,
                )
            except Exception as ex:
                logger.exception(ex)

    return result
