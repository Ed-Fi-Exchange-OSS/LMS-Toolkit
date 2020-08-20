# Getting data into CSV from Canvas API

### Canvas REST API
This script gets the data from the Canvas REST API
[Canvas docs](https://canvas.instructure.com/doc/api/)

### What does it do?
Generates a CSV with information about the students that didn't complete assignments for all the courses of the year.

### How to use it
1. Run the command ``yarn install``.
2. Copy the .env.example file to .env and update its values.
3. Run the command ``node index``.
4. The CSV file should be created at the same level as the index.js file.

### .env information
CANVAS_BASE_URL=[CANVAS_BASE_URL]
> The url of the canvas instalation

ACCESS_TOKEN=[YOUR_BEARER_ACCESS_TOKEN]
> In order to work properly, it shoyld be an admin token

CANVAS_ADMIN_ID=[ADMIN_USER_ID]
> A numeric value. At this point we will just provide it manually

YEAR_TO_REPORT=2020
> The csv considers assignments from courses wich have a start_at <= YEAR_TO_REPORT or end_at >= YEAR_TO_REPORT
