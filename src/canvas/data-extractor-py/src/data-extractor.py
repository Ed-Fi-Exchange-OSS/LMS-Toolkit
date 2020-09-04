from lib import exportData
from dotenv import load_dotenv
from lib.courses import getCoursesForYear
from lib.students import getStudentsForCourse, getEnrollmentsForStudent
from lib.assignments import getAssignmentsForCourse
from lib.submissions import getSubmissionsForAssignment

load_dotenv()

all_courses = getCoursesForYear()
all_students = list()
all_assignments = list()
all_submissions = list()
all_enrollments = list()

for course in all_courses:
    course_id = course["id"]
    students = getStudentsForCourse(course_id)
    assignments = getAssignmentsForCourse(course_id)

    for assignment in assignments:
        assignment_id = assignment["id"]
        submissions_for_assignment = getSubmissionsForAssignment(course_id, assignment_id)
        all_submissions = all_submissions + submissions_for_assignment

    students = list(filter(lambda student: student not in all_students, students))
    all_students = all_students + students

    all_assignments = all_assignments + assignments

for student in all_students:
    student_id = student["id"]
    student_enrollments = getEnrollmentsForStudent(student_id)
    all_enrollments = all_enrollments + student_enrollments

exportData.ToCsv(all_courses, "courses")
exportData.ToCsv(all_students, "students")
exportData.ToCsv(all_assignments, "assignments")
exportData.ToCsv(all_submissions, "submissions")
exportData.ToCsv(all_enrollments, "enrollments")
