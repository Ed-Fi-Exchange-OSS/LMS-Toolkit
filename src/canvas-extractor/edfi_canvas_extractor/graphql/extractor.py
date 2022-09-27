# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import json
import logging
import requests

from typing import List

from .schema import query_builder
from .utils import validate_date


class Singleton(object):
    _instance = None

    def __call__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__call__(class_, *args, **kwargs)
        return class_._instance


class Extract(Singleton):
    courses: List
    sections: List

    def __init__(self):
        self.data = None
        self.courses = list()
        self.sections = list()

    def get_from_canvas(self, query: str):
        """
        Get GraphQL Query from Canvas

        Parameters
        ----------
        query: str
            query string for GraphQL

        Returns
        -------
        Dict JSON Object
        """

        GRAPHQL_URL = f"{self.base_url}/api/graphql"
        GRAPHQL_AUTH = {'Authorization': f'Bearer {self.access_token}'}

        try:
            fetch = requests.post(
                GRAPHQL_URL,
                headers=GRAPHQL_AUTH,
                json={"query": query}
                )

            if fetch.status_code != 200:
                fetch.raise_for_status()

            body = json.loads(fetch.text)

            if "errors" in body:
                raise RuntimeError(str(body))

            return body

        except requests.exceptions.HTTPError as err:
            logging.error(err)


    def extract(self, body) -> None:
        """
        Extract data from GraphQL query in Canvas

        Parameters
        ----------
        body: Dict JSON Object
        """
        courses = body["data"]["account"]["coursesConnection"]["nodes"][0]

        for course in courses["term"]["coursesConnection"]["nodes"]:
            if course["state"] not in ["available", "completed"]:
                continue

            start_term = courses["term"]["startAt"]
            end_term = courses["term"]["endAt"]

            if start_term is not None and end_term is not None:
                if not validate_date(self.start, self.end, start_term, end_term):
                    continue

            self.courses.append({
                "id": course["_id"],
                "name": course["name"],
                "state": course["state"],
                })

            sections = course["sectionsConnection"]["nodes"]
            for section in sections:
                self.sections.append({
                    "id": section["_id"],
                    "name": section["name"],
                    "sis_section_id": section["sisId"],
                    "created_at": section["createdAt"],
                    "updated_at": section["updatedAt"],
                    })

        if courses.get("pageInfo"):
            courses_page = courses["pageInfo"]
            if courses_page["hasNextPage"]:
                after = courses_page["endCursor"]
                query = query_builder(self.account, after)
                self.get_from_canvas(query)

    def set_credentials(self, base_url, access_token) -> None:
        """
        Set credentials to get from GraphQL

        Parameters
        ----------
        args: MainArguments
        """
        self.base_url = base_url
        self.access_token = access_token

    def set_account(self, account) -> None:
        """
        Set account number to get from GraphQL

        Parameters
        ----------
        account: str 
            an account number
        """
        self.account = account

    def set_dates(self, start_date, end_date) -> None:
        """
        Set dates to filter courses fetched from
        GraphQL query in Canvas

        Parameters
        ----------
        start_date: str
            a string with start date
        end_date: str
            a string with end date
        """
        self.start = start_date
        self.end = end_date

    def run(self) -> None:
        if not self.data:
            query = query_builder(self.account)

            try:
                data = self.get_from_canvas(query)
                self.extract(data)
                self.data = True
            except Exception as e:
                logging.error(e)

    def get_courses(self) -> List:
        """
        Returns a List of Courses

        Returns
        -------
        List
            a List of Courses
        """
        return self.courses

    def get_sections(self) -> List:
        """
        Returns a sorted List of Sections

        Returns
        -------
        List
            a List of Sections
        """
        return sorted(self.sections, key=lambda x: x.id)
