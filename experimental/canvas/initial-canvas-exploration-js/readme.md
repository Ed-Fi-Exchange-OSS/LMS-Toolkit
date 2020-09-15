# Interacting with the Canvas API

Starting point: [Canvas APIs: Getting started, the practical ins and outs,
gotchas, tips, and
tricks](https://community.canvaslms.com/t5/Developers-Group/Canvas-APIs-Getting-started-the-practical-ins-and-outs-gotchas/ba-p/263685)

Also see [Canvas OAuth2 Documentation](https://canvas.instructure.com/doc/api/file.oauth.html)

Before starting, create [developer keys](http://fizz-canvas.centralus.cloudapp.azure.com/accounts/site_admin/developer_keys#) or get a [user access token](http://fizz-canvas.centralus.cloudapp.azure.com/profile/settings) through the user interface.

## Authentication

### Manual Token Generation

> "For testing your application before you've implemented OAuth, the simplest
> option is to generate an access token on your user's profile page."

[Source](https://canvas.instructure.com/doc/api/file.oauth.html#manual-token-generation)

### Flows

Supports the following flows:

* `authorization_code`
* `refresh_token`
* `client_credentials`

The first two flows are generally used for web applications signing-in on behalf
of a user, not stand-alone clients (e.g. Postman, or an ETL script). The third
option is for applications signing-in "on their own behalf." However, it seems
that the `client_credentials` grant is primarily for supporting the LTI Advantage
services (Names and Role API, Line Items, Score, and Result).

## Client Credentials

File `client-credentials.js` will sign-in with client credentials for LTI
Advantage access. The investigation stopped at sign-in due to the lack of data
in the system. In addition, it is not yet clear if the LTA Advantage services
will actually be needed.

To setup client credentials, one must create an LTI-style Developer Key in the
Canvas Admin interface. In addition, the credentials must have a JSON Web Key
(JWK), with the public key portion assigned to the Developer Key. A
private-public key pair can be created at [mkjwk.org](https://mkjwk.org/).

Before running the script, copy the `.env.example` to `.env` and customize by
pasting in the JWK key pair and the numeric client ID for the developer key.

### Authorization Code

The authorization code flow has a redirect in the middle of it, and I have not
figured out how to get it working from Postman or node.js. File
`authorization-code.js` has some initial work that only gets as far as a user
sign-in screen. I don't understand why that is the response. I would have
expected a redirect header in order to use the "out-of-band" code to perform the
authentication, but I'm not getting that header. Might return to this at another
time.

## GraphQL with User Access Token

[Documentation](https://canvas.instructure.com/doc/api/file.graphql.html)

Acquire a token manually for the given user. Create the following request in
your favorite tool.

    POST /api/graphql HTTP/1.1
    Host: http://fizz-canvas.centralus.cloudapp.azure.com
    Authorization: Bearer <personal access token>
    Content-Type: application/x-www-form-urlencoded

    query=query { course(id: "1") { id _id name } }

Response - note there's only one course in the system at the time when this was
first tested.

    {
        "data": {
            "course": {
                "id": "Q291cnNlLTE=",
                "_id": "1",
                "name": "First Test Course"
            }
        }
    }

## REST with User Access Token

Again, using a manually-acquired token, create the following request in your favorite tool:

    GET /api/v1/courses HTTP/1.1
    Host: http://fizz-canvas.centralus.cloudapp.azure.com
    Authorization: Bearer <personal access token>

The response is more detailed than the GraphQL example, because in that example
we literally asked for only three fields.

    [
        {
            "id": 1,
            "name": "First Test Course",
            "account_id": 3,
            "uuid": "xMJH764sUgxai5cp27U77OR4cujQJjKWMqXd7Sq0",
            "start_at": null,
            "grading_standard_id": null,
            "is_public": false,
            "created_at": "2020-08-11T22:21:22Z",
            "course_code": "First",
            "default_view": "modules",
            "root_account_id": 1,
            "enrollment_term_id": 1,
            "license": "public_domain",
            "grade_passback_setting": null,
            "end_at": null,
            "public_syllabus": false,
            "public_syllabus_to_auth": false,
            "storage_quota_mb": 500,
            "is_public_to_auth_users": false,
            "apply_assignment_group_weights": false,
            "calendar": {
                "ics": "http://fizz-canvas.centralus.cloudapp.azure.com/feeds/calendars/course_xMJH764sUgxai5cp27U77OR4cujQJjKWMqXd7Sq0.ics"
            },
            "time_zone": "America/Chicago",
            "blueprint": false,
            "sis_course_id": null,
            "sis_import_id": null,
            "integration_id": null,
            "enrollments": [
                {
                    "type": "teacher",
                    "role": "TeacherEnrollment",
                    "role_id": 4,
                    "user_id": 1,
                    "enrollment_state": "active",
                    "limit_privileges_to_course_section": false
                }
            ],
            "hide_final_grades": false,
            "workflow_state": "unpublished",
            "restrict_enrollments_to_course_dates": false
        }
    ]
