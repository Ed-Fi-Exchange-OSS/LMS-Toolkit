# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass
import logging
from typing import Union

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
from .mapping import submissions as submissionsMap


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
        users_list = self._client.get_users(self._page_size).get_all_pages()

        logger.debug("Exporting users: get roles")
        roles_list = self._client.get_roles(self._page_size).get_all_pages()

        users_df = sync.sync_resource(RESOURCE_NAMES.USER, self._db_engine, users_list)
        roles_df = sync.sync_resource(RESOURCE_NAMES.ROLE, self._db_engine, roles_list)

        return (
            usersMap.map_to_udm(users_df, roles_df)
            if not users_df.empty
            else pd.DataFrame()
        )

    def get_sections(self) -> pd.DataFrame:
        """
        Gets all Schoology sections.

        Returns
        -------
        list
        """

        logger.debug("Exporting sections: get active courses")
        courses_list = self._client.get_courses(self._page_size).get_all_pages()

        def _get_section_for_course(section_id: Union[int, str]):
            return self._client.get_section_by_course_id(section_id).get_all_pages()

        logger.debug("Exporting sections: get sections for active courses")
        all_sections: list = []
        for course in courses_list:
            all_sections = all_sections + _get_section_for_course(course["id"])

        sections = sync.sync_resource(
            RESOURCE_NAMES.SECTION,
            self._db_engine,
            all_sections
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
            self._client.get_assignments(section_id, self._page_size).get_all_pages()
            )

        return assignmentsMap.map_to_udm(assignments, section_id)

    def get_submissions(self, assignment_id: int, section_id: int) -> pd.DataFrame:
        """
        Gets all Schoology submissions for the given assignments.

        Parameters
        ----------
        assignment_id:
            The id of the assignment
        section_id:
            The id of the section
        Returns
        -------
        pd.DataFrame
            List of submissions
        """

        all_submissions = self._client.get_submissions_by_section_id_and_grade_item_id(
                section_id,
                assignment_id,
                self._page_size,
                ).get_all_pages()

        all_submissions = [
            {
                **row,
                'id': f'{section_id}#{assignment_id}#{row["uid"]}'
            }
            for row in all_submissions
        ]

        data = sync.sync_resource(
            RESOURCE_NAMES.SUBMISSION,
            self._db_engine,
            all_submissions
        )
        return submissionsMap.map_to_udm(data)

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

        enrollments = sync.sync_resource(
            RESOURCE_NAMES.ENROLLMENT,
            self._db_engine,
            self._client.get_enrollments(section_id).get_all_pages()
            )

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

        def _sync_wrapper(data: pd.DataFrame):
            """ Attendance_events entity has a more complex mapping. For most
            entities, sync process running before mapping is fine, but considering
            the process involved for this entity, the mapper for attendance events
            will accept an additional callable for sync process that will run when
            the mapping process is ready
            """
            return sync.sync_resource(
                RESOURCE_NAMES.ATTENDANCE_EVENTS,
                self._db_engine,
                data.to_dict('records'),
                "SourceSystemIdentifier"
                )

        events_df = attendanceMap.map_to_udm(
            events,
            section_associations,
            sync_callback=_sync_wrapper)

        return events_df

    def get_section_activities(self, section_id: int) -> pd.DataFrame:
        """
        Gets all Schoology section-activities for a section, in the Ed-Fi UDM format.

        Parameters
        ----------
        section_id: int
            Schoology section identifiers

        Returns
        -------
        DataFrame containing the section activities
        """

        discussions = self._client.get_discussions(section_id)
        replies: list = []
        for discussion in discussions:
            discussion_id = discussion["id"]
            replies = replies + self._client.get_discussion_replies(section_id, discussion_id)

        if len(replies) == 0:
            return pd.DataFrame()

        sync_replies = sync.sync_resource(
            RESOURCE_NAMES.USER_ACTIVITIES,
            self._db_engine,
            replies
            )

        return discussionRepliesMap.map_to_udm(pd.DataFrame(sync_replies), section_id)
