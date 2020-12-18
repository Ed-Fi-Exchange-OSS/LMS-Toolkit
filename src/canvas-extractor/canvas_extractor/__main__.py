# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from typing import List
from dotenv import load_dotenv
from pandas import DataFrame
import sqlalchemy

from canvasapi import Canvas
from canvasapi.assignment import Assignment
from canvasapi.course import Course
from canvasapi.enrollment import Enrollment
from canvasapi.submission import Submission
from canvasapi.user import User


from api.assignments import assignments_synced_as_df, request_assignments
from api.courses import courses_synced_as_df, request_courses
from api.enrollments import enrollments_synced_as_df, request_enrollments
from api.students import request_students, students_synced_as_df
from api.submissions import request_submissions, submissions_synced_as_df
from config import get_canvas_api, get_sync_db_engine
# import export_data

load_dotenv()

canvas: Canvas = get_canvas_api()

courses: List[Course] = request_courses(canvas)
students: List[User] = request_students(courses)
assignments: List[Assignment] = request_assignments(courses)
submissions: List[Submission] = request_submissions(assignments)
enrollments: List[Enrollment] = request_enrollments(students)

sync_db: sqlalchemy.engine.base.Engine = get_sync_db_engine()

courses_df: DataFrame = courses_synced_as_df(courses, sync_db)
students_df: DataFrame = students_synced_as_df(students, sync_db)
assignments_df: DataFrame = assignments_synced_as_df(assignments, sync_db)
submissions_df: DataFrame = submissions_synced_as_df(submissions, sync_db)
enrollments_df: DataFrame = enrollments_synced_as_df(enrollments, sync_db)

# Temporary - just for demonstration until UDM mapping
courses_df.to_csv("data/courses.csv", index=False)
students_df.to_csv("data/students.csv", index=False)
assignments_df.to_csv("data/assignments.csv", index=False)
submissions_df.to_csv("data/submissions.csv", index=False)
enrollments_df.to_csv("data/enrollments.csv", index=False)
