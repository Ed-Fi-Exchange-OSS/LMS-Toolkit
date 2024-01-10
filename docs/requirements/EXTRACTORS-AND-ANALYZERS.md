# LMS Toolkit - LMS Extractors and Analyzers

## Functional Requirements Summary

As described in more detail on the [main project
page](/display/OTD/LMS+Toolkit), LMS Toolkit will produce applications
("extractors") for retrieving student classroom and usage data from various
Learning Management Systems (LMS's), including:

* Canvas
* Google Classroom
* Schoology

Additional applications ("analyzers") may be created to support analytics over
the extracted data.

## Vision

### Constraints and Assumptions

1. Desire a modular system rather than a monolithic one, so that it is easy for
   an organization to choose which parts of the system to use.
2. Asynchronous job orchestration / scheduling can best be handled by existing
   third-party utilities.
3. Intermediate data synchronization action might utilize an in-memory database.
4. Each LMS will have separate Extractor scripts.
5. CSV files will be standardized across all LMS's.
6. Each Analyzer will operate on standardized CSV files, thus making them
   LMS-independent.

### Proposed Process

A job orchestration / task scheduling service will:

1. Call an "LMS Extractor" script
    1. Which queries the LMS's API Service, then
    2. Logs information about the process and accesses synchronization data
    3. Exports data to CSV files.
2. Optionally call one or more "LMS Analyzer" scripts
    1. Which read the CSV files
    2. Analyze them (for example, calculating which students are missing
       assignment submissions), and
    3. Write additional output to CSV.

## Output Data

### Format

The output CSV files will be modeled on the Learning Management System Unified
Data Model (LMS-UDM), although not strictly adhering to it, as explained below.
The following table partially demonstrates the expected display of the CSV file
for Users, based on the data model shown in the image on the right. Note that
the `EntityStatus` in this diagram needs to be replaced with `DeletedAt`, and it
won't be included in the CSV file: it is an interpolated value, based on the
_disappearance_ of a record in the file. Note shown in the table for brevity's
sake: `SourceCreateDate`  and `SourceLastModifiedDate`, which are only populated
in the rare cases where the LMS actually records these dates. The CSV files also
have interpolated `CreateDate`  and `LastModifiedDate`  columns with dates
determined by using the [LMS Toolkit - Synchronization
Strategy](/pages/createpage.action?spaceKey=OTD&title=LMS+Toolkit+-+Synchronization+Strategy&linkCreation=true&fromPageId=83791000).

| SourceSystemIdentifier | SourceSystem | UserRole | LocalUserId | SISUserIdentifier | Name      | EmailAddress    |
| ---------------------- | ------------ | -------- | ----------- | ----------------- | --------- | --------------- |
| ​123456789             | ​Canvas      | Student​ | 654321​     | 987321456​        | John Doe​ | john.doe@a.edu​ |

#### Section-Related Resources

In resources that are "children" of a Section - for example, assignments - the
UDM will show the logical foreign key `LMSSectionIdentifier`. This value is a
synthetic primary key that is only created at the point of uploading the file
into a relational database. Within the CSV file, we can only reference the
source system identifiers - thus the Assignments CSV file will contain a column
for `LMSSectionSourceSystemIdentifier` instead of `LMSSectionIdentifier`.

#### Submission Type

Within Assignments we find an interesting edge case: Canvas allows an assignment
to have multiple "submission types", for example: _online\_entry_ and
_online\_upload_.Other systems with an equivalent field only allow one value. In
the UDM the `Assignment.SubmissionType` is modeled as a collection. To simplify
the file creation, the Canvas values will be kept in a single field as a
JSON-like array. For example:

| LMSSectionSourceSystemIdentifier | SourceSystem | SourceSystemIdentifier | Title                              | SubmissionType                              |
| -------------------------------- | ------------ | ---------------------- | ---------------------------------- | ------------------------------------------- |
| 104                              | Canvas       | 111                    | Algebra Foundations                | \['online\_text\_entry', 'online\_upload'\] |
| 104                              | Canvas       | 112                    | Solving Equations and Inequalities | \['online\_upload'\]                        |

_(Some columns were removed from this table for illustrative purposes only)_

### Filesystem

The structure of the output on the filesystem will mirror the model
relationships, for example the exported assignments file will be nested in a
directory for the section to which the assignments belong. Files will be named
based on date/time stamp. In this way, a user can always find the latest data
output by file name, which will generally contain the entire set of current data
for that area of data.

**CSV Data Storage**

```none
/ed-fi-udm-lms/users/<YYYY-mm-dd-HH-MM-SS>.csv
/ed-fi-udm-lms/sections/<YYYY-mm-dd-HH-MM-SS>.csv
/ed-fi-udm-lms/section=<id>/section-associations/<YYYY-mm-dd-HH-MM-SS>.csv
/ed-fi-udm-lms/section=<id>/assignments/<YYYY-mm-dd-HH-MM-SS>.csv
/ed-fi-udm-lms/section=<id>/assignment=<id>/submissions/<YYYY-mm-dd-HH-MM-SS>.csv
/ed-fi-udm-lms/section=<id>/grades/<YYYY-mm-dd-HH-MM-SS>.csv
/ed-fi-udm-lms/section=<id>/attendance-events/<YYYY-mm-dd-HH-MM-SS>.csv
/ed-fi-udm-lms/section=<id>/user-activities/<YYYY-mm-dd-HH-MM-SS>.csv
```

#### Out of Scope - Saving Raw JSON Data

> [!WARNING] We considered saving the raw JSON in a "landing zone", and saving
> the CSV to something like a "gold zone". At this time we do not intend to save
> the raw JSON because we do not want to support it.

To facilitate debugging, and allow for potential re-processing, the raw from API
calls will be persisted as JSON. These data may be stored on the filesystem or
in an embedded database. If stored on the filesystem, the files may be
compressed to minimize required disk space requirements. Data storage scheme to
be determined.

**JSON Raw Data Storage**

```none
/output/landing/Schoology/Year=2020/Month=09/Day=16/users-<timestamp>.json
/output/landing/Schoology/Year=2020/Month=09/Day=16/courses-<timestamp>.json
/output/landing/Schoology/Year=2020/Month=09/Day=16/sections-<timestamp>.json
/output/landing/Schoology/Year=2020/Month=09/Day=16/Section=<id>/enrollments-<timestamp>.json
/output/landing/Schoology/Year=2020/Month=09/Day=16/Section=<id>/assignments-<timestamp>.json
/output/landing/Schoology/Year=2020/Month=09/Day=16/Section=<id>/submissions-<timestamp>.json
/output/landing/Schoology/Year=2020/Month=09/Day=16/Section=<id>/grades-<timestamp>.json
```
