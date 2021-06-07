# lms-harmonizer

Utility / process for linking LMS data with SIS data in an Ed-Fi ODS. Assumes
that LMS data have been retrieved from an LMS via an LMS Extractors and uploaded
into tables in the lms schema via LMS Data Store Loader.


## Getting Started

1. Requires Python 3.9+ and Poetry.
1. Install required Python packages:

   ```bash
   poetry install
   ```

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

_Also see
[build.py](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/docs/build.md)_
for use of the build script.

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

