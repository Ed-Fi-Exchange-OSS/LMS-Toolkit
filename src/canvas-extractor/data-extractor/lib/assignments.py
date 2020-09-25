# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from lib.canvasRequest import get

def getAssignments(courseId, assignmentStatus):
    assignments = get(f"/api/v1/courses/{courseId}/assignments?bucket={assignmentStatus}")
    return assignments

def getAssignmentsForCourse(courseId):
    past_assignments = getAssignments(courseId, "past")
    overdue_assignments = getAssignments(courseId, "overdue")
    return list(past_assignments + overdue_assignments)
