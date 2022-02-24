# GraphQL Exploration

## Experiment

Created two versions of a script - one using GraphQL and one using the regular
Canvas API:

* Gets the main account
* Retrieves all courses in the main account
* Retrieves all enrollments in the all of the courses
* Writes courses, enrollments, and users to CSV for comparison
* Writes execution time to the console.

Result: both scripts are returning the same information. On Stephen's computer,
`canvas_api.py` completed in average time of about 91 seconds, and `graphql.py`
completed in average time of about 7 seconds, although 10-11 seconds might be a
better estimate (first execution is always slower than repeats, perhaps due to
some database caching).

Conclusion: yes, we can get significant time savings with the GraphQL API.

## Supported Resources

Can it support everything used by the Canvas Extractor? The notes below show
separate GraphQL queries. However, the whole point of GraphQL is to minimize
API calls. Everything that falls under the `account` root can likely
be part of the same API call. Additional experimentation will be needed
to verify this, and to fully understand how to work with paging when there
are nested pages (e.g. how do you page through enrollments when you also
have paging turned on for courses?)

The notes below show _most_, but perhaps not _all_ of the individual elements
that need to be requested. Further detailed analysis will need to be carried out
while looking at the mapping of Canvas API elements to the CSV file extracts.

* Assignments - YES

  ```none
  query MyQuery {
    account(id: "1") {
      coursesConnection {
        nodes {
          _id
          name
          courseCode
          assignmentsConnection {
            nodes {
              _id
              dueAt
              dueDateRequired
              name
              pointsPossible
              submissionTypes
            }
          }
        }
      }
    }
  }
  ```

* Authentication Events (treated as "System Activities") - NO, unless overlooked
* Grades - YES

  ```none
  query MyQuery {
    account(id: "1") {
      coursesConnection {
        nodes {
          enrollmentsConnection {
            nodes {
              user {
                enrollments {
                  grades {
                    finalScore
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  ```

* Enrollments (treated as "Section Associations") - YES, see `graphql.py`.
* Sections - YES

  ```none
  query MyQuery {
    account(id: "1") {
      coursesConnection {
        nodes {
          _id
          name
          sectionsConnection {
            nodes {
              _id
              name
              sisId
            }
          }
          courseCode
        }
      }
    }
  }
  ```

* Submissions - YES

  ```none
  query MyQuery {
    account(id: "1") {
      coursesConnection {
        nodes {
          _id
          name
          courseCode
          submissionsConnection {
            nodes {
              _id
              createdAt
              grade
              gradingStatus
              late
              missing
              postedAt
              score
              state
              user {
                _id
              }
            }
          }
        }
      }
    }
  }
  ```

* Users - YES, see `graphql.py`.

## Next Steps

1. More experimentation with paging for _nested_ resources. Paging should be set at 100.
2. Combine into one big query.
3. Write that big GraphQL query and the paging process into the Canvas Extractor,
   perhaps in the API folder or directly in `client_facade`.
4. Carefully review all existing logic and bring it into the query, for example:
   * Which columns to retrieve and map into the UDM
   * Any filtering on teachers, status
   * Course dates
5. Use opnieuw on GraphQL query for rate limit handling.
6. Remove old API folder and `client_facade` code, except for System Activities.

## Resources

* [GraphiQL live explorer](https://edfialliance.instructure.com/login/canvas)
  (must have an account in the Ed-Fi sandbox).
* [Canvas REST API documentation](https://canvas.instructure.com/doc/api/)
* [Canvas GraphQL documentation](https://canvas.instructure.com/doc/api/file.graphql.html)
* [CanvasAPI Python library](https://canvasapi.readthedocs.io/en/stable/index.html)
