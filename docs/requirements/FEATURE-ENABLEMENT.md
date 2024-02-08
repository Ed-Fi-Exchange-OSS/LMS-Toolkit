# Feature Enablement

## User Story

As a data analyst, I want to configure which resources are extracted from an
LMS, so that I can minimize network resources and download times.

## Resource Groups

Due to foreign key relationships, it does not make sense to configure an
extractor on a per-resource basis. Instead we can think about _resource groups_.

| Resource Group | Resources | Notes |
| --- | --- | --- |
| Resource Group | Resources | Notes |
| --- | --- | --- |
| ​Core | Users<br><br>Sections​<br><br>Section Associations | Cannot be disabled |
| Activities | Section Activities<br><br>System Activities |     |
| Attendance | Attendance Events |     |
| Assignments | Assignments<br><br>Assignment Submissions |     |
| Grades | Grade | Will not be available in 1.0 release since we don't have Grades capability yet. |

## Options

> [!INFO] Decision \
> After the daily standup on 5/3/2021, Eric / Brad / Gabrielle / Stephen agreed
> on using Option 2 below.

### 1. Configure via CLI Switches

With individual flags like this, the configuration help will be easy to read
(each feature listed separately), but it doesn't make sense to have anything
"on" by default.

Only download users, sections, and section associations:

```shell
poetry run python edfi-schoology-extractor --client-key "..." --client-secret "..."
```

Turn on all features:

```shell
poetry run python edfi-schoology-extractor --client-key "..." --client-secret "..." --feature-activities --feature-attendance --feature-assignments --feature-grades
```

Only turn on assignments:

```shell
poetry run python edfi-schoology-extractor --client-key "..." --client-secret "..." --feature-assignments
```

.env file:

```none
SCHOOLOGY_KEY=...
SCHOOLOGY_SECRET=...
FEATURE_ACTIVITIES=true
FEATURE_ATTENDANCE=true
FEATURE_ASSIGNMENTS=true
# Following line is not actually necessary - off by default
FEATURE_GRADES=false
```

### 2. Configure via Single Options Argument, No Default

> [!NOTE] This option again throws out the idea of anything being "on" by
> default

Only download users, sections, and section associations:

```shell
poetry run python edfi-schoology-extractor --client-key "..." --client-secret "..."
``````

Turn on all features:

```shell
poetry run python edfi-schoology-extractor --client-key "..." --client-secret "..." --feature activities, attendance, assignments, grades
```

Alternate:

```shell
poetry run python edfi-schoology-extractor --client-key "..." --client-secret "..." --feature activities --feature attendance --feature assignments --feature grades
```

Only turn on assignments:

```shell
poetry run python edfi-schoology-extractor --client-key "..." --client-secret "..." --feature assignments
```

.env file:

```none
SCHOOLOGY_KEY=...
SCHOOLOGY_SECRET=...
# Enable all but Grades
FEATURE=[ACTIVITIES, ATTENDANCE, ASSIGNMENTS]
```

### 3. Configure via Single Options Argument, With Default

In this case, when no options are provided we can have a default that leaves one
or more switches on.

Download users, sections, and section associations (core) and Assignments and
Grades (on by default):

```shell
poetry run python edfi-schoology-extractor --client-key "..." --client-secret "..."
```

Turn on all features:

```shell
poetry run python edfi-schoology-extractor --client-key "..." --client-secret "..." --feature activities, attendance, assignments, grades
```

Alternate:

```shell
poetry run python edfi-schoology-extractor --client-key "..." --client-secret "..." --feature activities --feature attendance --feature assignments --feature grades
```

Turn on Activities and Attendance without Assignments and Grades:

```shell
poetry run python edfi-schoology-extractor --client-key "..." --client-secret "..." --feature attendance, activities
```

.env file:

```none
SCHOOLOGY_KEY=...
SCHOOLOGY_SECRET=...
# Enable all but Grades
FEATURE=[ACTIVITIES, ATTENDANCE, ASSIGNMENTS]
# If `FEATURE` is omitted then downloads Assignments and Grades by default
```
