require('dotenv').config()
const exportData = require('./lib/exportData')
const { getCoursesForYear } = require('./lib/courses')
const { getStudentsForCourse, getEnrollmentsForStudent } = require('./lib/students')
const { getAssignmentsForCourse } = require('./lib/assignments')
const { getSubmissionsForAssignment } = require('./lib/submissions')

const getAssignments = async () => {
  const allCourses = await getCoursesForYear(process.env.YEAR_TO_REPORT)
  let allStudents = []
  let allAssignments = []
  let allSubmissions = []
  let allEnrollments = []

  for(let coursesIndex = 0; coursesIndex < allCourses.length; coursesIndex++) {
    const courseId = allCourses[coursesIndex].id
    let students = await getStudentsForCourse(courseId)
    const assignments = await getAssignmentsForCourse(courseId)

    for(let assignmentIndex = 0; assignmentIndex < assignments.length; assignmentIndex++) {
      const assignmentId = assignments[assignmentIndex].id
      const submissionsForAssigment = await getSubmissionsForAssignment(courseId, assignmentId)
      allSubmissions = [ ...allSubmissions, ...submissionsForAssigment ]
    }

    students = students.filter( newStudent => !allStudents.some( existingStudent => existingStudent.id=== newStudent.id ))
    allStudents = [ ...allStudents, ...students ]
    allAssignments = [ ...allAssignments, ...assignments ]
  }

  for(let studentsIndex = 0; studentsIndex < allStudents.length; studentsIndex++) {
    const studentEnrollments = await getEnrollmentsForStudent(allStudents[studentsIndex].id)
    allEnrollments = [ ...allEnrollments, ...studentEnrollments ]
  }

  exportData.ToCsv(allCourses, 'courses')
  exportData.ToCsv(allStudents, 'students')
  exportData.ToCsv(allAssignments, 'assignments')
  exportData.ToCsv(allSubmissions, 'submissions')
  exportData.ToCsv(allEnrollments, 'enrollments')

  return
}

getAssignments()
