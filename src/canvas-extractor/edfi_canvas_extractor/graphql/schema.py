# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Optional


def query_builder(account_id: int, after_cursor: Optional[str] = "") -> str:
    ACCOUNT_ID = account_id
    PAGE_SIZE = 10

    return f"""
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
                          sisId
                          name
                          createdAt
                          updatedAt
                        }}
                      }}
                      enrollmentsConnection {{
                        nodes {{
                          _id
                          state
                          type
                          user {{
                              _id
                              email
                              name
                              sisId
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
