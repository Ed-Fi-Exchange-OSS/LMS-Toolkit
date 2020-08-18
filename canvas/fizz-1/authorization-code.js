const axios = require('axios');
(require('dotenv')).config();

const baseUrl = process.env.CANVAS_BASE_URL;
const clientId = process.env.CANVAS_CLIENT_ID;
const redirect = "urn:ietf:wg:oauth:2.0:oob"; //"https://www.ed-fi.org"

var config = {
  method: 'get',
  url: `${baseUrl}/login/oauth2/auth?client_id=${clientId}&response_type=code&state=YYY&redirect_uri=${redirect}`,
};

axios(config)
.then(function (response) {
    // response.data contains HTML!
    // Hunting for the authenticity_token value.
    const pattern = /name=\"authenticity_token\" value=\"([^\"]+)"/;
    const matches = pattern.exec(response.data);
    if (matches) {
        const authenticityToken = matches[1];
    }

    // hm... that's a csrf token
    khLhN8L35/3pvFWbl9UK/k8mI3MKemnL2W1tsIpHubjeWJAFicOIqoqIP96nslCYNhZaBHotAZGwWx3d5AHI6A==
    // Now back to Canvas

    // have not figured out how to do this yet. Might not even be feasible. User
    // access token seems the simplest approach.

})
.catch(function (error) {
  console.log(error);
});
