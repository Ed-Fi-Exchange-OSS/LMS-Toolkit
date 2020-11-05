# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass
import logging
from typing import Any, Dict, List

import pandas as pd
import sqlalchemy

from .helpers import sync
from .helpers.constants import RESOURCE_NAMES
from .api.request_client import RequestClient
from .mapping import users as usersMap
from .mapping import assignments as assignmentsMap
from .mapping import sections as sectionsMap
from .mapping import section_associations as sectionAssocMap
from .mapping import attendance as attendanceMap
from .mapping import discussion_replies as discussionRepliesMap


logger = logging.getLogger(__name__)


@dataclass
class SchoologyExtractFacade:
    """
    Provides business logic to orchestrate retrieval of data from the LMS and
    reshape it into the Ed-Fi LMS Unified Data Model (UDM).

    Parameters
    ----------
    request_client : RequestClient
        Instance of a Schoology request client
    page_size : int
        Number of records to retrieve with each API call
    db_engine : sqlalchemy.engine.base.Engine
        Database connectivity for sync process
    """

    request_client: RequestClient
    page_size: int
    db_engine: sqlalchemy.engine.base.Engine


    @property
    def _client(self):
        assert isinstance(self.request_client, RequestClient)
        return self.request_client

    @property
    def _page_size(self):
        assert isinstance(self.page_size, int)
        return self.page_size

    @property
    def _db_engine(self):
        assert isinstance(self.db_engine, sqlalchemy.engine.base.Engine)
        return self.db_engine

    def get_users(self) -> pd.DataFrame:
        """
        Gets all Schoology users.

        Returns
        -------
        pd.DataFrame
        """

        logger.debug("Exporting users: get users")
        users_response = self._client.get_users(self._page_size)
        users_list: List[Any] = []
        while True:
            users_list = users_list + users_response.current_page_items
            if users_response.get_next_page() is None:
                break

        logger.debug("Exporting users: get roles")
        roles_list: List[Any] = []
        roles_response = self._client.get_roles(self._page_size)
        while True:
            roles_list = roles_list + roles_response.current_page_items
            if roles_response.get_next_page() is None:
                break

        users_df = sync.sync_resource(RESOURCE_NAMES.USER, self._db_engine, users_list)
        roles_df = sync.sync_resource(
            RESOURCE_NAMES.ROLE,
            self._db_engine,
            roles_list
        )

        return (
            usersMap.map_to_udm(users_df, roles_df)
            if not users_df.empty
            else pd.DataFrame()
        )

    def get_sections(self) -> pd.DataFrame:
        """
        Gets all Schoology users.

        Returns
        -------
        list
        """

        logger.debug("Exporting sections: get active courses")
        courses_response = self._client.get_courses(self._page_size)
        courses_list: List[Any] = []
        while True:
            courses_list = courses_list + courses_response.current_page_items
            if courses_response.get_next_page() is None:
                break

        logger.debug("Exporting sections: get sections for active courses")

        # TODO: inconsistency - in this case the pagination is handled inside of
        # the client, instead of being handled here. Arguably there should be
        # some other thing, neither this service nor the client, that handles
        # the paging. As BB said in a pr comment, perhaps it should be handled
        # in a decorator. This works but we should consider refactoring to a
        # cleaner approach.
        sections = sync.sync_resource(
            RESOURCE_NAMES.SECTION,
            self._db_engine,
            self._client.get_section_by_course_ids([c["id"] for c in courses_list])
            )

        return sectionsMap.map_to_udm(sections)

    def get_assignments(self, section_id: int) -> pd.DataFrame:
        """
        Gets all Schoology assignments for the given sections, with separate
        DataFrame output for each section.

        Parameters
        ----------
        section_id : int
            A Section Id

        Returns
        -------
        pd.DataFrame
            DataFrame with all assignment data, in the unified data model format.
        """

        assignments = sync.sync_resource(
            RESOURCE_NAMES.ASSIGNMENT,
            self._db_engine,
            self._client.get_assignments(section_id, self._page_size)
            )

        return assignmentsMap.map_to_udm(assignments, section_id)

    def get_submissions(self, assignments: pd.DataFrame) -> list:
        """
        Gets all Schoology submissions for the given assignments.

        Parameters
        ----------
        assignments: pd.DataFrame
            A DataFrame containing assignment data

        Returns
        -------
        list
            List of submission dictionaries
        """

        submissions: List[Dict[str, Any]] = []

        for _, assignment in assignments.iterrows():
            section_id = assignment["LMSSectionSourceSystemIdentifier"]
            grade_item_id = assignment["SourceSystemIdentifier"]

            submissions_response = (
                self._client.get_submissions_by_section_id_and_grade_item_id(
                    section_id,
                    grade_item_id,
                    self._page_size,
                )
            )

            while True:
                submissions = submissions + submissions_response.current_page_items
                if submissions_response.get_next_page() is None:
                    break

        return submissions

    def get_section_associations(self, section_id: int) -> pd.DataFrame:
        """
        Gets all Schoology enrollments (section associations) for the given section.

        Parameters
        ----------
        section_id : int
            A Section Id

        Returns
        -------
        pd.DataFrame
            DataFrame with all assignment data, in the unified data model format.
        """

        enrollments = self._client.get_enrollments(section_id)

        return sectionAssocMap.map_to_udm(pd.DataFrame(enrollments), section_id)

    def get_attendance_events(
        self, section_id: int, section_associations: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Gets all Schoology attendance events for a section, in the Ed-Fi UDM format.

        Parameters
        ----------
        section_id: int
            Schoology section identifiers
        section_associations: pd.DataFrame
            DataFrame containing Section Associations in the UDM format, used to
            traverse enrollment information to find the correct User and Section
            identifiers

        Returns
        -------
        DataFrame containing the attendance events
        """

        events = self._client.get_attendance(section_id)

        events_df = attendanceMap.map_to_udm(events, section_associations)

        return events_df

    def get_user_activities(self, section_id: int) -> pd.DataFrame:
        """
        Gets all Schoology user-activities for a section, in the Ed-Fi UDM format.

        Parameters
        ----------
        section_id: int
            Schoology section identifiers

        Returns
        -------
        DataFrame containing the user activities
        """

        discussions = self._client.get_discussions(section_id)
        replies: list = []
        for discussion in discussions:
            discussion_id = discussion["id"]
            replies = replies + self._client.get_discussion_replies(section_id, discussion_id)

        if len(replies) == 0:
            return pd.DataFrame()

        return discussionRepliesMap.map_to_udm(pd.DataFrame(replies), section_id)
