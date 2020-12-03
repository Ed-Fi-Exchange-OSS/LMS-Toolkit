# Schoology Data Generator

This script generates test data and loads that data into a Schoology sandbox.

## Base Configuration

Sandbox configuration is provided through the same environment variable/command
line interface (CLI) as the extractor.  For example, the generator will
automatically make use of an existing extractor .env file.  However, the
generator only uses a subset of the extractor configuration values.

| Description | Required | Command Line Argument | Environment Variable |
| ----------- | -------- | --------------------- | -------------------- |
| Schoology API Key | yes | -k or --client-key | SCHOOLOGY_KEY |
| Schoology API Secret | yes |  -s or --client-secret | SCHOOLOGY_SECRET |
| Number of retry attempts for failed API calls | no (default: 4) | none | REQUEST_RETRY_COUNT |
| Timeout window for retry attempts, in seconds | no (default: 60 seconds) | none | REQUEST_RETRY_TIMEOUT_SECONDS |

## Additional Configuration

The number of entities to generate are currently hardcoded in the `__main__`.py
file, requiring an edit to change. For each type of entity, certain values (e.g.
valid email domains) may be hardcoded at the top of file where data generation
takes place (e.g. `users.py` for Users).

When possible, API loaders for each type of entity will have code to roll back
entity creation. This can be enabled/disabled by commenting out the usage of
_rollback* functions.

## Execution

Execute the extractor with CLI args:

```bash
poetry run python.exe tests/data_generation -k your-schoology-client-key -s your-schoology-client-secret
```

Alternately, run with environment variables or `.env` file:

```bash
poetry run python.exe tests/data_generation
```

## Output

No local output, but execution results in new test data in the specified Schoology sandbox.

## Legal Information

Copyright (c) 2020 Ed-Fi Alliance, LLC and contributors.

Licensed under the [Apache License, Version 2.0](LICENSE) (the "License").

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

See [NOTICES](NOTICES.md) for additional copyright and license notifications.
