# lms-harmonizer

Utility / process for linking LMS data with SIS data in an Ed-Fi ODS. Assumes
that LMS data have been retrieved from an LMS via an LMS Extractors and uploaded
into tables in the lms schema via LMS Data Store Loader.

## Harmonization Process

The primary duty of the LMS Harmonizer is to match Student and Sections found in
the data extracted from upstream Learning Management Systems (LMS) with the same
entities in an Ed-Fi ODS database, which are sourced from a Student Information
System (SIS). These systems often do not have perfect alignment, so that the
"harmonization" process used by this tool is imperfect and may need
customization to fit your implementation.

Any LMS records that cannot be matched to SIS records are considered
"exceptions"; you can generate CSV exports listing the exceptions by using one
of the command line options described below. With that information, you can then
either update the LMS source system by providing it with additional information,
or you can customize this process.

The out-of-the box solution has the following mapping logic:

### Student Mapping

For Canvas and Schoology, the default assumption is that the SIS's unique
identifier for the student, which has been loaded into the
`Student.StudentUniqueId` field via the Ed-FI ODS / PAI, has also been loaded
into the LMS in the following field:

* Canvas: `sis_user_id` ([API documentation](https://canvas.instructure.com/doc/api/users.html#User))
* Schoology: `school_uid` ([API documentation](https://developers.schoology.com/api-documentation/rest-api-v1/user))

Google Classroom does not have such a field. Instead, the Harmonizer assumes
that the student's email address used in Google Classroom is also recorded in
the SIS and loaded into the ODS. The Harmonizer then does a simple matching of
records by that email address, under the assumption that no two students have
the same email address.

### Section Mapping

The solution currently assumes that the SIS has a globally-unique identifier,
which has been loaded into the `Section.SectionIdentifier` field in the ODS /
API. This same value is then assumed to be loaded into the following field for each LMS:

* Canvas: `sis_section_id` on a course ([API
  documentation](https://canvas.instructure.com/doc/api/courses.html))
* Google Classroom: `course.aliases` object ([API
  documentation](https://developers.google.com/classroom/reference/rest/v1/courses.aliases))
* Schoology: `section_school_code` on a course section ([API
  documentation](https://developers.schoology.com/api-documentation/rest-api-v1/course-section))

### Customization

If your implementation does not match the logic described above, then you can clone
this repository and modify the stored procedures to fit alternate logic.

## Getting Started

1. Requires Python 3.9+ and Poetry.
1. Requires that you have the ODS/API Suite 3, Version 5.2 and have [installed the
   Ed-Fi-LMS extension](../../docs/installing-the-extension.md).
1. Manually install the stored procedures and views used by the Harmonizer
   (NOTE: the development team is exploring automation options) into your ODS
   database. These are in
   [extension/EdFi.Ods.Extensions.LMSX/Artifacts/LMS-Harmonizer](../../extension/EdFi.Ods.Extensions.LMSX/Artifacts/LMS-Harmonizer)
1. Install required Python packages:

   ```bash
   poetry install
   ```

## Configuration

Supported parameters:

| Description                 | Required            | Command Line Argument                   | Environment Variable        |
| --------------------------- | ------------------- | --------------------------------------- | --------------------------- |
| DB Server                   | yes                 | `-s` or `--server`                      | DB_SERVER                   |
| DB Port                     | no (default: 1433)  | `--port`                                | DB_PORT                     |
| DB Name                     | yes                 | `-d` or `--dbname`                      | DB_NAME                     |
| Exceptions report directory | no (no default)     | `-e` or `--exceptions-report-directory` | EXCEPTIONS_REPORT_DIRECTORY |
| DB Username **              | no (no default)     | `-u` or `--username`                    | DB_USERNAME                 |
| DB Password **              | no (no default)     | `-p` or `--password`                    | DB_PASSWORD                 |
| Use integrated security **  | no (default: false) | `-i` or `--useintegratedsecurity`       | USE_INTEGRATED_SECURITY     |
| Log level*                  | no (default: INFO)  | `-l` or `--log-level`                   | LOG_LEVEL                   |
| Encrypt db connection       | no (default: False) | `-n` or `--encrypt`                     | ENCRYPT_SQL_CONNECTION      |
| Trust db server certificate | no (default: False) | `-t` or `--trust-certificate`           | TRUST_SERVER_CERTIFICATE    |

\* Valid values for the optional _log level_:

* DEBUG
* INFO(default)
* WARNING
* ERROR
* CRITICAL

\** If using integrated security, DB Username and password won't be required,
otherwise they are required.

## Running the Tool

For detailed help, execute `poetry run python edfi_lms_harmonizer -h`.

Sample call using full integrated security, loading from the sample files
directory:

```bash
poetry run python edfi_lms_harmonizer --server localhost --dbname lms_toolkit --useintegratedsecurity
```

## Developer Notes

### Dev Operations

1. Style check: `poetry run flake8`
1. Static typing check: `poetry run mypy .`
1. Run unit tests: `poetry run pytest`
1. Run unit tests with code coverage: `poetry run coverage run -m pytest`
1. View code coverage: `poetry run coverage report`
1. Run SQL integration tests: `poetry run pytest tests_integration_sql`

_Also see
[build.py](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/docs/build.md)_
for use of the build script.

### Integration Testing

See [Integration test setup](./tests_integration_sql/README.md) for information on
configuring integration testing to work in various environments.

## Legal Information

Copyright (c) 2021 Ed-Fi Alliance, LLC and contributors.

Licensed under the [Apache License, Version
2.0](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/LICENSE) (the
"License").

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

See
[NOTICES](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/NOTICES.md)
for additional copyright and license notifications.
