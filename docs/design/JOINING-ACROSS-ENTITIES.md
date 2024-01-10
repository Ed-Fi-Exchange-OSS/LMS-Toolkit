# LMS - Joining Entities across Systems

## The Problem

With the LMS Toolkit and the work towards a future an Ed-Fi [LMS
API](/display/EXCHANGE/LMS+API), a important problem to resolve is how to join
records across LMS and SIS systems: how do we determine that two data records
from these two disparate systems refer to the same real-world entity?

Given the LMS use cases as of this writing (see [LMS
Toolkit#UseCases](https://techdocs.ed-fi.org/display/EXCHANGE/Ed-Fi+LMS+Toolkit)),
it is assumed that there are 2 main elements that need to be joined from LMS
data back to SIS entities:

* Students
* Sections

Future elements may also need to be joined, but do not fall into the current
priority use cases. In considering how this joining should occur, we rely on the
current Ed-Fi community scope of the Canvas, Schoology and Google Classroom LMS
systems.

In this research we consider several factors:

* The Ed-Fi data model itself and what we know of SIS vendor usage of it
* What LMS systems can store/provide, particularly as evidenced via their
  current APIs (i.e., what data can an LMS system give?)
* What data elements are typical of major rostering systems (i.e., what data
  would we expect the LMS to get?)

## Joining Students

Joining students is the more straightforward case but not without complexity. We
recommend that the local district SIS ID be used with joining LMS data, as this
ID tends to be the one used across LEA information systems.

### Ed-Fi

In Ed-Fi, the main identifier for Student is StudentUniqueID. For LEAs, the
standard practice and recommendation is to set this to the local district SIS
ID. Ed-Fi can also hold an array of StudentIdentificationCodes
on StudentEducationOrganizationAssociation; this is generally used in an LEA to
hold data such as the student state identifier and possibly IDs for that
individual in other systems.

Canvas and Schoology both have a place for the student SIS ID, but Google does
not have a field which requires those semantics. Therefore we discuss these
cases separately.

### Canvas and Schoology

#### Recommended / Canonical

Of the current LMS systems Canvas and Schoology contain a place to add the local
district SIS ID:

* Canvas: sis\_user\_id
  (optional) -  [https://canvas.instructure.com/doc/api/users.html#User](https://canvas.instructure.com/doc/api/users.html#User)
* Schoology: school\_uid (required)
  - [https://developers.schoology.com/api-documentation/rest-api-v1/user](https://developers.schoology.com/api-documentation/rest-api-v1/user)

The simplest case is that the local district ID is added to these locations, and
that this element is matched to Ed-Fi Student.StudentUniqueID, which is
recommended to be the local student district ID.

#### Possible but Non-recommended

It is possible that multiple student IDs exist and the school district could
have added other IDs to the Canvas and Schoology fields above. In this case, the
joining will need to be accomplished through another matching algorithm. 

Ed-Fi can store an array of identifiers in the StudentIdentificationCode array
on StudentEducationOrganizationAssociation. Ed-Fi also has fields such as
ElectronicEmail that are expected to be unique. These can be matched to similar
fields on Canvas or Schoology.

This is not a recommended pattern and has many drawbacks, the main one being the
highly customized nature of the join. It should also not be necessary given the
semantics of the Canvas and Schoology fields listed above.

### Google Classroom

Google Classroom has no field clearly designated to receive the student ID.
Accordingly, there are 2 options. 

* **Recommended/canonical**: the Google Student.UserId is rostered to be the
  local district SIS ID. This may be common practice, but we are unsure at this
  time.
* **Possible but Non-recommended**: in some cases Student.UserId is set to the
  Google ID (an email address). In this case, the join will have to be
  accomplished by joining this Google ID to one of these sources:
  * An identifier from the Ed-Fi StudentIdentificationCode array
    (see [https://schema.ed-fi.org/datahandbook-v320/index.html#/StudentIdentificationCode532](https://schema.ed-fi.org/datahandbook-v320/index.html#/StudentIdentificationCode532))
    on StudentEducationOrganizationAssociation.
  * An ElecronicMailAddress on ElectronicMail
    on StudentEducationOrganizationAssociation

## Joining Sections

The case of joining sections is more complex. as the Ed-Fi identity is more
complex and the LMS systems have taken different approaches.

### Ed-Fi Section Identity

In Ed-Fi, the main section key is a composite natural key.

For API transactions, there is also a REST UUID assigned by the API host to all
API resources, but Ed-Fi does not recommend this be propagated in the ecosystem,
given the risk of further confusing section identity. The REST ID however is
frequently stored and used by clients in order to update data sent to an Ed-Fi
API.

The Ed-Fi section key looks like this:

|         |                |             |                   |                 |
| ------- | -------------- | ----------- | ----------------- | --------------- |
| Entity  | Reference      | Reference   | Reference         | Field           |
| Section | CourseOffering | \-          | \-                | LocalCourseCode |
| School  | \-             | SchoolId\*  |
| Session | \-             | SessionName |
| \-      | SchoolYear     |
| School  | SchoolId\*     |
| \-      | \-             | \-          | SectionIdentifier |

_\*SchoolId is unified - meaning that the SchoolID from CourseOffering.School
and  Course.CourseOffering.Session.School must be identical._

This is a complex key, and trying to join all of these fields reliably with
their counterparts in an LMS system would be a daunting task, particularly as
the LMS generally has a much "shallower" version of the SIS core roster data.

Potentially problematic are these fields:

*   LocalCourseCode: it is commonplace to have tiered sets of course codes; for
    example local codes that map to state codes (e.g., to track progress against
    state and local graduation requirements)). However as is evident in the
    "Rostering" section below, the LMS system is shallower, and has at most 1
    course code (if any). This is _probably_ a match for LocalCourseCode, but
    not necessarily.
*   SessionName: again, these are "shallow" in LMS systems, sometimes optional.
    Plus, joining on a string ("name") is often error-prone.
*   SchoolId: the school reference on CourseOffering matches what is seen in LMS
    rostering, but there is some risk that schoolId will come from different
    systems (e.g. a local vs a state vs the federal NCES ID) 

While it is theoretically possible to match the Ed-Fi Section key to a LMS
section via a full match on all Ed-Fi fields, such a match seems likely to have
problems in the field given the diversity of possible options. 

#### How unique is Section.SectionIdentifier?

It seemed reasonable to expect that Section.SectionIdentifier might be unique,
so we reached out to major SIS systems to ask how unique this value was (we
assumed only current school year cases; no longitudinal cases explored). For
those systems that responded:

* For 2 systems, SectionIdentifier was unique within the LEA context
* For one SIS, it was not: for that system, SectionIdentifier was unique within
  the context of a LocalCourseCode

### Potential Canonical Mappings To LMS Systems

#### Canvas

For Canvas, the strategy for joining back to SIS data seems to be via
**Course.sis\_course\_id** (optional) defined as "the SIS identifier for the
course"
- [https://canvas.instructure.com/doc/api/courses.html](https://canvas.instructure.com/doc/api/courses.html)

There is also a **Course.CourseCode** (required?), which seems to be parallel to
the Ed-Fi **Course.CourseCode** or **CourseOffering.LocalCourseCode**. This
entity possibly allows "external" identity for Course to be seen
as **Course.sis\_course\_id + Course,CourseCode**; however, it seems more likely
that the assumption is that **Course.sis\_course\_id** is unique within the
Canvas instance.

#### Schoology

For Schoology, the strategy for joining seems to be via the
**CourseSection.section\_school\_code** and **CourseSection.section\_code** : 1
of these must be present
-  [https://developers.schoology.com/api-documentation/rest-api-v1/course-section](https://developers.schoology.com/api-documentation/rest-api-v1/course-section) These
are defined as:

* **section\_school\_code** -  "The section school code must be unique across
  the school "
* **section\_code **\- "The section code must be unique across the course and
  grading period (e.g. "Spring 2010" can only have one "10b" for course
  "ENG101")."

Looking at the Schoology data model, it is unclear what other strategies would
be possible for joining back to a SIS section.

#### Classroom

As the id for a Course is assigned by Classroom, the only option seems to be a
CourseAlias -
see [https://developers.google.com/classroom/reference/rest/v1/courses.aliases#CourseAlias](https://developers.google.com/classroom/reference/rest/v1/courses.aliases#CourseAlias) This
feature seems designed for this purpose of handling local organization
identifiers.

An alias is a string of the format: \["d"|"p"\]:\[string\] that must be trimmed
to obtain a SIS identifier.

### Provisional Conclusions for Joining Sections

When we factor in what is available in the LMS via the LMS APIs (see sections
below), we come to this provisional conclusion:

1. In most cases – and as the "canonical" method – the join to the LMS section
   can and should be driven off of matching Ed-Fi Section.SectionIdentifer to a
   corresponding LMS section ID or code, stored in the locations marked above
    * We should generally encourage SIS systems to move towards a Ed-Fi
      Section.SectionIdentifer that is unique within an LEA context (there seems
      to be no reason to not do this)
2. In some cases, we should assume that additional logic is necessary to join
   the Ed-Fi and LMS section
    * In some of those cases, that logic may use the additional information on
      course codes to join the LMS section to an Ed-Fi section using Ed-Fi
      Section.SectionIdentifer and Ed-Fi Section.LocalCourseCode
    * In some cases, the additional logic will be necessary to account for
      situations where SectionIdentifers are not in the "canonical" location,
      have additional formatting applied, or other non-standard local mappings
      have occurred.
3. When Ed-Fi collects the data, we should attempt (via ETL or API) to capture
   the Section.SectionIdentifer and the Section.LocalCourseCode

## Rostering Review

We also reviewed rostering systems, as these also define 'standardized" entities
and identifiers for students, sections and related core entities.

### Clever

[https://dev.clever.com/docs/data-model#schema](https://dev.clever.com/docs/data-model#schema)

Clever uses an internal GUID system for assigning the main identifier for
entities. For joining data back to other systems, Clever seems to take the
strategy of providing a place for the SIS ID via a required field **sis\_id**
for the "primary entities" to join (**User**, **School** **Section**), but not
for all entities (**Term** and **Course**, though Course has some field that
might join back to the SIS). 

| Clever Entity         | Ed-Fi Entity | Joinable Identifier(s)                                                                                                            |
| --------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| User (role="student") | Student      | **sis\_id**                                                                                                                       |
| School                | School       | **sis\_id**                                                                                                                       |
| Course                | Course       | **name** and a **number** - only guaranteed to have 1 of these                                                                    |
| Section               | Section      | **sis\_id**<br><br>optional reference to **Course**<br><br>optional reference to **Term**<br><br>required reference to **School** |
| Term                  | Session      | **name** (optional)                                                                                                               |

### OneRoster

[https://www.imsglobal.org/oneroster-v11-final-specification](https://www.imsglobal.org/oneroster-v11-final-specification)

OneRoster seems to use a local "surrogate" ID system based on GUIDs. These IDs
are assigned by the writing system, and they function as the main identifiers
for entities. 

> _SourcedId - all Objects MUST be identified by a Source Identifier. This is a
> GUID[\[1\]](https://www.imsglobal.org/oneroster-v11-final-specification#_ftn1) System
> ID for an object. This is the GUID that SYSTEMS will refer to when making API
> calls, or when needing to identify an object. It is RECOMMENDED that systems
> are able to map whichever local ids (e.g. database key fields) they use to
> SourcedId. The sourcedId of an object is considered an addressable property of
> an entity and as such will not be treated as Personally Identifiable
> Information (PII) by certified products._

From: [https://www.imsglobal.org/oneroster-v11-final-specification#\_Toc480452007](https://www.imsglobal.org/oneroster-v11-final-specification#_Toc480452007)

There are also a few spots in the data model where a local SIS ID could be
captured, but these are optional and often weakly semantic, unlike the Clever
connections back to SIS IDs.

A student enrollment requires a **User**, **Org** (type="school")  and
**Class**, but also has its own **sourcedId**. 

It is also universally possible to add customized metadata via the **metadata**
element which hangs off of all entities.

| OneRoster Entity      | Ed-Fi Entity | Joinable Identifier(s)                                                                                                                                                                  |
| --------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| User (type="student") | Student      | **sourcedId**<br><br>**username**<br><br>**identifier** (optional) - defined as "human readable ID, such as student id"<br><br>optional array of **userIds** (fields: type, identifier) |
| Org (type="school")   | School       | **sourcedId**<br><br>**identifier** (optional) - defined as "human readable identifier for this organization" but the examples make this look like a SIS ID                             |
| Course                | Course       | **sourcedId**<br><br>**courseCode** (optional)                                                                                                                                          |
| Class                 | Section      | **sourcedId**<br><br>**classCode** (optional)<br><br>required reference to **School**<br><br>required reference to **Course**                                                           |
| AcademicSession       | Session      | **sourcedId**<br><br>**title**                                                                                                                                                          |

### Microsoft School Data Sync

[https://docs.microsoft.com/en-us/schooldatasync/school-data-sync-format-csv-files-for-sds](https://docs.microsoft.com/en-us/schooldatasync/school-data-sync-format-csv-files-for-sds)

It is unclear that School Data Sync is used to roster "LMS systems" beyond those
provided by Microsoft, but its model is provided below as an influential
example. It's approach seems similar to Clever in its reliance on SIS
identifiers. In its examples, the optional identifying fields (see below) that
also appear on the entities often mirror the **SIS ID** value.

From the way SDS handles enrollments, it is also clear that the
**Section** **SIS ID** is assumed to be unique across a district (the section
enrollment is the SIS ID for the Student and Section)

| SDS Entity                                     | Ed-Fi Entity | Joinable Identifier(s)                                                                                                |
| ---------------------------------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------- |
| Student                                        | Student      | **SIS ID**<br><br>**Student Number** (optional)<br><br>**State ID** (optional)                                        |
| School                                         | School       | **SIS ID**<br><br>**School Number** (optional)<br><br>**State ID** (optional)                                         |
| Section                                        | Section      | **SIS ID**<br><br>**Section Number** (optional)<br><br>**Term SIS ID** (optional)<br><br>**Course Number** (optional) |
| Section.Term\* fields (denormalized structure) | Session      | **Term SIS ID**                                                                                                       |
