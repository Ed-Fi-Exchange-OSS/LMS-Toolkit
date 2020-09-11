# Python-Base API Exploration

Be sure to have Python 3 and poetry installed.

## Environment Setup

1. In the explorations-py folder run the command:

    ```python
    poetry install
    ```

1. In vscode type `ctrl`+`shift`+`p` and search for the command `Python: select
   interpreter`, then point it to your generated folder `explorations-py/.venv`.

## Creating CSV of Courses

1. Set up your environment as described above.
1. In the explorations-py folder, copy the `.env.example` file to `.env` and
   substitute valid values into it.
1. In the explorations-py folder, run the command:

    ```powershell
    poetry run python.exe courses-extractor/canvas.py
    ```

1. Output as of 20 Aug 1:50 pm:

    ```text
    name,id,start_date
    Algebra I,ALG-1,2020-08-17 06:00:00+00:00
    English I,ENG-1,2020-08-17 06:00:00+00:00
    ```
