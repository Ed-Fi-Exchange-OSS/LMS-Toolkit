# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass
from logging import Logger
from typing import Any, Dict, List

import pandas as pd

from api.request_client import RequestClient
from mapping import users as usersMap


@dataclass
class Facade:
    logger: Logger
    request_client: RequestClient
    page_size: int

    @property
    def _logger(self):
        assert isinstance(self.logger, Logger)
        return self.logger

    @property
    def _client(self):
        assert isinstance(self.request_client, RequestClient)
        return self.request_client

    @property
    def _page_size(self):
        assert isinstance(self.page_size, int)
        return self.page_size

    def get_users(self) -> pd.DataFrame:

        self._logger.debug("Exporting users: get users")
        users_response = self._client.get_users(self._page_size)
        users_list: List[Any] = []
        while True:
            users_list = users_list + users_response.current_page_items
            if users_response.get_next_page() is None:
                break

        self._logger.debug("Exporting users: get roles")
        roles_list: List[Any] = []
        roles_response = self._client.get_roles()
        while True:
            roles_list = roles_list + roles_response.current_page_items
            if roles_response.get_next_page() is None:
                break

        users_df = pd.DataFrame(users_list)
        roles_df = pd.DataFrame(roles_list)

        return usersMap.map_to_udm(users_df, roles_df)

    def get_sections(self) -> list:

        self._logger.debug("Exporting sections: get active courses")
        courses_response = self._client.get_courses(self._page_size)
        courses_list: List[Any] = []
        while True:
            courses_list = courses_list + courses_response.current_page_items
            if courses_response.get_next_page() is None:
                break

        course_ids = map(lambda x: x["id"], courses_list)
        self._logger.debug("Exporting sections: get sections for active courses")

        return self._client.get_section_by_course_ids(list(course_ids))

    def get_assignments(
        self, sections: List[Dict[str, Any]], grading_periods: List[str]
    ) -> list:
        assignments = self._client.get_assignments_by_section_ids(
            [s["id"] for s in sections]
        )

        return [
            assignment
            for assignment in assignments
            if assignment["grading_period"] in grading_periods
        ]

    def get_submissions(self, assignments) -> list:
        submissions: List[Dict[str, Any]] = []

        for assignment in assignments:
            submissions_response = (
                self._client.get_submissions_by_section_id_and_grade_item_id(
                    assignment["section_id"],
                    str(assignment["grade_item_id"]),
                    self._page_size,
                )
            )

            while True:
                submissions = submissions + submissions_response.current_page_items
                if submissions_response.get_next_page() is None:
                    break

        return submissions
