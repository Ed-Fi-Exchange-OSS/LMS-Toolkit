from lib.canvasRequest import get

def getStudentsForCourse(courseId):
    students = get(f"/api/v1/courses/{courseId}/users?enrollment_role_id=3")
    return students

def getEnrollmentsForStudent(userId):
    enrollments = get(f"/api/v1/users/{userId}/enrollments")
    return enrollments
