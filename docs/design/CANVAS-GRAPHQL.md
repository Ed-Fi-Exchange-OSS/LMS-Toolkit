# Canvas Extractor Change to GraphQL

## Background Context

### Problem

Users of the Canvas Extractor have reported that the data extraction on even a
moderately-sized education organization runs for an excessively long time, on
the order of hours and sometimes too long to see to the end.

The development team noticed that there are a very large number of API calls,
each of which has significant overhead. For example, the process of getting
assignment information looks roughly like this:

* Get all accounts
* For each account
  * Get all courses
  * For each course
    * Get all sections
    * Get all section associations (includes users)
    * Get all assignments
    * For each assignment
      * Get all submissions

### GraphQL Spike

This is extremely "chatty". [GraphQL](https://graphql.org/) was created by
Facebook to help solve this problem of having extremely chatty REST APIs. Canvas
has a GraphQL interface. When the extractor work was started, that interface was
quite limited and the development team did not feel that it offered the needed
resources. Fast forward to February, 2022, and [recent
experiments](https://github.com/Ed-Fi-Alliance-OSS/LMS-Toolkit/blob/d2d47b6569738c85a1706589f53389e2ad74a50a/experimental/canvas/graphql/readme.md)
appear to demonstrate that the GrapQL interface has almost all of the required
data, and offers potentially an order of magnitude or better performance
improvement.

### Current Application Architecture

The following diagram is a rough sketch of the modules involved in getting data
from Canvas. "CanvasAPI" in red is a third-party Python library.

![Canvas extractor module sequence diagram](canvas-graphql-sequence.png)

This looks a little complicated. Why so many layers? One might argue that the
decomposition went too far. Each layer helped the development team reason about
the logic being applied and to operate with a meaningful interface for the data
going in either direction.

| module         | purpose                                                                                                                                                                                        |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| extract_facade | Orchestration of API calls, business logic, and write of the CSV. Can be called from the extractor's __main__.py  file, or can be called by a Jupyter notebook or another Python application.​ |
| client_facade  | Slight simplification of the API interface, returns Pandas DataFrame                                                                                                                           |
| api.courses    | courses module in api directory, serves as an adapter over CanvasAPI                                                                                                                           |

## Design for Canvas Extractor 1.3

> [!NOTE] These are initial thoughts on design, subject to change during
> implementation as the developers learn more about the interaction with Canvas.

### Pulling Data from the GraphQL Interface

Based on analysis in the [GraphQL spike
report](https://github.com/Ed-Fi-Alliance-OSS/LMS-Toolkit/tree/canvas-graphql-spike/experimental/canvas/graphql),
it appears that all data can be retrieved from [Canvas
GraphQL](https://canvas.instructure.com/doc/api/file.graphql.html) except the
authentication events. More on that in the next section.

Most of the data will be retrieved in "one" big GraphQL query ("one" in quotes
because of pagination). See the link above and
[graphql.py](https://github.com/Ed-Fi-Alliance-OSS/LMS-Toolkit/blob/d2d47b6569738c85a1706589f53389e2ad74a50a/experimental/canvas/graphql/graphql.py)
to build up the appropriate GraphQL query. The query can be tested manually at
https://edfialliance.instructure.com/graphiql.

The development team will need to inspect the actual data currently retrieved
with the Canvas Extractor, to ensure that the exact same fields are requested
from the GraphQL query.

> [!INFO] https://edfialliance.instructure.com/graphiql provides a live GraphQL
> browser for Ed-Fi developers who have access to the Ed-Fi Canvas sandbox.

### Authentication Events

The current code relies on having the list of user objects from the CanvasAPI
library. It loops through each user to get that user's authentication events.
With the change to GraphQL, the application will no longer have those objects.
In a pure library-based solution, the code would need to:

1. Get all accounts
2. vFor each account
   1. Get all users
   2. For each user
      1. Get all authentication events

The Ed-Fi sandbox account has one account with nearly 50,000 user records in it.
Retrieving all users is expensive: in one test, it took 11 minutes to retrieve
all of that data, using the default page size of 100.

However, the code will have already pulled all users who are enrolled in a
course via GraphQL. These are the users we care about. And we can make a direct
API call to retrieve information on that user with a direct API call, bypassing
CanvasAPI.

```python
user_id = 108  # SF
start_time = "2022-01-01"
end_time = "2022-02-24"

url = f"{canvas_base_url}/api/v1/audit/authentication/users/{user_id}?per_page=100&start_time={start_time}&end_time={end_time}"
headers = {"Authorization": f"Bearer {canvas_token}"}

r = requests.get(url, headers=headers)
if not r.status_code == 200:
    r.raise_for_status()

body = json.loads(r.text)
auth_events = body["events"]
print(auth_events)
```

Note carefully that this retrieves 100 events per page. This is the recommended
page size, although Canvas might support up to 200. They are cagey about what is
"reasonable." If there are more than 100 events, then there will be a Link
header on the response, like:

```none
Link: <https://edfialliance.instructure.com/api/v1/audit/authentication/users/108?end_time=2022-02-24&start_time=2022-01-01&page=first&per_page=2>; rel="current",<https://edfialliance.instructure.com/api/v1/audit/authentication/users/108?end_time=2022-02-24&start_time=2022-01-01&page=bookmark:WyJjbHVzdGVyMjYxX3NoYXJkXzE4NTU3IiwiMjAyMi0wMi0yMiAxMTo1NzoyOSAtMDYwMCJd&per_page=2>; rel="next",<https://edfialliance.instructure.com/api/v1/audit/authentication/users/108?end_time=2022-02-24&start_time=2022-01-01&page=first&per_page=2>; rel="first"
```

(:exclamation: This test used page size of 2 in order to force paging to occur).

The code will need to parse that header to find a "next" link and follow that
link. Note that the format is strange. One would expect semi-colon to separate
the three links, but instead it is the comma. The Semi-colon separates the URL
from its appropriate "rel" property. Thus rel="next"  belongs with the URL that
has page=bookmarkWyJ... .

### Putting It All Together

1. The GraphQL query will need to be build dynamically, based on the features
   that are enabled at runtime (grades, activities, assignments)
2. Create two new modules for the respective API calls:
   1. GraphQL
      1. Probably has a single method
   2. Authentication
3. Carefully ensure that both of them handle paging.
4. Carefully ensure that any post-extract business logic is preserved:
   1. Filters on state  or type  properties
   2. Date ranges
   3. De-duplication of students
5. The extract façade will need significant refactoring, naturally.

:exclamation: This looks like nearly a complete rewrite. We will still call it
version 1.3.0 to stay in sync with other applications, and because the
application interface will be unchanged.

During development, it might make sense to create a temporary new source folder
so that it remains easy to run both the new code and the old code. At the end of
the refactoring, delete the old/unused code, and move the new files into
canvas-extractor/edfi_canvas_extractor. Same naturally applies for the tests.

### User Stories

[LMS-308 - Rewrite Canvas Extractor to Use
GraphQL](https://tracker.ed-fi.org/browse/LMS-308) DONE

To make this more manageable, the following user stories are suggested (with
acceptance criteria).

1. As a data engineer, I want to extract sections from Canvas.
   1. Same runtime interface as the existing Canvas extractor
   2. Filter on the start and end date for a course (must be applied after
      extract, as GraphQL doesn't provide a query term for this)
   3. Preserve the state  filtering ("available", "completed") (applied after
      extract)
   4. Preserve the SQLite synchronization process, which detects changes since
      the last extract
   5. Preserve all output logging
   6. Same section CSV output as the existing Canvas extractor
2. As a data engineer, I want to extract students and section associations from
   Canvas. (Depends on story 1)
   1. Filter enrollment type by student (must be applied after extract)
   2. Preserve the SQLite synchronization process, which detects changes since
      the last extract
   3. Preserve all output logging
   4. Same student, and section-association  CSV output as the existing Canvas
      extractor
3. As a data engineer, I want to extract assignments from Canvas. (Depends on
   story 1)
   1. Preserve the SQLite synchronization process, which detects changes since
      the last extract
   2. Preserve all output logging
   3. Same assignment CSV output as the existing Canvas extractor
4. As a data engineer, I want to extract assignment submissions from Canvas.
   (Depends on story 3)
    1. Preserve the SQLite synchronization process, which detects changes since
       the last extract
    2. Preserve all output logging
    3. Same submissions CSV output as the existing Canvas extractor
5. As a data engineer, I want to extract section grades from Canvas. (Depends on
   story 2)
    1. Preserve the SQLite synchronization process, which detects changes since
       the last extract
    2. Preserve all output logging
    3. Same grades CSV output as the existing Canvas extractor
6. As a data engineer, I want to extract authentication events from Canvas.
   (Independent, though best to do after story 1)
    1. Preserve the SQLite synchronization process, which detects changes since
       the last extract
    2. Map event_type "login" to value "in", otherwise "out".
    3. Filter on the start and end date.
    4. Preserve all output logging
    5. Same activities CSV file as the existing Canvas extractor
