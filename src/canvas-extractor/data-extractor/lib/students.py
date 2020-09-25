# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from lib.canvasRequest import get

def getStudentsForCourse(courseId):
    students = get(f"/api/v1/courses/{courseId}/users?enrollment_role_id=3")
    return students

def getEnrollmentsForStudent(userId):
    enrollments = get(f"/api/v1/users/{userId}/enrollments")
    return enrollments
