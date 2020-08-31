# Generate a list of users with missing assignments

### What does it do?
Input:
CSV files with information about:
* Courses
* Assignments
* Students
* Enrollments
* Submissions

Output:
* A CVS file with information about students with missing assignments.

### How to use it
1. Run the command ``pipenv install``.
2. Copy the .env.example file to .env and update its values.
3. Enable the corresponding virtual environment.
4. Open and run the test.ipynb file

### .env information
CSV_INPUT_BASE_PATH=[PATH_WHERE_INPUT_CSV_WILL_BE_LOCATED]
> The location of the input csv files

CSV_OUTUP_PATH=[PATH_WHERE_OUTPUT_CSV_WILL_BE_LOCATED]
> The location where you want the output files to be generated

