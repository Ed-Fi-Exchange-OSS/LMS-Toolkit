const axios = require('./axios')

const getStudentsForCourse = async (courseId) => {
  const { data } = await axios.get(
    `/api/v1/courses/${courseId}/users?enrollment_role_id=3`)
  return data
}

module.exports = {
  getStudentsForCourse
}
