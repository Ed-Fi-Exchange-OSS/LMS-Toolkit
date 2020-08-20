
const axios = require('./axios')

const getAssignments = async (courseId, assignmentStatus) => {
  const { data } = await axios.get(`/api/v1/courses/${courseId}/assignments?bucket=${assignmentStatus}`)
  return data
}

const getAssignmentsForCourses = async (courses) => {
  let assignments= []

  await Promise.all(courses.map(async ({id}) => {
    const pastAssignments = await getAssignments(id, 'past')
    const overdueAssignments = await getAssignments(id, 'overdue')
    //testing purpose
    const actualAssignments = await getAssignments(id, 'unsubmitted')

    assignments = [ ...assignments, ...pastAssignments, ...overdueAssignments, ...actualAssignments ]
  }))

  return assignments
}

const getMissingAssignmentsForUser =  async (userId) => {
  const { data } = await axios.get(`/api/v1/users/${userId}/missing_submissions`)
  return data
}



module.exports = {
  getAssignmentsForCourses,
  getMissingAssignmentsForUser
}
