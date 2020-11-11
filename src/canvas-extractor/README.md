# Canvas LMS

This project provides tools to extract data from Canvas via the Canvas API
and analyze that data.

This data extractor targets two audiences. The first is someone who wants
the data out of Canvas LMS into a .csv file that can be loaded into a
spreadsheet. The second for someone who is familiar with Jupyter Notebook, a
common Python-based tool for analysis and reporting.

## Folder Structure

You can explore the work done by navigating across the sub-folders.

## Installing and running the tools

### Requirements

1. Python 3.8
1. Poetry 1.0.10
1. [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
1. Optional: Latest version of VS Code

### Configuring Canvas

To use the Canvas API, you will need to get an "API access token."

In Canvas, data privileges are by user account, and access tokens are tied to
user accounts, so you need to be able to login to Canvas as a user who has
access privileges over the data for your organization - i.e. probably an
administrator account.

1. Login to Canvas (see note above about account privileges)
2. Go to Account >> Settings
3. Go to the section "Approved Integrations" and click on "New Access Token"
4. Fill out the fields and click "Generate Token". It is recommended you
    provide an expiration date.
5. On the popup screen, copy down the long string that appears beside "Token:"
    - this is your access token.

Note that this token will provide access to data that mirrors the access of the
user account it is connected to, so if you are not in an administrator account,
less data will be available when you use the API using this token.

### Installation

Follow these steps to install:

1. Run the command `poetry install` in this folder.
2. Copy the .env.example file to a file named '.env' and update its values. Most
   of these are just system paths or the URL of the Canvas installation. You
   will need the access token you created earlier for this step.

## Running the tools

### PowerShell

1. Run the script

    ```powershell
    poetry run python.exe ./data-extractor/main.py
    ```



