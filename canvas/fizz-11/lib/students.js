const axios = require('./axios')

const getStudentsForCourse = async (courseId) => {
  // role_id 3 is the id for student role
  const { data } = await axios.get(
    `/api/v1/courses/${courseId}/users?enrollment_role_id=3`)

  return data
}

const getEnrollmentsForStudent= async (userId) => {
  // role_id 3 is the id for student role
  const { data } = await axios.get(
    `/api/v1/users/${userId}/enrollments`)

  return data
}
//

module.exports = {
  getStudentsForCourse,
  getEnrollmentsForStudent
}
