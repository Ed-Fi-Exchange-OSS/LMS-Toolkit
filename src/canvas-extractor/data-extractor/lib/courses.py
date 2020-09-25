# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from lib.canvasRequest import get
import os
from datetime import datetime

def getCoursesByStatus(status):
    admin_user_id = os.getenv("CANVAS_ADMIN_ID")
    courses = get(f"/api/v1/accounts/{admin_user_id}/courses?state={status}")
    return courses

def getAvailableCourses():
    return getCoursesByStatus("available")

def getCompletedCourses():
    return getCoursesByStatus("completed")

def getCoursesForYear():
    available_courses = getAvailableCourses()
    completed_courses = getCompletedCourses()
    total_courses = available_courses + completed_courses
    return list(filter(filterCoursesByYear, total_courses))

def filterCoursesByYear(course):
    year = int(os.getenv("DATA_EXTRACTOR_YEAR_TO_EXTRACT"))

    course_end_year = False
    course_start_year = False
    if (course["end_at"]):
        course_end_year = datetime.strptime(course["end_at"], "%Y-%m-%d%H:%M:%SZ").year

    if (course["start_at"]):
        course_start_year = datetime.strptime(course["start_at"], "%Y-%m-%dT%H:%M:%SZ").year

    return (course_end_year and (course_end_year >= year)) or (course_start_year and (course_start_year <= year))
