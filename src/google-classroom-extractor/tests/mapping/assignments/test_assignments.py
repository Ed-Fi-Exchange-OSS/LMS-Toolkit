# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict
from datetime import datetime
import pandas as pd
from google_classroom_extractor.mapping.assignments import coursework_to_assignments_dfs
from google_classroom_extractor.mapping.constants import (
    SOURCE_SYSTEM,
    ENTITY_STATUS_ACTIVE,
)

# unique value for each column in fixture
COURSE_ID = "1"
ID = "2"
TITLE = "3"
DESCRIPTION = "4"
STATE = "5"
ALTERNATE_LINK = "6"
CREATION_TIME = "7"
UPDATE_TIME = "8"
MAX_POINTS = "9"
DUEDATE_YEAR = 2000
DUEDATE_MONTH = 10
DUEDATE_DAY = 11
DUETIME_HOURS = 12
DUETIME_MINUTES = 13
WORK_TYPE = "14"
SUBMISSION_MODIFICATION_MODE = "15"
ASSIGNEE_MODE = "16"
CREATOR_USER_ID = "17"
SCHEDULED_TIME = "18"
TOPIC_ID = "19"

# mutates first dict
def merged_dict(dict1: Dict, dict2: Dict) -> Dict:
    dict1.update(dict2)
    return dict1


def test_mappings():
    # arrange
    coursework_df = pd.DataFrame(
        {
            "courseId": [COURSE_ID],
            "id": [ID],
            "title": [TITLE],
            "description": [DESCRIPTION],
            "state": [STATE],
            "alternateLink": [ALTERNATE_LINK],
            "creationTime": [CREATION_TIME],
            "updateTime": [UPDATE_TIME],
            "maxPoints": [MAX_POINTS],
            "workType": [WORK_TYPE],
            "submissionModificationMode": [SUBMISSION_MODIFICATION_MODE],
            "assigneeMode": [ASSIGNEE_MODE],
            "creatorUserId": [CREATOR_USER_ID],
            "dueDate.year": [DUEDATE_YEAR],
            "dueDate.month": [DUEDATE_MONTH],
            "dueDate.day": [DUEDATE_DAY],
            "dueTime.hours": [DUETIME_HOURS],
            "dueTime.minutes": [DUETIME_MINUTES],
            "scheduledTime": [SCHEDULED_TIME],
            "topicId": [TOPIC_ID],
        }
    )

    # act
    assignments_dfs: Dict[str, pd.DataFrame] = coursework_to_assignments_dfs(
        coursework_df
    )

    # assert
    assert len(assignments_dfs) == 1
    assignments_df: pd.DataFrame = assignments_dfs[COURSE_ID]
    row_count, column_count = assignments_df.shape
    assert row_count == 1
    assert column_count == 12

    row_dict = assignments_df.to_dict(orient="records")[0]
    assert row_dict["AssignmentCategory"] == WORK_TYPE
    assert row_dict["AssignmentDescription"] == DESCRIPTION
    assert row_dict["DueDateTime"] == datetime(
        DUEDATE_YEAR, DUEDATE_MONTH, DUEDATE_DAY, DUETIME_HOURS, DUETIME_MINUTES
    )
    assert row_dict["EndDateTime"] == ""
    assert row_dict["EntityStatus"] == ENTITY_STATUS_ACTIVE
    assert row_dict["MaxPoints"] == MAX_POINTS
    assert row_dict["SourceSystem"] == SOURCE_SYSTEM
    assert row_dict["SourceSystemIdentifier"] == f"{COURSE_ID}:{ID}"
    assert row_dict["StartDateTime"] == SCHEDULED_TIME
    assert row_dict["Title"] == TITLE
    assert row_dict["CreateDate"] == CREATION_TIME
    assert row_dict["LastModifiedDate"] == UPDATE_TIME

BOILERPLATE: Dict[str, str] = {
    "description": DESCRIPTION,
    "state": STATE,
    "alternateLink": ALTERNATE_LINK,
    "creationTime": CREATION_TIME,
    "updateTime": UPDATE_TIME,
    "maxPoints": MAX_POINTS,
    "workType": WORK_TYPE,
    "submissionModificationMode": SUBMISSION_MODIFICATION_MODE,
    "assigneeMode": ASSIGNEE_MODE,
    "creatorUserId": CREATOR_USER_ID,
    "dueDate.year": DUEDATE_YEAR,
    "dueDate.month": DUEDATE_MONTH,
    "dueDate.day": DUEDATE_DAY,
    "dueTime.hours": DUETIME_HOURS,
    "dueTime.minutes": DUETIME_MINUTES,
    "scheduledTime": SCHEDULED_TIME,
    "topicId": TOPIC_ID,
}

def test_multiple_in_same_section():
    # arrange
    coursework1: Dict[str, str] = {
        "courseId": COURSE_ID,
        "id": ID,
        "title": TITLE,
    }

    coursework2_id = "coursework2_id"
    coursework2_title = "coursework2_title"

    coursework2: Dict[str, str] = {
        "courseId": COURSE_ID,
        "id": coursework2_id,
        "title": coursework2_title,
    }

    coursework_df = pd.DataFrame.from_dict(
        [
            merged_dict(coursework1, BOILERPLATE),
            merged_dict(coursework2, BOILERPLATE),
        ]
    )

    # act
    assignments_dfs: Dict[str, pd.DataFrame] = coursework_to_assignments_dfs(
        coursework_df
    )

    # assert
    assert len(assignments_dfs) == 1
    assignments_df: pd.DataFrame = assignments_dfs[COURSE_ID]
    row_count, _ = assignments_df.shape
    assert row_count == 2

    coursework1_dict = assignments_df.to_dict(orient="records")[0]
    assert coursework1_dict["SourceSystemIdentifier"] == f"{COURSE_ID}:{ID}"
    assert coursework1_dict["Title"] == TITLE

    coursework2_dict = assignments_df.to_dict(orient="records")[1]
    assert coursework2_dict["SourceSystemIdentifier"] == f"{COURSE_ID}:{coursework2_id}"
    assert coursework2_dict["Title"] == coursework2_title

def test_in_different_sections():
    # arrange
    coursework1: Dict[str, str] = {
        "courseId": COURSE_ID,
        "id": ID,
        "title": TITLE,
    }

    coursework2_course_id = "coursework2_course_id"
    coursework2_title = "coursework2_title"

    coursework2: Dict[str, str] = {
        "courseId": coursework2_course_id,
        "id": ID,
        "title": coursework2_title,
    }

    coursework_df = pd.DataFrame.from_dict(
        [
            merged_dict(coursework1, BOILERPLATE),
            merged_dict(coursework2, BOILERPLATE),
        ]
    )

    # act
    assignments_dfs: Dict[str, pd.DataFrame] = coursework_to_assignments_dfs(
        coursework_df
    )

    # assert
    assert len(assignments_dfs) == 2
    assignments_df1: pd.DataFrame = assignments_dfs[COURSE_ID]
    row_count, _ = assignments_df1.shape
    assert row_count == 1

    coursework1_dict = assignments_df1.to_dict(orient="records")[0]
    assert coursework1_dict["SourceSystemIdentifier"] == f"{COURSE_ID}:{ID}"
    assert coursework1_dict["Title"] == TITLE


    assignments_df2: pd.DataFrame = assignments_dfs[coursework2_course_id]
    row_count, _ = assignments_df2.shape
    assert row_count == 1

    coursework2_dict = assignments_df2.to_dict(orient="records")[0]
    assert coursework2_dict["SourceSystemIdentifier"] == f"{coursework2_course_id}:{ID}"
    assert coursework2_dict["Title"] == coursework2_title
