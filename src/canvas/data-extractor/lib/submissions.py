from lib.canvasRequest import get
import os

def getSubmissionsForAssignment(courseId, assignmentId):
    submissions = get(f"/api/v1/courses/{courseId}/assignments/{assignmentId}/submissions")
    return submissions
