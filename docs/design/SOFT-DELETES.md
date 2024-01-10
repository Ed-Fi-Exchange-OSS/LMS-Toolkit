# Defining "Soft Delete"

If a record came in from the source system "yesterday" and is no longer in the source system extract "today", then we will perform a soft delete by setting a DeletedAt column value to the current date/time stamp.

If that record re-appears then next day, we will "un-soft-delete" by changing DeletedAt back to null. Why not just write a new record?

* Preserve existing relationships.
* Preserve existing manual interventions - e.g. if upstream system does not have the SIS identifier in the record, and a system administrator performs some process to add the SIS identifier to the record, then creating a new record would force the system administrator to re-apply that intervention.

The latter logic also implies that updates should be written in place rather than performing "soft updates".

Why perform soft deletes at all? To avoid cascading deletes that may not have been intended. For example, the source system "removes" a student but continues reporting on the student enrollment in a section. With soft delete in place we need not have any confusion about the status of the student enrollment in the section: it will continue to mirror what was present in the source system.

## Naïve Approach

When pulling data from the API's provided by Canvas, Google Classroom, and Schoology, we cannot query to find out about removed  resources - things that have been deleted. If a resource disappears from the API response, then it simply disappears from the output CSV files. As a reminder, the CSV exports contain the entire available data set for the given context, rather than containing only new/modified records.

The simple - and incomplete - approach is to compare the destination table to the raw file; if any records in the table are lacking in the file, then mark them as "deleted". In this sense, records are identified by the composite natural key (SourceSystem , SourceSystemIdentifier).

## Correct Approach

The approach above is over-eager because it does not take the domain hierarchy into account. In most cases, as a single file does not contain all records for the given resource type. Instead, it contains all records of a resource type that "belong" to a particular parent node.

| Contains all records | Contains all records for given section | ... all records for given assignment |
| -------------------- | -------------------------------------- | ------------------------------------ |
| Sections             | Assignments                            | Assignment Submissions               |
| System Activities    | Attendance Events                      |                                      |
| Users                | Grades                                 |                                      |
|                      | Section Activities                     |                                      |
|                      | Section Associations                   |                                      |

Thus for the two columns on the right, it is important that we compare existing database records to the filesystem records based on not only (SourceSystem , SourceSystemIdentifier) but also the parent identifier - either LMSSectionSourceSystemIdentifier  or AssignmentSourceSystemIdentifier.

## Test Cases

End-to-end application testing can be performed using sample data, since the process above is independent of the extractors. Scenarios to cover:

### ​Sections: Soft Delete Missing Record

```none
Given ​the LMSSection table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  |
     | BestLMS      | B123456                | (null)     |
     | BestLMS      | B234567                | (null)     |

  and there is a new Sections file that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSSection table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  |
     | BestLMS      | B123456                | (null)     |
     | BestLMS      | B234567                | (not null) |
```

### Sections: Validate Matches on Source System

```none
Given ​the LMSSection table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  |
     | BestLMS      | B123456                | (null)     |
     | FirstLMS     | F234567                | (null)     |

  and there is a new Sections file that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSSection table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  |
     | BestLMS      | B123456                | (null)     |
     | FirstLMS     | F234567                | (null)     |
```

### System Activities - Soft Delete Missing Record

```none
Given ​the LMSSystemActivity table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  |
     | BestLMS      | B123456                | (null)     |
     | BestLMS      | B234567                | (null)     |

  and there is a new System Activities file that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSSystemActivity table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  |
     | BestLMS      | B123456                | (null)     |
     | BestLMS      | B234567                | (not null) |
```

### System Activities: Validate Matches on Source System

```none
Given ​the LMSSystemActivity table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  |
     | BestLMS      | B123456                | (null)     |
     | FirstLMS     | F234567                | (null)     |

  and there is a new System Activities file that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSSystemActivity table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  |
     | BestLMS      | B123456                | (null)     |
     | FirstLMS     | F234567                | (null)     |
```

### Users: Soft Delete Missing Record

```none
Given ​the LMSUser table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  |
     | BestLMS      | B123456                | (null)     |
     | BestLMS      | B234567                | (null)     |

  and there is a new Users file that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSUser table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  |
     | BestLMS      | B123456                | (null)     |
     | BestLMS      | B234567                | (not null) |
```

### Users: Validate Matches on Source System

```none
Given ​the LMSUser table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  |
     | BestLMS      | B123456                | (null)     |
     | FirstLMS     | F234567                | (null)     |

  and there is a new Users file that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSUser table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  |
     | BestLMS      | B123456                | (null)     |
     | FirstLMS     | F234567                | (null)     |
```

### Assignments: Soft Delete Missing Record

```none
Given ​the Assignment table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (null)     | B098765              |

  and there is a new Assignments file for Section B098765 that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSUser table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (not null) | B098765              |
```

### Assignments: Validate Matches on Source System

```none
Given ​the Assignment table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | FirstLMS     | F234567                | (null)     | F098765              |

  and there is a new Assignments file for Section B098765 that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSUser table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | FirstLMS     | F234567                | (null)     | F098765              |
```

### Assignments: Validate Matches on Section Identifier

```none
Given ​the Assignment table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (null)     | B109876              |

  and there is a new Assignments file for Section B098765 that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSUser table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (null)     | B109876              |
```

### Attendance: Soft Delete Missing Record

```none
Given ​the LMSUserAttendanceEvent table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (null)     | B098765              |

  and there is a new Attendance Events file for Section B098765 that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSUserAttendanceEvent table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (not null) | B098765              |
```

### Attendance: Validate Matches on Source System

```none
Given ​the LMSUserAttendanceEvent table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | FirstLMS     | F234567                | (null)     | F098765              |

  and there is a new Attendance Events file for Section B098765 that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSUserAttendanceEvent table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | FirstLMS     | F234567                | (null)     | F098765              |
```

### Assignments: Validate Matches on Section Identifier

```none
Given ​the LMSUserAttendanceEvent table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (null)     | B109876              |

  and there is a new Attendance Events file for Section B098765 that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSUserAttendanceEvent table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (null)     | B109876              |
```

### Grades: Soft Delete Missing Record

```none
Given ​the LMSGrade table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (null)     | B098765              |

  and there is a new Grades file for Section B098765 that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSGrade table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (not null) | B098765              |
```

### Grades: Validate Matches on Source System

```none
Given ​the LMSGrade table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | FirstLMS     | F234567                | (null)     | F098765              |

  and there is a new Grades file for Section B098765 that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSGrade table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | FirstLMS     | F234567                | (null)     | F098765              |
```

### Grades: Validate Matches on Section Identifier

```none
Given ​the LMSGrade table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (null)     | B109876              |

  and there is a new Grades file for Section B098765 that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSGrade table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (null)     | B109876              |
```

### Section Activities: Soft Delete Missing Record

```none
Given ​the LMSSectionActivity table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (null)     | B098765              |

  and there is a new Section Activities file for Section B098765 that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSSectionActivity table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (not null) | B098765              |
```

### Section Activities: Validate Matches on Source System

```none
Given ​the LMSSectionActivity table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | FirstLMS     | F234567                | (null)     | F098765              |

  and there is a new Section Activities file for Section B098765 that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSSectionActivity table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | FirstLMS     | F234567                | (null)     | F098765              |
```

### Section Activities: Validate Matches on Section Identifier

```none
Given ​the LMSSectionActivity table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (null)     | B109876              |

  and there is a new Section Activities file for Section B098765 that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSSectionActivity table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (null)     | B109876              |
```

### Section Association: Soft Delete Missing Record

```none
Given ​the LMSUserLMSSectionAssociation table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (null)     | B098765              |

  and there is a new Section Associations file for Section B098765 that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSUserLMSSectionAssociation table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (not null) | B098765              |
```

### Section Association: Validate Matches on Source System

```none
Given ​the LMSUserLMSSectionAssociationtable has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | FirstLMS     | F234567                | (null)     | F098765              |

  and there is a new Section Associations file for Section B098765 that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSUserLMSSectionAssociation table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | FirstLMS     | F234567                | (null)     | F098765              |
```

### Section Association: Validate Matches on Section Identifier

```none
Given ​the LMSUserLMSSectionAssociation table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (null)     | B109876              |

  and there is a new Section Associations  file for Section B098765 that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the LMSUserLMSSectionAssociation table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (null)     | B109876              |
```

### Assignment Submission: Soft Delete Missing Record

```none
Given ​the AssignmentSubmission table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | AssignmentIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (null)     | B098765              |

  and there is a new Submissions file for Section B098765 that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the AssignmentSubmission table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | AssignmentIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (not null) | B098765              |
```

### Assignment Submission: Validate Matches on Source System

```none
Given ​the AssignmentSubmission has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | FirstLMS     | F234567                | (null)     | F098765              |

  and there is a new Submissions file for Section B098765 that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the AssignmentSubmission table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | FirstLMS     | F234567                | (null)     | F098765              |
```

### Assignment Submission: Validate Matches on Section Identifier

```none
Given ​the AssignmentSubmission table has records with
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (null)     | B109876              |

  and there is a new Submissions file for Section B098765 that contains
     | SourceSystem | SourceSystemIdentifier |
     | BestLMS      | B123456                |

 When the LMS Data Store Loader runs

 Then the AssignmentSubmission table now has
     | SourceSystem | SourceSystemIdentifier | DeletedAt  | LMSSectionIdentifier |
     | BestLMS      | B123456                | (null)     | B098765              |
     | BestLMS      | B234567                | (null)     | B109876              |
```
