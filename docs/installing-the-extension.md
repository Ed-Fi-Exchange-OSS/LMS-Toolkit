# Installing the Ed-Fi-LMS Extension

## Introduction

The `Ed-Fi-LMS` extension to Ed-Fi Data Standard can be loaded into an Ed-Fi
ODS/API Suite 3, version 5.2 code base for deployment. In theory it should work
with older data standards, but it is only being tested with Ed-Fi Data Standard
version 3.3-a, which is implemented in the API version 5.2.

When do deployed, `Assignments` and `AssignmentSubmissions` can be uploaded into
an ODS database through the Ed-Fi API. Alternately, one can use the [LMS
Harmonizer](../src/lms-harmonizer) to copy LMS Toolkit data uploaded with [LMS
Data Store Loader](../src/lms-ds-loader) directly into the `edfilms.Assignment`
and associated extension tables.

For more information about the extension data model, please see [LMS
Extension](https://techdocs.ed-fi.org/display/EFTD/LMS+Extension) in Tech Docs.

## Adding the Extension to the ODS / API

These instructions assume you have already [gotten
started](https://techdocs.ed-fi.org/display/ODSAPIS3V520/Getting+Started) with
the Ed-Fi ODS/API Suite 3, Version 5.2*, and they assume that the LMS Toolkit
repository exists in the same parent directory as `Ed-Fi-ODS` and
`Ed-Fi-ODS-Implementation`. (* be sure to use the code from the v5.2 release,
not from the `main` branch: run `git checkout v5.2` in both `Ed-Fi-ODS` and
`Ed-Fi-ODS-Implementation`).

1. Copy the entire
   [EdFi.Ods.Extensions.EdFiLMS](../extension/EdFi.Ods.Extensions.EdFiLMS) directory
   into your `Ed-Fi-ODS-Implementation/Application` directory.
1. Add this project as a reference in the API project:
   1. Open the solution in Visual Studio
   1. Add the extension project into the "Ed-Fi Extensions" folder in the solution
   1. Add the new project as a reference in the WebAPI project.
1. Re-run `initdev`.
1. To test, run the solution by starting the API in the default Sandbox mode,
   and starting the Sandbox Admin and Swagger UI.
1. In Swagger UI, confirm that the new descriptors and  resources are available.

## Bulk-Loading Default Descriptors

1. Acquire a key and secret for bulk upload:
   1. If following the steps above:
      1. Open the `appsettings.development.json` file in Visual Studio, under
         the SandboxAdmin project
      1. Use the key and secret found there for either the minimal or populated template
   1. If using something other than Sandbox mode, then use Admin App to create a
      new key and secret using the Sandbox or Descriptor Bootstrap claimset.
1. Customize [LoadDescriptors.ps1](../extension/LoadDescriptors.ps1) by pasting your
   key and secret into it. * _caution: do not commit these changes to source control_
1. Review other parameters in that script and adjust as necessary.
1. Compile the client side bulk loader in the `Ed-Fi-ODS` directory. Either:
   1. Open `Ed-Fi-ODS\Utilities\DataLoading\LoadTools.sln` and compile with Visual Studio, or
   1. At a command prompt, run:
      ```powershell
       > cd Ed-Fi-ODS\Utilities\DataLoading
       > dotnet restore LoadTools.sln
       > dotnet build LoadTools.sln
1. At a command prompt, run the bulk load script:
   ```powershell
   > cd LMS-Toolkit\extension
   > ./LoadDescriptor.sps1
   ```
