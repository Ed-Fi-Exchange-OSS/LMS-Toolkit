# Canvas Data Generator

This script generates test data and loads that data into a Canvas sandbox.

## Base Configuration

Sandbox configuration is provided through the same environment variable/command
line interface (CLI) as the extractor.  For example, the generator will
automatically make use of an existing extractor .env file.  However, the
generator only uses a subset of the extractor configuration values.

| Description | Required | Command Line Argument | Environment Variable |
| ----------- | -------- | --------------------- | -------------------- |
| Base Canvas URL | yes | `-b` or `--base-url` | CANVAS_BASE_URL |
| Canvas API access token | yes | `-a` or `--access-token` | CANVAS_ACCESS_TOKEN |
| Output Directory | no (default: [working directory]/data) | `-o` or `--output-directory` | OUTPUT_DIRECTORY |
| Start date, yyyy-mm-dd format | yes | `-s` or `--start_date` | START_DATE |
| End date, yyyy-mm-dd format | yes | `-e` or `--end_date` | END_DATE |
| Log level | no (default: INFO) | `-l` or `--log-level` | LOG_LEVEL |

## Configuration Requiring Code Changes

The `__main__.py` contains constants controlling the number of entities
to be generated and loaded for each entity type. These should be edited
directly in the file to tune the generator.

Additionally, at the end of `__main__.py` rollbacks are performed on all loaded data,
removing that just-created data from Canvas. Comment out the rollback section
to preserve the data in Canvas.

## Execution

Execute the extractor with CLI args:

```bash
poetry run python.exe tests/data_generation -b your-base-url -a your-access-token
```

Alternately, run with environment variables or `.env` file:

```bash
poetry run python.exe tests/data_generation
```

## Output

No local output, but execution results in new test data in the specified Canvas sandbox.

## Legal Information

Copyright (c) 2020 Ed-Fi Alliance, LLC and contributors.

Licensed under the [Apache License, Version 2.0](LICENSE) (the "License").

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

See [NOTICES](NOTICES.md) for additional copyright and license notifications.
