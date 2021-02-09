# LMS Toolkit

The LMS Toolkit helps school districts unlock, transform and simplify, and use
instructional system data.

The Toolkit's initial use cases focus on student assignment completion /
delinquency, and on general student activity and "presence" in instructional
systems. You can read more about this on [Ed-Fi Tech
Docs](https://techdocs.ed-fi.org/display/EDFITOOLS/LMS+Toolkit).

## Getting Started

All of the tools in this repository require [Python
3.8](https://www.python.org/downloads/release/python-380/) or higher and
[Poetry](https://python-poetry.org/docs/). Please install both and insure the
`python` and `poetry` commands are available in your command path before trying
to run any of the tools.

## Tools

The Toolkit consists of extractors and loaders:

* **LMS Extractors**: utilities that extracts data from important K12 instructional
  systems and merges that data into a common format ([LMS Unifying Data
  Model](https://techdocs.ed-fi.org/display/EDFITOOLS/LMS+Unifying+Data+Model)),
  as CSV files. Extractors are available for the following platforms:
  * [Canvas](src/canvas-extractor)
  * [Google Classroom](src/google-classroom-extractor)
  * [Schoology](src/schoology-extractor)
* **LMS Loader**: pushes CSV files into a relational database. :exclamation:
    [LMS Data Store Loader](src/lms-ds-loader) is currently in proof-of-concept stage,
    only capable of uploading User files.

We also anticipate utilities and features that help reconcile this instructional
data with data from SIS and assessment systems.

## Data Analysis Documentation

Several [Jupyter Notebooks](src/notebooks/readme.md) have been developed to
document the output files and provide sample analyses:

* [Filesystem Tutorial/In Danger of
  Failing](src/notebooks/filesystem-tutorial.ipynb)
* [User Login Activity](src/notebooks/student_logins.ipynb)
* [Student Assignment Submissions](src/notebooks/student_submissions.ipynb)

## Developer Information

* [Build script](docs/build.md): a Python script to automate common developer
  operations.
* [Continuous Integration](actions/): automated unit testing and more, using GitHub Actions.
* [File Tester](utils/file-tester): a script for validating the directory
  structure, columns, and some formatting details for files created by the
  extractor utilities.
* [Ed-Fi Tracker: Project Fizz](https://tracker.ed-fi.org/browse/FIZZ): issue tracking.
* The [experimental](experimental) directory contains proof of concept code used
  to help develop the extractors. These projects have been kept for historical
  access by the core development team, and are unlikely to be of interest to
  anyone else.
* The [docs](docs) directory contains additional documentation, including diagrams developed using [draw.io](https://draw.io), sample output files, MetaEd files defining the data model, and SQL scripts for generating database tables that will eventually be populated using the LMS Data Store Loader.

## Legal Information

Copyright (c) 2020 Ed-Fi Alliance, LLC and contributors.

Licensed under the [Apache License, Version 2.0](LICENSE) (the "License").

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

See [NOTICES](NOTICES.md) for additional copyright and license notifications.
