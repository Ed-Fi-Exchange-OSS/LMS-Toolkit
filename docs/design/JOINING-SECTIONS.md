# LMS - Joining Sections

> [!INFO] Upon review, Option #2 below was seen as the strongest direction
> forward and is the initial one to be pursued.

## Problem

The Alliance Learning Management Systems (LMS) data integration efforts need a
strategy for joining LMS sections back to Student Information System (SIS)
sections.  Unfortunately, this join is not straightforward, due to several
factors:

1. the differences of purpose between SIS and LMS systems, which leads to
   different data structures and data management processes
2.  the weak state of rostering solution implementations in many areas of K12
    generally (i.e., lack of standardization and normative guidelines for how
    sections should be identified across K12)
3. the composite nature of the Ed-Fi section key (see [LMS - Joining Entities
   across
   Systems#Ed-FiSectionIdentity](/display/EXCHANGE/LMS+-+Joining+Entities+across+Systems#LMSJoiningEntitiesacrossSystems-Ed-FiSectionIdentity))


| Entity  | Reference      | Reference   | Reference         | Field           |
| ------- | -------------- | ----------- | ----------------- | --------------- |
| Entity  | Reference      | Reference   | Reference         | Field           |
| Section | CourseOffering | \-          | \-                | LocalCourseCode |
| School  | \-             | SchoolId\*  |
| Session | \-             | SessionName |
| \-      | SchoolYear     |
| School  | SchoolId\*     |
| \-      | \-             | \-          | SectionIdentifier |

_The Ed-Fi Section key_

## Use Cases

The solution to his problem must also consider two use cases:

1. The joining of LMS and SIS sections via the [LMS
   Harmonizer](./LMS-HARMONIZER.md) (i.e., the Load/Transform part of the ETL
   process from the LMS Toolkit - see [LMS Toolkit Design](./README.md)
2. A future [LMS API](./LMS-API.md), to support direct data integration
   scenarios from LMS to SIS

## Scope

The LMS Harmonizer – as an ETL application – is likely capable of solving the 3
three problems at top, by allowing for some amount of "local intelligence"
and/or configuration to be inserted into the process. That does not come without
a cost (i.e., it costs the localization effort), but it does provide a workable
solution.

However, the same is not true of the LMS API. An API-based solution can likely
solve problem #1, but problems #2 and #3 would remain:

* there is simply not a clear line of sight to agreement on section identity
  across current rostering specifications - on this point, see: [LMS - Joining
  Entities across
  Systems#RosteringReview](/display/EXCHANGE/LMS+-+Joining+Entities+across+Systems#LMSJoiningEntitiesacrossSystems-RosteringReview)
* given #2, it is unlikely that many LMS systems will have the data to meet the
  demands of the Ed-Fi section key - on this point, see [LMS - Joining Entities
  across
  Systems#JoiningSections](/display/EXCHANGE/LMS+-+Joining+Entities+across+Systems#LMSJoiningEntitiesacrossSystems-JoiningSections)

It is of course possible to integrate "configurability" into the API interfaces
provided by LMS vendors (i.e. the vendor allows "localization" of the API
interface in the same way the Ed-Fi API allows), but the purpose of rostering is
to avoid such configurability generally, so would be seen potentially as
self-defeating, and such configurability is unlikely to be able to solve some
issues, such as matching course codes from SIS to LMS (necessary to solve
problem #3)

## Technical 

The initial implementation of hosting the "joinable" LMS data in the Ed-Fi ODS
is via a extension in the "edfilms" namespace - this detail is needed to
understand the options below.

### Option 1

* Join on edfilms.Assignment.SectionIdentifier to
   edfi.Section.SectionIdentifier

| PROs                | CONs                                                         |
| ------------------- | ------------------------------------------------------------ |
| Simple to implement | Will force some SIS systems to alter their Ed-Fi section key |
|                     | Solution not usable by some agencies, out-of-the-box         |

### Option 2

* Join on edfilms.Assignment.SectionIdentifier
  to edfi.Section.SectionIdentifier 
* Plus add an optional reference to Section on edfilms.Assignment that the
  harmonizer would meet

| PROs                                                                | CONs                                                                                                                 |
| ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Allows an API client to easily know that an element has been joined | Creates a situation in which an API resource can be inconsistent with itself (or can we unify on SectionIdentifier?) |
| Allows use of current Ed-Fi key, albeit in limited ways             | Potentially confusing to readers of the data: 2 Section keys                                                         |

### Option 3

* Add section "lookup" interface.

Interestingly, this was a characteristic of Ed-Fi 1.0 in its XML binding. It is
also similar to the strategy behind the ODS Identity API.

In this model. the ODS presents an interface that takes identifying attributes
for section and attempts to "lookup" the unique section.  Arguably, this is
already possible via the GET interface, but an independent API could offer more
powerful search options (the GET interface performs an "exact match" that ANDs
all the parameters).

| PROs                              | CONs                                                     |
| --------------------------------- | -------------------------------------------------------- |
| Supports use of Ed-Fi natural key | Feature does not exist, or does not exist in robust form |
|                                   | Forces clients to store the Ed-Fi natural key (5 fields) |
