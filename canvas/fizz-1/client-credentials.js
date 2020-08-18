const jose = require('jose');
const uuidv4 = require('uuid').v4;
const axios = require('axios');
(require('dotenv')).config();

const keyPair = JSON.parse(process.env.JWK_KEY_PAIR);
const jwk = jose.JWK.asKey(keyPair);

const assertion = {
    iss: 'https://www.ed-fi.org',
    sub: process.env.CANVAS_CLIENT_ID,
    'aud': `${process.env.CANVAS_BASE_URL}/login/oauth2/token`,
    'iat': Date.now(),
    'exp': 9000661750031,
    'jti': uuidv4()
};

const token = jose.JWT.sign(assertion, jwk);

console.log(token);

const authRequest = {
    grant_type: 'client_credentials',
    client_assertion_type: 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
    client_assertion: token,
    scope:'https://purl.imsglobal.org/spec/lti-nrps/scope/contextmembership.readonly https://purl.imsglobal.org/spec/lti-ags/scope/lineitem https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly https://purl.imsglobal.org/spec/lti-ags/scope/score'
}

var data = JSON.stringify(authRequest);

var config = {
    method: 'post',
    url: `${process.env.CANVAS_BASE_URL}/login/oauth2/token`,
    headers: {
      'Content-Type': 'application/json'
    },
    data : data
  };

  axios(config)
  .then(function (response) {
    console.log(`Access token: ${response.data.access_token}`);
  })
  .catch(function (error) {
    console.log(error);
  });
