# Python-Base API Exploration

Be sure to have Python 3 installed; this exploration was done with 3.8.5 on
Windows, thus the executable command is `python` not `python3`.

## Virtual Environment Setup

1. Create a virtual environment:

    ```python
    python -m venv c:\virtualenv\canvas
    ```

1. Windows users: if you have not already adjusted your PowerShell execution
   policy, you'll need to do so now. Minimum level required for Python virtual
   environment:

    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```

1. In the PowerShell window where you will be invoking Python, activate the
   virtual environment:

    ```powershell
    c:\virtualenv\canvas\scripts\activate.ps1
    ```

1. Ed-Fi/MSDF staff must install the MSDF root certificate into pip to avoid
   errors. Assuming you already have msdfrootca.cer in c:\, run this command:

   ```powershell
   pip config set global.cert c:\msdfrootca.cer
   ```

Reference: [Creation of virtual
environments](https://docs.python.org/3/library/venv.html)

## Creating CSV of Courses

1. Activate the virtual environment as described above.
1. Install all required Python modules:

    ```powershell
    pip install -r requirements.txt
    ```

1. Copy the `.env.example` file to `.env` and substitute valid values into it.
1. Run the script:

    ```powershell
    python canvas.py
    ```

1. Output as of 20 Aug 1:50 pm:

    ```text
    name,id,start_date
    Algebra I,ALG-1,2020-08-17 06:00:00+00:00
    English I,ENG-1,2020-08-17 06:00:00+00:00
    ```
