# Getting data into CSV from Canvas API

### Canvas REST API

This script gets the data from the Canvas REST API
[Canvas docs](https://canvas.instructure.com/doc/api/)

### What does it do?

Generates some CSV files with information for a specified year, extracted from Canvas REST API:

-   Courses
-   Assignments
-   Students
-   Enrollments
-   Submissions

### Requirements

-   python 3.8
-   pip 20.2.2
-   pipenv 2020.8.13

### How to use it

1. Follow the instructions from the [main readme](../README.md).
1. From the upper folder, run the command `poetry run python.exe ./data-extractor/main.py`.
1. The file will be generated in the path defined in the .env file.
