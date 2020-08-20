require('dotenv').config()
const exportData = require('./lib/exportData')
const { getCoursesForYear } = require('./lib/courses')
const { getStudentsForCourse } = require('./lib/students')
const { getMissingAssignmentsForUser } = require('./lib/assignments')

const getAssignments = async () => {
  const courses = await getCoursesForYear(process.env.YEAR_TO_REPORT)
  const coursesToPrint = []

  for(let coursesIndex= 0; coursesIndex<courses.length; coursesIndex++) {
    const courseId = courses[coursesIndex].id
    const students = await getStudentsForCourse(courseId)
    const studentsWithMissingAssignments = []

    for(let studentsIndex= 0; studentsIndex<students.length; studentsIndex++) {
      const userId = students[studentsIndex].id
      const missingAssignments = await getMissingAssignmentsForUser(userId)
      const missingAssignmentsForCourse = missingAssignments
        .filter(missingAssignment => missingAssignment.course_id === courseId)

      if (missingAssignmentsForCourse && missingAssignmentsForCourse.length) {
        students[studentsIndex].missingAssignments = missingAssignmentsForCourse
        studentsWithMissingAssignments.push(students[studentsIndex])
      }
    }

    if(studentsWithMissingAssignments.length > 0) {
      courses[coursesIndex].studentsWithMissingAssignments = studentsWithMissingAssignments
      coursesToPrint.push(courses[coursesIndex])
    }
  }

  exportData.ToCsv(coursesToPrint, 'students_with_missing_assignments')

  return coursesToPrint
}

getAssignments()
