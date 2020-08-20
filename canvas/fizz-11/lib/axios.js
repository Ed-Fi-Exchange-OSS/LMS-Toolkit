const axios = require('axios')

axios.defaults.headers.common['Authorization'] = `Bearer ${process.env.ACCESS_TOKEN}`
axios.defaults.baseURL = `${process.env.CANVAS_BASE_URL}`

module.exports = axios
