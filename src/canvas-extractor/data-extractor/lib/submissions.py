# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from lib.canvasRequest import get
import os

def getSubmissionsForAssignment(courseId, assignmentId):
    submissions = get(f"/api/v1/courses/{courseId}/assignments/{assignmentId}/submissions")
    return submissions
