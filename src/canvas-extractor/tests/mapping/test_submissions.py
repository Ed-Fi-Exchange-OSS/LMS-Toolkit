# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License,  Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
import pytest

from canvas_extractor.mapping.submissions import map_to_udm_submissions


def describe_when_mapping_empty_DataFrame():
    def it_should_return_empty_DataFrame():
        df = map_to_udm_submissions(pd.DataFrame())
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
        return map_to_udm_submissions(df)

    def it_should_have_correct_number_of_columns(result):
        assert result.shape[1] == 13

    def it_should_have_schoology_as_SourceSystem(result):
        assert result["SourceSystem"].iloc[0] == "Canvas"

    def it_should_map_id_to_SourceSystemIdentifier(result):
        assert result["SourceSystemIdentifier"].iloc[0] == "130"

    def it_should_map_uid_to_LMSUserSourceSystemIdentifier(result):
        assert result["LMSUserSourceSystemIdentifier"].iloc[0] == "113"

    def it_should_map_created_to_SubmissionDateTime(result):
        assert result["SubmissionDateTime"].iloc[0] == "2020/09/14 17:23:46"

    def it_should_have_empty_SourceCreateDate(result):
        assert result["SourceCreateDate"].iloc[0] is None

    def it_should_have_empty_SourceLastModifiedDate(result):
        assert result["SourceLastModifiedDate"].iloc[0] is None
