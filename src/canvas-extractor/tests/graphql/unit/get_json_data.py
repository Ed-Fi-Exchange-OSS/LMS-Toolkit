# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import json
import logging
import os

from os.path import exists
from dotenv import load_dotenv

from edfi_canvas_extractor.graphql.extractor import GraphQLExtractor
from edfi_canvas_extractor.graphql.schema import query_builder


load_dotenv()


def get_json_data():
    CANVAS_BASE_URL = os.environ['CANVAS_BASE_URL']
    CANVAS_ACCESS_TOKEN = os.environ['CANVAS_ACCESS_TOKEN']
    START_DATE = "2021-01-01"
    END_DATE = "2030-01-01"

    query = query_builder(1)

    gql = GraphQLExtractor(
        CANVAS_BASE_URL,
        CANVAS_ACCESS_TOKEN,
        "1",
        START_DATE,
        END_DATE,
        )

    body = gql.get_from_canvas(query)

    return body


def write_json_file(body: str) -> None:
    PATH = "tests/graphql/unit/sample-data.json"

    if exists(PATH):
        logging.info("File exists!")
        with open(PATH, 'w') as f:
            f.write(json.dumps(body, indent=2))


def main():
    data = get_json_data()
    write_json_file(data)


if __name__ == '__main__':
    main()
