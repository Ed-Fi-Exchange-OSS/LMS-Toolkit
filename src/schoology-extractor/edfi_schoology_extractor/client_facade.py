# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass
import logging
from typing import Any, Dict, List, Union

from pandas import DataFrame, concat
import sqlalchemy

from edfi_schoology_extractor.helpers import sync
from edfi_schoology_extractor.helpers.constants import RESOURCE_NAMES
from edfi_schoology_extractor.api.request_client import RequestClient
from edfi_schoology_extractor.mapping import users as usersMap
from edfi_schoology_extractor.mapping import assignments as assignmentsMap
from edfi_schoology_extractor.mapping import sections as sectionsMap
from edfi_schoology_extractor.mapping import section_associations as sectionAssocMap
from edfi_schoology_extractor.mapping import attendance as attendanceMap
from edfi_schoology_extractor.mapping import discussion_replies as discussionRepliesMap
from edfi_schoology_extractor.mapping import discussions as discussionsMap
from edfi_schoology_extractor.mapping import submissions as submissionsMap
from edfi_schoology_extractor.mapping import section_updates as sectionUpdatesMap

logger = logging.getLogger(__name__)


@dataclass
class ClientFacade:
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
    def _client(self) -> RequestClient:
        assert isinstance(self.request_client, RequestClient)
        return self.request_client

    @property
    def _page_size(self) -> int:
        assert isinstance(self.page_size, int)
        return self.page_size

    @property
    def _db_engine(self) -> sqlalchemy.engine.base.Engine:
        assert isinstance(self.db_engine, sqlalchemy.engine.base.Engine)
        return self.db_engine

    def get_users(self) -> DataFrame:
        """
        Gets all Schoology users.

        Returns
        -------
        DataFrame
            DataFrame with all user data, in the unified data model format.
        """

        logger.debug("Exporting users: get users")
        users_list = self._client.get_users(self._page_size).get_all_pages()

        logger.debug("Exporting users: get roles")
        roles_list = self._client.get_roles(self._page_size).get_all_pages()

        users_df: DataFrame = sync.sync_resource(
            RESOURCE_NAMES.USER, self._db_engine, users_list
        )
        roles_df: DataFrame = sync.sync_resource(
            RESOURCE_NAMES.ROLE, self._db_engine, roles_list
        )

        return (
            usersMap.map_to_udm(users_df, roles_df)
            if not users_df.empty
            else DataFrame()
        )

    def get_sections(self) -> DataFrame:
        """
        Gets all Schoology sections.

        Returns
        -------
        DataFrame
            DataFrame with all section data, in the unified data model format.
        """

        logger.debug("Exporting sections: get active courses")
        courses_list = self._client.get_courses(self._page_size).get_all_pages()

        def _get_section_for_course(section_id: Union[int, str]) -> List[Dict[str, Any]]:
            return self._client.get_section_by_course_id(section_id).get_all_pages()

        logger.debug("Exporting sections: get sections for active courses")
        all_sections: List[Dict[str, Any]] = []
        for course in courses_list:
            all_sections = all_sections + _get_section_for_course(course["id"])

        sections_df: DataFrame = sync.sync_resource(
            RESOURCE_NAMES.SECTION, self._db_engine, all_sections
        )

        return sectionsMap.map_to_udm(sections_df)

    def get_assignments(self, section_id: int) -> DataFrame:
        """
        Gets all Schoology assignments for the given sections, with separate
        DataFrame output for each section.

        Parameters
        ----------
        section_id : int
            A Section Id

        Returns
        -------
        DataFrame
            DataFrame with all assignment data, in the unified data model format.
        """

        assignments_df: DataFrame = sync.sync_resource(
            RESOURCE_NAMES.ASSIGNMENT,
            self._db_engine,
            self._client.get_assignments(section_id, self._page_size).get_all_pages(),
        )

        return assignmentsMap.map_to_udm(assignments_df, section_id)

    def get_submissions(self, assignment_id: int, section_id: int) -> DataFrame:
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
        DataFrame
            DataFrame with all submission data, in the unified data model format.
        """

        all_submissions = self._client.get_submissions_by_section_id_and_grade_item_id(
            section_id,
            assignment_id,
            self._page_size,
        ).get_all_pages()

        all_submissions = [
            {**row, "id": f'{section_id}#{assignment_id}#{row["uid"]}'}
            for row in all_submissions
        ]

        submissions_df: DataFrame = sync.sync_resource(
            RESOURCE_NAMES.SUBMISSION, self._db_engine, all_submissions
        )
        return submissionsMap.map_to_udm(submissions_df)

    def get_section_associations(self, section_id: int) -> DataFrame:
        """
        Gets all Schoology enrollments (section associations) for the given section.

        Parameters
        ----------
        section_id : int
            A Section Id

        Returns
        -------
        DataFrame
            DataFrame with all section association data, in the unified data model format.
        """

        enrollments_df: DataFrame = sync.sync_resource(
            RESOURCE_NAMES.ENROLLMENT,
            self._db_engine,
            self._client.get_enrollments(section_id).get_all_pages(),
        )

        return sectionAssocMap.map_to_udm(enrollments_df, section_id)

    def get_attendance_events(
        self, section_id: int, section_associations: DataFrame
    ) -> DataFrame:
        """
        Gets all Schoology attendance events for a section, in the Ed-Fi UDM format.

        Parameters
        ----------
        section_id: int
            Schoology section identifiers
        section_associations: DataFrame
            DataFrame containing Section Associations in the UDM format, used to
            traverse enrollment information to find the correct User and Section
            identifiers

        Returns
        -------
        DataFrame
            DataFrame with all attendance event data, in the unified data model format.
        """

        events = self._client.get_attendance(section_id)

        def _sync_wrapper(data: DataFrame) -> DataFrame:
            """Attendance_events entity has a more complex mapping. For most
            entities, sync process running before mapping is fine, but considering
            the process involved for this entity, the mapper for attendance events
            will accept an additional callable for sync process that will run when
            the mapping process is ready
            """
            return sync.sync_resource(
                RESOURCE_NAMES.ATTENDANCE_EVENTS,
                self._db_engine,
                data.to_dict("records"),
                "SourceSystemIdentifier",
            )

        events_df: DataFrame = attendanceMap.map_to_udm(
            events, section_associations, sync_callback=_sync_wrapper
        )

        return events_df

    def get_section_activities(self, section_id: int) -> DataFrame:
        """
        Gets all Schoology section-activities for a section, in the Ed-Fi UDM format.

        Parameters
        ----------
        section_id: int
            Schoology section identifiers

        Returns
        -------
        DataFrame
            DataFrame with all section activity data, in the unified data model format.
        """

        def _get_discussions_and_discussion_replies() -> DataFrame:
            discussions = self._client.get_discussions(section_id)
            sync_discussions: DataFrame = sync.sync_resource(
                RESOURCE_NAMES.DISCUSSIONS, self._db_engine, discussions
            )
            mapped_discussions: DataFrame = discussionsMap.map_to_udm(
                sync_discussions, section_id
            )

            all_mapped_replies: DataFrame = DataFrame()
            for discussion in discussions:
                discussion_id = discussion["id"]
                replies: List[Dict[str, Any]] = self._client.get_discussion_replies(
                    section_id, discussion_id
                )
                sync_replies: DataFrame = sync.sync_resource(
                    RESOURCE_NAMES.DISCUSSION_REPLIES, self._db_engine, replies
                )
                mapped_replies: DataFrame = discussionRepliesMap.map_to_udm(
                    sync_replies, section_id, discussion_id
                )
                all_mapped_replies = concat([all_mapped_replies, mapped_replies])

            return concat([mapped_discussions, all_mapped_replies])

        def _get_section_updates() -> DataFrame:
            section_updates = self.request_client.get_section_updates(
                section_id
            ).get_all_pages()

            section_updates_df: DataFrame = sync.sync_resource(
                RESOURCE_NAMES.SECTION_UPDATE_TABLE, self._db_engine, section_updates
            )

            return sectionUpdatesMap.map_to_udm(section_updates_df, section_id)

        return concat(
            [
                _get_discussions_and_discussion_replies(),
                _get_section_updates(),
            ]
        )
