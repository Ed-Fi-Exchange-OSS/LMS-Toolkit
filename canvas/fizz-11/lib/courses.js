const axios = require('./axios')

const adminUserId = process.env.CANVAS_ADMIN_ID

const getCoursesByStatus= async (status) => {
  // this method shold handle API pagination complexity,
  // so we can make sure this will return the total of courses
  const { data: courses } = await axios.get(
    `/api/v1/accounts/${adminUserId}/courses?state=${status}`)

  return courses
}

const getAvailableCourses = async () => await getCoursesByStatus('available')
const getCompletedCourses = async () => await getCoursesByStatus('completed')

const getCoursesForYear = async (year) => {
  if (!year) console.error('You must specify a year for the method getCoursesForYear')

  const availableCourses = await getAvailableCourses()
  const completedCourses = await getCompletedCourses()

  const totalCourses = [...availableCourses, ...completedCourses]
  const coursesForYear = totalCourses.filter(
    course => {
      const courseEndYear = `${new Date(course.end_at).getFullYear()}`
      const courseStartYear = `${new Date(course.start_at).getFullYear()}`
      const yearString = `${year}`
      return courseEndYear >= yearString || courseStartYear <= yearString
    }
  )

  return coursesForYear
}

module.exports = {
  getCoursesForYear
}
