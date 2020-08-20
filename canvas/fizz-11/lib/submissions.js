const axios = require('./axios')

const getSubmissions = async (courseId, assignmentId) => {
  const { data } = await axios.get(`/api/v1/courses/${courseId}/assignments/${assignmentId}/submissions`)
  return data
}

const getSubmissionsForAssignments= async (assignments) => {
  let submissions= []

  await Promise.all(courses.map(async ({id}) => {
    const pastAssignments = await getAssignments(id, 'past')
    const overdueAssignments = await getAssignments(id, 'overdue')
    //testing purpose
    const actualAssignments = await getAssignments(id, 'unsubmitted')

    assignments = [ ...assignments, ...pastAssignments, ...overdueAssignments, ...actualAssignments ]
  }))
}
