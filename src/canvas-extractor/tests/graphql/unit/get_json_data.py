# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import json
import logging

from os.path import exists
from dotenv import dotenv_values

from edfi_canvas_extractor.graphql.extractor import GraphQLExtractor
from edfi_canvas_extractor.graphql.schema import query_builder


def get_json_data():
    config = dotenv_values()

    CANVAS_BASE_URL = str(config['CANVAS_BASE_URL'])
    CANVAS_ACCESS_TOKEN = str(config['CANVAS_ACCESS_TOKEN'])
    START_DATE = config['START_DATE']
    END_DATE = config['END_DATE']

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
    PATH = "sample-data.json"

    if exists(PATH):
        logging.info("File exists!")
        with open(PATH, 'w') as f:
            f.write(json.dumps(body, indent=2))


def main():
    data = get_json_data()
    write_json_file(data)


if __name__ == '__main__':
    main()
