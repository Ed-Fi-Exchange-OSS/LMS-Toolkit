# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License,  Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
import pytest
import json

from edfi_canvas_extractor.mapping.submissions import map_to_udm_submissions

SECTION_ID = "1234567890"


def describe_when_mapping_empty_DataFrame():
    def it_should_return_empty_DataFrame():
        df = map_to_udm_submissions(pd.DataFrame(), SECTION_ID)
        assert (df == pd.DataFrame()).all().all()


def describe_when_mapping_Schoology_DataFrame_to_EdFi_DataFrame():
    @pytest.fixture
    def result() -> pd.DataFrame:

        submissions = """id,body,url,grade,score,submitted_at,submitted_at_date,assignment_id,user_id,submission_type,workflow_state,grade_matches_current_submission,graded_at,grader_id,attempt,cached_due_date,cached_due_date_date,excused,late_policy_status,points_deducted,grading_period_id,extra_attempts,posted_at,late,missing,seconds_late,entered_grade,entered_score,preview_url,anonymous_id,course_id,graded_at_date,posted_at_date,CreateDate,LastModifiedDate
130,"<p><span>Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum.</span></p>",,,,2020-09-14T17:23:46Z,2020-09-14 17:23:46+00:00,114,113,online_text_entry,submitted,True,,,1,2021-05-01T06:01:00Z,2021-05-01 06:01:00+00:00,,,,,,,False,False,0,,,https://edfialliance.instructure.com/courses/104/assignments/114/submissions/113?preview=1&version=1,Sg6Ki,104,,,2020-12-31 15:26:01.372034,2020-12-31 15:26:01.372034
129,"<p><span>Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum.</span></p>",,,,2020-09-14T17:26:42Z,2020-09-14 17:26:42+00:00,114,114,online_text_entry,submitted,True,,,1,2021-05-01T06:01:00Z,2021-05-01 06:01:00+00:00,,,,,,,False,False,0,,,https://edfialliance.instructure.com/courses/104/assignments/114/submissions/114?preview=1&version=1,6fcko,104,,,2020-12-31 15:26:01.372034,2020-12-31 15:26:01.372034"""

        lines = submissions.split("\n")
        section_associations = pd.DataFrame(
            [x.split(",") for x in lines[1:]], columns=lines[0].split(",")
        )

        # Arrange
        df = pd.DataFrame(section_associations)

        # Act
        return map_to_udm_submissions(df, SECTION_ID)

    def it_should_have_correct_number_of_columns(result):
        assert result.shape[1] == 12

    def it_should_have_schoology_as_SourceSystem(result):
        assert result["SourceSystem"].iloc[0] == "Canvas"

    def it_should_map_id_to_SourceSystemIdentifier(result):
        assert result["SourceSystemIdentifier"].iloc[0] == "130"

    def it_should_map_section_and_assignment_id_to_SourceSystemIdentifier(result):
        assert result["AssignmentSourceSystemIdentifier"].iloc[0] == f"{SECTION_ID}-114"

    def it_should_map_uid_to_LMSUserSourceSystemIdentifier(result):
        assert result["LMSUserSourceSystemIdentifier"].iloc[0] == "113"

    def it_should_map_created_to_SubmissionDateTime(result):
        assert result["SubmissionDateTime"].iloc[0] == "2020-09-14 17:23:46"

    def it_should_have_empty_SourceCreateDate(result):
        assert result["SourceCreateDate"].iloc[0] is None

    def it_should_have_empty_SourceLastModifiedDate(result):
        assert result["SourceLastModifiedDate"].iloc[0] is None


def describe_when_mapping_submission_using_read_data_example():
    @pytest.fixture
    def result() -> pd.DataFrame:
        # Arrange
        submission = json.loads("""
{
    "id": 7898567,
    "body": null,
    "url": "<redacted>",
    "grade": "20",
    "score": 20.0,
    "submitted_at": "2021-03-16T16:20:10Z",
    "assignment_id": 356597,
    "user_id": 1163,
    "submission_type": "online_url",
    "workflow_state": "graded",
    "grade_matches_current_submission": true,
    "graded_at": "2021-03-30T16:11:38Z",
    "grader_id": 7870,
    "attempt": 1,
    "cached_due_date": "2021-03-23T03:59:59Z",
    "excused": false,
    "late_policy_status": null,
    "points_deducted": null,
    "grading_period_id": 219,
    "extra_attempts": null,
    "posted_at": "2021-03-30T16:11:38Z",
    "late": false,
    "missing": false,
    "seconds_late": 0,
    "entered_grade": "20",
    "entered_score": 20.0,
    "preview_url": "<redacted>",
    "attachments": [
        {
            "id": 1391841,
            "uuid": "S4ULVActQGOL3LZGABUpgzgyhUYYRMB4zCbmETrw",
            "folder_id": null,
            "display_name": "websnappr20210316-5557-1ilhto4.png",
            "filename": "websnappr20210108-20780-7nj0ua.png",
            "upload_status": "success",
            "content-type": "image/png",
            "url": "<redacted>",
            "size": 26447,
            "created_at": "2021-03-16T16:20:16Z",
            "updated_at": "2021-03-16T16:20:16Z",
            "unlock_at": null,
            "locked": false,
            "hidden": false,
            "lock_at": null,
            "hidden_for_user": false,
            "thumbnail_url": "<redacted>",
            "modified_at": "2021-03-16T16:20:16Z",
            "mime_class": "image",
            "media_entry_id": null,
            "locked_for_user": false,
            "preview_url": null
        }
    ],
    "anonymous_id": "uhwKy",
    "CreateDate": "2021-03-20 16:20:16",
    "LastModifiedDate": "2021-03-20 16:20:16"
}""")
        submissions_df = pd.DataFrame.from_dict(submission)

        # Act
        return map_to_udm_submissions(submissions_df, SECTION_ID)

    def it_should_have_correct_number_of_columns(result):
        assert result.shape[1] == 12

    def it_should_have_schoology_as_SourceSystem(result):
        assert result["SourceSystem"].iloc[0] == "Canvas"

    def it_should_map_id_to_SourceSystemIdentifier(result):
        assert result["SourceSystemIdentifier"].iloc[0] == 7898567

    def it_should_map_section_and_assignment_id_to_SourceSystemIdentifier(result):
        assert result["AssignmentSourceSystemIdentifier"].iloc[0] == f"{SECTION_ID}-356597"

    def it_should_map_uid_to_LMSUserSourceSystemIdentifier(result):
        assert result["LMSUserSourceSystemIdentifier"].iloc[0] == 1163

    def it_should_map_created_to_SubmissionDateTime(result):
        assert result["SubmissionDateTime"].iloc[0] == "2021-03-16 16:20:10"

    def it_should_have_empty_SourceCreateDate(result):
        assert result["SourceCreateDate"].iloc[0] is None

    def it_should_have_empty_SourceLastModifiedDate(result):
        assert result["SourceLastModifiedDate"].iloc[0] is None
