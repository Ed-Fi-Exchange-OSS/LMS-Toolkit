# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

# #####
# ##### Commented out to preserve in case we want to try later
# #####
# ##### On hold for now, having trouble mocking out canvasapi objects
# #####


# from typing import List
# import pytest
# import pook
# from canvasapi.course import Course
# from canvas_extractor.api.courses import request_courses
# from tests.api.api_helper import MOCK_CANVAS_BASE_URL, setup_fake_canvas_object

# # unique value for each column in fixture
# ID = "1"
# NAME = "2"
# ACCOUNT_ID = "3"
# UUID = "4"
# START_AT = "5"
# START_AT_DATE = "2020-06-06"
# GRADING_STANDARD_ID = "7"
# IS_PUBLIC = "8"
# CREATED_AT = "9"
# CREATED_AT_DATE = "2020-10-10"
# COURSE_CODE = "11"
# DEFAULT_VIEW = "12"
# ROOT_ACCOUNT_ID = "13"
# ENROLLMENT_TERM_ID = "14"
# LICENSE = "15"
# GRADE_PASSBACK_SETTING = "16"
# END_AT = "17"
# PUBLIC_SYLLABUS = "18"
# PUBLIC_SYLLABUS_TO_AUTH = "19"
# STORAGE_QUOTA_MB = "20"
# IS_PUBLIC_TO_AUTH_USERS = "21"
# APPLY_ASSIGNMENT_GROUP_WEIGHTS = "22"
# CALENDAR = "23"
# TIME_ZONE = "24"
# BLUEPRINT = "25"
# SIS_COURSE_ID = "26"
# SIS_IMPORT_ID = "27"
# INTEGRATION_ID = "28"
# HIDE_FINAL_GRADES = "29"
# WORKFLOW_STATE = "30"
# RESTRICT_ENROLLMENTS_TO_COURSE_DATES = "31"
# OVERRIDDEN_COURSE_VISIBILITY = "32"


# def describe_when_requesting_latest_courses():
#     @pytest.fixture
#     def courses() -> List[Course]:
#         # arrange
#         pook.activate()
#         response_json = f"""
#         {{
#           "courses": [
#             {{
#               "id": "{ID}",
#               "name: "{NAME}",
#               "account_id: "{ACCOUNT_ID}",
#               "uuid: "{UUID}",
#               "start_at: "{START_AT}",
#               "start_at_date: "{START_AT_DATE}",
#               "grading_standard_id: "{GRADING_STANDARD_ID}",
#               "is_public: "{IS_PUBLIC}",
#               "created_at: "{CREATED_AT}",
#               "created_at_date: "{CREATED_AT_DATE}",
#               "course_code: "{COURSE_CODE}",
#               "default_view: "{DEFAULT_VIEW}",
#               "root_account_id: "{ROOT_ACCOUNT_ID}",
#               "enrollment_term_id: "{ENROLLMENT_TERM_ID}",
#               "license: "{LICENSE}",
#               "grade_passback_setting: "{GRADE_PASSBACK_SETTING}",
#               "end_at: "{END_AT}",
#               "public_syllabus: "{PUBLIC_SYLLABUS}",
#               "public_syllabus_to_auth: "{PUBLIC_SYLLABUS_TO_AUTH}",
#               "storage_quota_mb: "{STORAGE_QUOTA_MB}",
#               "is_public_to_auth_users: "{IS_PUBLIC_TO_AUTH_USERS}",
#               "apply_assignment_group_weights: "{APPLY_ASSIGNMENT_GROUP_WEIGHTS}",
#               "calendar: "{CALENDAR}",
#               "time_zone: "{TIME_ZONE}",
#               "blueprint: "{BLUEPRINT}",
#               "sis_course_id: "{SIS_COURSE_ID}",
#               "sis_import_id: "{SIS_IMPORT_ID}",
#               "integration_id: "{INTEGRATION_ID}",
#               "hide_final_grades: "{HIDE_FINAL_GRADES}",
#               "workflow_state: "{WORKFLOW_STATE}",
#               "restrict_enrollments_to_course_dates: "{RESTRICT_ENROLLMENTS_TO_COURSE_DATES}",
#               "overridden_course_visibility: "{OVERRIDDEN_COURSE_VISIBILITY}"
#             }}
#           ]
#         }}
#         """
#         pook.get(
#             f"{MOCK_CANVAS_BASE_URL}/api/v1/accounts",
#             response_json="""{
#                 "id": "1",
#                 "name": "111",
#                 "uuid": "222",
#                 "workflow_state": "active"
#             }""",
#             reply=200,
#         )
#         pook.get(
#             f"{MOCK_CANVAS_BASE_URL}/api/v1/accounts/1/courses",
#             response_json=response_json,
#             reply=200,
#         )

#         # act
#         return request_courses(setup_fake_canvas_object())

#     def it_should_have_correct_shape(courses):
#         assert len(courses) == 1
#         assert len(courses[0]) == 32

#     def it_should_map_dataframe_columns_correctly(courses):
#         row_dict = courses[0]
#         assert row_dict["id"] == ID
#         assert row_dict["name"] == NAME
