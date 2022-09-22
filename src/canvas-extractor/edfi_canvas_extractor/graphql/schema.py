# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


from typing import Optional


def query_builder(
    account_id: int,
    after_cursor: Optional[str] = ""
) -> str:
    """
    a Query to GraphQL to obtain the data

    Parameters
    ----------
    account_id: str
        an account id to get from GraphQL
    after_cursor: str, optional
        to switch between results pages

    Returns
    -------
    string
        a query with parameters to get from GraphQL
    """
    ACCOUNT_ID = account_id
    PAGE_SIZE = 10

    query = f"""
      query {{
        account(id: {ACCOUNT_ID}) {{
            coursesConnection(first: {PAGE_SIZE}, after: "{after_cursor}") {{
            nodes {{
                term {{
                  startAt
                  endAt
                  coursesConnection {{
                    nodes {{
                      _id
                      name
                      state
                      sectionsConnection {{
                          nodes {{
                          _id
                          name
                          sisId
                          createdAt
                          updatedAt
                        }}
                      }}
                      enrollmentsConnection {{
                        nodes {{
                          _id
                          createdAt
                          updatedAt
                          state
                          type
                          section {{
                            _id
                          }}
                          user {{
                              _id
                              sisId
                              createdAt
                              email
                              name
                              loginId
                          }}
                        }}
                      }}
                    }}
                  }}
                }}
              }}
              pageInfo {{
                hasNextPage
                endCursor
              }}
            }}
          }}
        }}
    """

    return query