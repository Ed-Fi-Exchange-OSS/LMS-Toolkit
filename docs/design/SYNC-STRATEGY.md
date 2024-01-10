# LMS Toolkit - Synchronization Strategy

## Introduction

Whenever possible, we should store API data that we have already pulled and only
request new or updated data.  This minimizes the amount of data that we pull at
any one time, which is important for data transfer times and to avoid
throttling.  This requires a persistence strategy and reconciliation process for
each incremental pull.  The process used will depend on the features of the API
to determine new and changed data.

In addition, some API resources do not provide date/time stamps for creation and
modification. These values can be inferred at the time of data extraction with
the help of this synchronization strategy, even for APIs that do not provide the
ability to perform date-limited data pulls.

## Design Notes

To date, we've settled on pandas DataFrames as the in-memory store for extractor
data.  This looks to be a good choice going forward.  They are proven to scale
well as DataFrames are used in big data applications.  In synchronizing with
pandas DataFrames, we will need to record the identity columns for each
DataFrame.  We can then take advantage of the DataFrame "drop_duplicates"
feature to dedupe records.  We should also record the import date for each row.

We will need a persistent store for our DataFrames.  Given the targeted user
base, a server-free datastore would be an ideal first step to reduce system
complexity.  SQLite is a well-known server-free option with good pandas
integration, and should be our first choice.  We should however keep our eye on
DuckDB, a server-free data store with even better pandas integration that
minimizes DataFrame memory utilization.  However, DuckDB is currently still in
preview.

SQLite itself may also be used to remove duplicates.  An incremental pull can be
appended to a SQLite table via a DataFrame.  Then, we can take advantage of
SQLite's built-in auto-incrementing "rowid" columns to dedupe with a single
DELETE query by grouping older rowids by the identity columns of the table.  For
example, with a Student table where courseId and userId are the identity:

```sql
DELETE from Students WHERE rowid NOT IN (SELECT MAX(rowid) FROM Students GROUP BY courseId, userId)
```

We will also need to manage the amount of data incoming on each request.  This
should be done where possible through a batch pull facility, by paging with a
sort order, or at a minimum just through paging.  A page should be the unit of
synchronization.  Pulls should be ready to receive a throttle notification from
APIs that are rate-limited, typically as a 429 Too Many Requests response status
code, and rate limit by following the Retry-After response header if provided,
or alternately using an exponential backoff library such as opnieuw.

Some data may be fetchable by date or date range.  We will assume that the
overall time frame for the data is a single school year.  To take advantage of
this, the extractor will need to be configured with the start of school year
date.  Data fetched in this way should preserve "as-of-date" metadata for the
day it was fetched-by (Note: This is not the same as an import date).  New
fetch-by-date actions can then begin the date range with the later of the school
year start date or immediately after the last as-of-date.  These data pulls also
be segmented by a configurable maximum time window as another way to avoid huge
date range pulls to sync up to the present.  This may mean several fetches to
bring the end of the fetch-by date range to the present date.

Other data may not be fetchable by date, but may have update timestamps as part
of the result.  If fetch results can be order by update time descending, this
would allow for paging to find the newest data by limiting results to be newer
than the latest already-imported update time.

Data synchronization becomes more complicated once data has been joined from
multiple endpoints.  Joined records would need updating if a join endpoint with
update timestamps is updated.  Joins across time windows like this can be
avoided by storing the data in the original API form.  Storage in normalized
form also allows us to avoid data duplication.  This is important because
storage space is at a premium for single workstation applications.

## Google Classroom

Google Classroom provides for fetching by date for user usage data.  The
extractor requires a start date as a parameter while also taking an optional end
date to manually limit the timeframe for pulling data.  User usage data in the
SQLite sync DB includes the date of the usage record.

Before a pull, the sync DB is queried for the last date of user usage records.
Assuming there are records, the start date for this pull is one day after the
last date in the sync DB.  Otherwise the start date is taken from the required
parameter.  The end date of the pull is either the optional end date parameter,
if one exists, or simply the date of the pull itself.

Pulled usage data is merged into the sync DB by record identity, which is user
and usage date.  If there are duplicate records due to a pull overlapping with
existing data, the old records are discarded.

### Synchronization Challenges

The original synchronization plan was for incremental data fetches to merge data
with the sync DB, with duplicates handled by new records replacing old ones.
This handles the situation of capturing updates.  However, there is no mechanism
to detect deleted records in this scheme.  In fact, these Incremental updates
will hinder the ability to detect deleted records.

## Schoology

Schoology does not support querying by date range or sorting the output results.
We can limit the assignment and submission data to only those sections that are
in specified grading periods. However the section  resource documentation has
this statement:

> View a list of sections for a course (paged). The following parameters can be
> added to this path:
>
> * include_past: Set this to 1 to include sections from expired/past grading
>   periods.

Therefore it might not be necessary to limit by grading period. Several
resources are dependent on Section. So long as we don't set include_past when
retrieving sections, then those dependent resources - for example Assignment -
will also be limited to active sections.

## Canvas

TBD
