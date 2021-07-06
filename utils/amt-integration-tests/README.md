# Analytics Middle Tier Integration Testing

## Goal

Install the Analytics Middle Tier (AMT) "Student Engagement" views and validate
that they are returning the expected data.

## Pre-requisites

* SQL Server 2017+, with `sqlcmd` available in the command path.
* Install
  [sqlpackage.exe](https://docs.microsoft.com/en-us/sql/tools/sqlpackage/sqlpackage?view=sql-server-ver15)

  ```PowerShell
  choco install -y sqlpackage
  ```

* Clone [Analytics Middle
  Tier](https://github.com/Ed-Fi-Alliance-OSS/Ed-Fi-Analytics-Middle-Tier) into
  the same parent directory as the LMS Toolkit or in a higher parent.

  ```PowerShell
  git clone https://github.com/Ed-Fi-Alliance-OSS/Ed-Fi-Analytics-Middle-Tier
  ```

* .NET Core 3.1 SDK

## How It Works

1. Creates a new database called `test_analytics_middle_tier_engage` on the localhost,
   using integrated security, from the `EdFi_Ods_3.2.dacpac` from the Analytics
   Middle Tier.
2. Install the Analytics Middle Tier `core` and `engage` collections.
3. Loads sample data.
4. Performs a number of tests to confirm that the AMT components have been
   installed correctly and that they function as expected.
5. Teardown the sample database.

## Runtime Options

Note: if no options are provided, then the tests will use integrated security to
connect to SQL Server on the default port on localhost, and will use database
name `test_analytics_middle_tier_engage`.

| Argument | Default | Purpose |
| -- | -- | -- |
| --skip-teardown | false | Skip the teardown of the database. Potentially useful for debugging |
| --server | localhost | Database server name or IP address |
| --port | 1433 | Database server port number |
| --dbname | test_analytics_middle_tier_engage | Name of the test database  |
| --useintegratedsecurity | true | Use Integrated Security for the database connection |
| --username | (none) | Database username when not using integrated security |
| --password | (none) | Database user password, when not using integrated security |

## Future Considerations

* Downloading AMT via a package or release, instead of relying on a clone.
* Using a cross-platform tool for dacpac management, instead of sqlpackage.exe,
  so that this can be run on Linux.
