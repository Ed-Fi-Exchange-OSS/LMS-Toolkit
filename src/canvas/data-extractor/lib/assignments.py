from lib.canvasRequest import get

def getAssignments(courseId, assignmentStatus):
    assignments = get(f"/api/v1/courses/{courseId}/assignments?bucket={assignmentStatus}")
    return assignments

def getAssignmentsForCourse(courseId):
    past_assignments = getAssignments(courseId, "past")
    overdue_assignments = getAssignments(courseId, "overdue")
    return list(past_assignments + overdue_assignments)
