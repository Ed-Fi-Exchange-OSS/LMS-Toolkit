# FIZZ-16: Extract login and access data for students in Canvas LMS

## Goal

### Story

As a school district, I want to know if the student engaged with my Canvas
LMS and/or a particular course on a particular school day

### Acceptance Criteria

A capture of these data points, or an assessment that these are not available

1. If a student logged into Canvas on a particular school day
1. A metric of either how long the student was logged in or how many Canvas
   resources (courses, assignments or other system entity) were accessed by a
   student on a particular day
1. If a student logged into a particular Canvas course on a particular school
   day
1. A metric of either how long the student was logged in to a course or how many
   Canvas resources in that course the student accessed on a particular day

## Getting Started

1. If you don't already have it, install
   [pipenv](https://docs.pipenv.org/install). (!) WARNING! pipenv does not like
   it if you have multiple versions of Python installed. You may run into errors
   in that case.

    ```powershell
    pip install --user pipenv
    ```

2. And add this path to your PATH environment variable (assuming you are running
   Python 3.8): `%APPDATA%\Python\Python38\scripts`.

3. (!) If on the MSDF network, first get a copy of the MSDF root certificate and
   place it in your `c:\`, then run the following in your PowerShell window,
   otherwise the `pipenv install` command will fail.

    ```powershell
    $env:REQUESTS_CA_BUNDLE="C:\msdfrootca.cer"
    ```

4. Now run `pipenv install` to install required modules.

5. Open `explore.ipynb` in your favorite Jupyter platform and run it.

