# Cross-Cutting Architecture Requirements and Decisions

## Purpose

This document will outline the high-level and cross-cutting architectural requirements and decisions applying to the LMS Toolkit.

## High-level Technical Requirements


1. This is an open source project, under the Apache 2.0 license.
2. The project will use the right tool for the job, with the Ed-Fi Alliance defaulting to Python-based tools for data engineering tasks.
3. Where able to do so, utilize existing 3rd party packages, only writing new code if existing packages are insufficient. Example: API client libraries for accessing an LMS.
4. Each package will be separately versioned using SemVer 2.0.
5. Package naming convention: `ed-fi-<purpose>-<type>` , example `ed-fi-canvas-extractor`, or `ed-fi-missing-assignments-analyzer`.
6. The generic application structure will be an orchestration script / program, linking to packages / modules, so that it is easy to re-use those packages / modules in different contexts. In Python tools, this would look like a `main.py`  orchestration script, runnable at the command line, along with other Python files representing the API access logic and other manipulation.
7. Ed-Fi Python tools will pass configuration data to the `main.py`  script through environment variable or command line, with command line options taking precedence, e.g. if both env var and command arg are provided, then the command arg is used.
8. TeamCity will be used for continuous integration, relying on Kotlin scripts to provide version-controlled configuration in the same repository as the main code base.

## Python-based Application Development

### Toolkit

1. [Poetry](https://python-poetry.org/) will be used for dependency management and packaging.
2. [ConfigArgParse](https://github.com/bw2/ConfigArgParse) for the `main.py` command line interface
3. [DotEnv](https://github.com/theskumar/python-dotenv) for the `main.py`  environment variable management
4. [PyTest](https://docs.pytest.org/en/stable/) will be used for test automation.
5. [Black](https://black.readthedocs.io/en/stable/) for opinionated code formatting
6. [Flake8](https://flake8.pycqa.org/en/latest/) for style enforcement
7. [Pandas](https://pandas.pydata.org/) data analysis and manipulation library
8. [Jupyter](https://jupyter.org/) notebooks for code exploration and documentation
9. [opnieuw](https://tech.channable.com/posts/2020-02-05-opnieuw.html) for retry handling
10. ... and other libraries as needed.

### Packaging and Distribution

1. Each Python package will be packed in both sdist and wheel formats.

    > "In fact, Python’s package installer, pip, always prefers wheels because
    > installation is always faster, so even pure-Python packages work better
    > with wheels."
    >
    > "Default to publishing both sdist and wheel archives
    > together,_unless_you’re creating artifacts for a very specific use case
    > where you know the recipient only needs one or the other."
    >
    > [https://packaging.python.org/overview/](https://packaging.python.org/overview/)

2. Both pre-release and release packages will be published to the [Ed-Fi Azure Artifacts feed](/display/SDLC/Azure+Artifacts+Setup).
    1. Potentially useful reference: [https://iscinumpy.gitlab.io/post/azure-devops-python-wheels/](https://iscinumpy.gitlab.io/post/azure-devops-python-wheels/)
3. Future consideration: might publish full releases to PyPi.

## Project Layout

All source code will be in [https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit)

```none
root/
- docs/             Data model and usage documentation
---- sample-in/     CSV files with fake student data for loading into the LMS
---- sample-out/    Example CSV files that match the data model
- experimental/
 src/
---- <application name>/
------- tests/
------- main.py
------- *.py
------- *.ipynb
------- poetry.lock
------- pyproject.toml
- LICENSE, README, NOTICES, etc.
```
