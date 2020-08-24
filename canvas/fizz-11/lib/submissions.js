const axios = require('./axios')

const getSubmissionsForAssignment = async (courseId, assignmentId) => {
  const { data } = await axios.get(`/api/v1/courses/${courseId}/assignments/${assignmentId}/submissions`)
  return data
}

// const getSubmissionsForAssignment= async (assignment) => {
//   const { id } = assignment
//   const pastAssignments = await getAssignments(id, 'past')
//   const overdueAssignments = await getAssignments(id, 'overdue')
//   //testing purpose

//   return [ ...pastAssignments, ...overdueAssignments, ...actualAssignments ]
// }

module.exports = {
  getSubmissionsForAssignment
}
