# file-tester

| WARNING: this utility is currently out of date as of the release of version 1.0 |
| -- |

## User Story

As an Ed-Fi developer, I want to run extractor output files through a simple
automated tester, so that I can validate the file formatting.

## Acceptance Criteria

* Confirms file paths
* Confirms that files are named with the datetime stamp.
* Confirms that each file type has the right columns.
* Confirms that all "DateTime" columns use format like 2020-11-12 13:21.
* Python script that accepts a base path and then checks files from there
* The source of the files should not matter (e.g. Schoology, Canvas, etc.)

## Usage

```bash
cd utils/file-tester
poetry install

# Let's test this repository's sample files.
poetry run python lms_file_tester ../../docs/sample-out

# Suppress informational messages - focus only on the problems
poetry run python lms_file_tester ../../docs/sample-out WARNING
```

## Example

Example of output from the `sample-out` directory:

```bash
2020-12-04 11:54:29,257 - INFO - __main__ - Starting LMS File Tester
2020-12-04 11:54:29,257 - INFO - __main__ - Basic directory structure is valid.
2020-12-04 11:54:29,265 - WARNING - __main__ - Users file contains extra columns {none} and is missing columns {'SourceCreateDate', 'SourceLastModifiedDate'}
2020-12-04 11:54:29,265 - WARNING - __main__ - Users file has an invalid timestamp format for CreateDate
2020-12-04 11:54:29,266 - WARNING - __main__ - Users file has an invalid timestamp format for LastModifiedDate
2020-12-04 11:54:29,268 - WARNING - __main__ - Sections file contains extra columns {none} and is missing columns {'SourceCreateDate', 'SourceLastModifiedDate'}
2020-12-04 11:54:29,268 - WARNING - __main__ - Sections file has an invalid timestamp format for CreateDate
2020-12-04 11:54:29,268 - WARNING - __main__ - Sections file has an invalid timestamp format for LastModifiedDate
2020-12-04 11:54:29,271 - WARNING - __main__ - Missing directory: ../../docs/sample-out\section=123456780\section-activities
2020-12-04 11:54:29,274 - INFO - __main__ - Assignment directory structure is valid for section 123456780, assignment 2942251001.
2020-12-04 11:54:29,275 - WARNING - __main__ - Missing directory: ../../docs/sample-out\section=123456780\assignment=2942251002\submissions
2020-12-04 11:54:29,280 - WARNING - __main__ - Submissions file contains extra columns {none} and is missing columns {'SourceCreateDate', 'SourceLastModifiedDate'}
2020-12-04 11:54:29,281 - WARNING - __main__ - Submissions file has an invalid timestamp format for SubmissionDateTime
2020-12-04 11:54:29,281 - WARNING - __main__ - Submissions file has an invalid timestamp format for CreateDate
2020-12-04 11:54:29,281 - WARNING - __main__ - Submissions file has an invalid timestamp format for LastModifiedDate
2020-12-04 11:54:29,281 - WARNING - __main__ - Missing directory: ../../docs/sample-out\section=123456789\section-activities
2020-12-04 11:54:29,284 - INFO - __main__ - Assignment directory structure is valid for section 123456789, assignment 2942251012.
2020-12-04 11:54:29,289 - WARNING - __main__ - Submissions file contains extra columns {none} and is missing columns {'SourceCreateDate', 'SourceLastModifiedDate'}
2020-12-04 11:54:29,289 - WARNING - __main__ - Submissions file has an invalid timestamp format for SubmissionDateTime
2020-12-04 11:54:29,289 - WARNING - __main__ - Submissions file has an invalid timestamp format for CreateDate
2020-12-04 11:54:29,289 - WARNING - __main__ - Submissions file has an invalid timestamp format for LastModifiedDate
2020-12-04 11:54:29,290 - WARNING - __main__ - Missing directory: ../../docs/sample-out\section=2385758954\section-associations
2020-12-04 11:54:29,290 - WARNING - __main__ - Missing directory: ../../docs/sample-out\section=2385758954\assignments
2020-12-04 11:54:29,290 - WARNING - __main__ - Missing directory: ../../docs/sample-out\section=2385758954\grades
2020-12-04 11:54:29,291 - WARNING - __main__ - Missing directory: ../../docs/sample-out\section=123456791\section-associations
2020-12-04 11:54:29,291 - WARNING - __main__ - Missing directory: ../../docs/sample-out\section=123456791\section-activities
2020-12-04 11:54:29,291 - WARNING - __main__ - Missing directory: ../../docs/sample-out\section=123456791\assignments
2020-12-04 11:54:29,291 - WARNING - __main__ - Missing directory: ../../docs/sample-out\section=123456791\grades
2020-12-04 11:54:29,296 - WARNING - __main__ - Attendance Events file contains extra columns {'UserLMSSectionAssociationSourceSystemIdentifier', 'UserSourceSystemIdentifier', 'SectionAssociationSystemIdentifier'} and is missing columns {'SourceCreateDate', 'LMSUserSourceSystemIdentifier', 'SourceLastModifiedDate', 'LMSUserLMSSectionAssociationSourceSystemIdentifier', 'LMSSectionAssociationSystemIdentifier'}
2020-12-04 11:54:29,296 - WARNING - __main__ - Attendance Events file has an invalid timestamp format for EventDate
2020-12-04 11:54:29,297 - WARNING - __main__ - Attendance Events file has an invalid timestamp format for CreateDate
2020-12-04 11:54:29,297 - WARNING - __main__ - Attendance Events file has an invalid timestamp format for LastModifiedDate
2020-12-04 11:54:29,305 - WARNING - __main__ - Grades file contains extra columns {none} and is missing columns {'SourceCreateDate', 'SourceLastModifiedDate'}
2020-12-04 11:54:29,305 - WARNING - __main__ - Grades file has an invalid timestamp format for CreateDate
2020-12-04 11:54:29,308 - WARNING - __main__ - Grades file has an invalid timestamp format for LastModifiedDate
2020-12-04 11:54:29,318 - WARNING - __main__ - Assignments file contains extra columns {none} and is missing columns {'SourceCreateDate', 'SourceLastModifiedDate'}
2020-12-04 11:54:29,328 - WARNING - __main__ - Section Associations file contains extra columns {none} and is missing columns {'SourceCreateDate', 'SourceLastModifiedDate'}
2020-12-04 11:54:29,328 - WARNING - __main__ - Section Associations file has an invalid timestamp format for StartDate
2020-12-04 11:54:29,329 - WARNING - __main__ - Section Associations file has an invalid timestamp format for EndDate
2020-12-04 11:54:29,329 - WARNING - __main__ - Section Associations file has an invalid timestamp format for CreateDate
2020-12-04 11:54:29,331 - WARNING - __main__ - Section Associations file has an invalid timestamp format for LastModifiedDate
2020-12-04 11:54:29,336 - WARNING - __main__ - Section Activities file contains extra columns {none} and is missing columns {'SourceCreateDate', 'SourceLastModifiedDate'}
2020-12-04 11:54:29,337 - WARNING - __main__ - Section Activities file has an invalid timestamp format for ActivityDateTime
2020-12-04 11:54:29,338 - WARNING - __main__ - Section Activities file has an invalid timestamp format for CreateDate
2020-12-04 11:54:29,340 - WARNING - __main__ - Section Activities file has an invalid timestamp format for LastModifiedDate
2020-12-04 11:54:29,341 - INFO - __main__ - System Activities directory structure is valid.
2020-12-04 11:54:29,350 - WARNING - __main__ - System Activities file contains extra columns {none} and is missing columns {'SourceCreateDate', 'SourceLastModifiedDate'}
2020-12-04 11:54:29,350 - WARNING - __main__ - System Activities file has an invalid timestamp format for ActivityDateTime
```

Of note:

* Some datetime values are incorrect.
* A few directories are missing (we now prefer to create directories and files
  even when there are no data to report on).
* The attendance event file is out of date with some changes, e.g. "User" to
  "LMSUser".
* None of the files has the new `SourceCreateDate` and `SourceLastModifiedDate`
  columns.

These are all easy things to correct, and the files will be clean by the time
anyone reads this. However, we will not add empty files or directories into
source control.
