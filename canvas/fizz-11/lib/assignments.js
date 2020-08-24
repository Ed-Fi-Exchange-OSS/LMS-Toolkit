
const axios = require('./axios')

const getAssignments = async (courseId, assignmentStatus) => {
  const { data } = await axios.get(`/api/v1/courses/${courseId}/assignments?bucket=${assignmentStatus}`)
  return data
}

const getAssignmentsForCourse = async (courseId) => {

  const pastAssignments = await getAssignments(courseId, 'past')
  const overdueAssignments = await getAssignments(courseId, 'overdue')

  return [ ...pastAssignments, ...overdueAssignments ]

}

const getMissingAssignmentsForUser =  async (userId) => {
  const { data } = await axios.get(`/api/v1/users/${userId}/missing_submissions`)
  return data
}



module.exports = {
  getAssignmentsForCourse,
  getMissingAssignmentsForUser
}
