# Installing the Ed-Fi-LMS Extension

## Introduction

The `Ed-Fi-LMS` extension to Ed-Fi Data Standard can be loaded into an Ed-Fi
ODS/API Suite 3, version 5.2+ code base for deployment. In theory it should work
with older data standards, but it is only being tested with Ed-Fi Data Standard
version 3.3-a, which is implemented in the API version 5.2.

When deployed, `Assignments` and `AssignmentSubmissions` can be uploaded into
an ODS database through the Ed-Fi API. Alternately, one can use the [LMS
Harmonizer](../src/lms-harmonizer) to copy LMS Toolkit data uploaded with [LMS
Data Store Loader](../src/lms-ds-loader) directly into the `edfilms.Assignment`
and associated extension tables.

For more information about the extension data model, please see [LMS
Extension](https://techdocs.ed-fi.org/display/EFTD/LMS+Extension) in Tech Docs.

## Deployment Process

There are several methods for deploying the extension into an ODS/API instance:

1. Integrate the extension source code directly into the ODS/API. :exclamation:
   This is the method required to build a new release of the extension.
2. Integrate the binary release of the extension into source code as a dynamic plugin.
3. Integrate the binary release of the extension into an ODS/API instance
   running from binaries, as a dynamic plugin.

After deployment, you can confirm that the installation succeeded by accessing
Web API application's version endpoint (the root endpoint) and looking in the
list of supported data models, where you should see something like this:

```json
{
    "version": "...",
    ...,
    "dataModels": [
        {
            "name": "Ed-Fi",
            ...
        },
        {
            "name": "LMSX",
            "version": "1.0.0"
        }
    ],
    "urls": ...
}
```

:exclamation: All of these instructions require running in PowerShell on
Windows. PowerShell Core on Linux is not yet supported. It should be technically
feasible to deploy from a Linux machine, but we have not tested this or
documented the extra commands that would be required to bypass PowerShell.

### Direct Source Code Integration into ODS/API

These instructions assume you have already [gotten
started](https://techdocs.ed-fi.org/display/ODSAPIS3V520/Getting+Started) with
the Ed-Fi ODS/API Suite 3, Version 5.2*, and they assume that the LMS Toolkit
repository exists in the same parent directory as `Ed-Fi-ODS` and
`Ed-Fi-ODS-Implementation`. (* be sure to use the code from the v5.2 release,
not from the `main` branch: run `git checkout v5.2` in both `Ed-Fi-ODS` and
`Ed-Fi-ODS-Implementation`).

1. Copy the entire
   [EdFi.Ods.Extensions.LMSX](../extension/EdFi.Ods.Extensions.LMSX) directory
   into your `Ed-Fi-ODS-Implementation/Application` directory.
1. Add this project as a reference in the API project:
   1. Through Visual Studio:
      1. Open the solution in Visual Studio
      1. Add the extension project into the "Ed-Fi Extensions" folder in the solution
      1. Add the new project as a reference in the WebAPI project.
   1. Or through the command line:

      ```powershell
      > dotnet sln .\Ed-Fi-Ods.sln add -s "Ed-Fi Extensions" .\EdFi.Ods.Extensions.LMSX\
      > dotnet add .\EdFi.Ods.WebApi\ reference .\EdFi.Ods.Extensions.LMSX\
      ```

1. Re-run `initdev` in PowerShell.
1. To test, run the solution by starting the API in the default Sandbox mode,
   and starting the Sandbox Admin and Swagger UI.
1. In Swagger UI, confirm that the new descriptors and resources are available.

### Dynamic Plugin Into Source Code

1. Copy [lmsx.ps1](../extension/lmsx.ps1) to your
   `Ed-Fi-ODS-Implementation/Plugin` directory.
2. Open the copy of `lmsx.ps1` and uncomment the correct "PackageVersion" entry
   for your target ODS/API version.
3. In your `Ed-Fi-ODS-Implementation/Application/EdFi.Ods.WebApi` directory, run
   the following commands (:exclamation: if you already have any dynamic
   extension, then increment the script number in the second command
   accordingly):

   ```powershell
   dotnet user-secrets set "Plugin:Folder" "../../Plugin"
   dotnet user-secrets set "Plugin:Scripts:0" "lmsx"
   ```

4. Run `initdev`:

   ```powershell
   ./Initialize-PowershellForDevelopment.ps1
    Initdev
    ```

When you run the Web API, look at the base endpoint, which has metadata about
your installation. Confirm that LMSX is listed in the data models. If not seen,
please review the steps above. Particularly check that you selected the correct
"PackageVersion" in step 2, matching the version of code that you are building
(5.2.x or 5.3.x).

### Dynamic Plugin Into Runtime

1. Download the correct version of the `EdFi.Suite3.RestApi.Databases` NuGet
   package from [Ed-Fi on Azure
   Artifacts](https://dev.azure.com/ed-fi-alliance/Ed-Fi-Alliance-OSS/_packaging?_a=package&feed=EdFi%40Release&package=EdFi.Suite3.RestApi.Databases&protocolType=NuGet&view=versions).
   If you are targeting ODS/API version 5.2, then download version 5.2.14406. If
   targeting version 5.3, then download 5.3.1146.
   * If you have `nuget.exe` you can download and extract files with the
     following command. This will create directory
     `EdFi.Suite3.RestApi.Databases.5.2.14406` in the current working directory.
     See link above for other available versions, matching the ODS/API releases:

   ```bash
   nuget.exe install EdFi.Suite3.RestApi.Databases -version 5.2.14406 -source https://pkgs.dev.azure.com/ed-fi-alliance/Ed-Fi-Alliance-OSS/_packaging/EdFi%40Release/nuget/v3/index.json
   ```

   * If you don't have `nuget.exe`, just download from the link above and treat
     it as a zip file. Unzip to an appropriate location.
2. Locate the directory for your WebAPI website. Does it have a `Plugin`
   sub-directory? If not, create it. Copy the full exact path for use in the
   next step.
3. In the new `EdFi.Suite3.RestApi.Databases` directory, edit
   `configuration.json` and add "lmsx" to the `Plugin.Scripts` array, as shown
   below. Paste the `Plugin` directory path into the `Folder` entry below:

   ```json
   "Plugin": {
       "Folder": "d:/Ed-Fi/5.2/WebApi/Plugin",
       "Scripts": [ "lmsx" ]
   }
   ```

   :exclamation: If you do not use the WebAPI project's Plugin directory at this
   step, then the plugin will not load when you run the application at the final
   step below.

4. In that same file, adjust the database connection strings and database engine
   as appropriate for your installation. If you are not sure what they are, then
   look in the `appsettings.json` file in your WebAPI directory.
5. Run the database deployment process in PowerShell while in the
   `EdFi.Suite3.RestApi.Databases` directory:

   ```powershell
   Import-Module ./Deployment.psm1
   Initialize-DeploymentEnvironment
   ```

6. Open the `appsettings.json` file in your WebAPI directory, and add an "lmsx"
   entry under `Scripts`, just as done in step 3 above.
7. Restart the web site in IIS.

## Client Authorization

To access the LMSX resources, API Clients need to have the "LMS Vendor" or
"Ed-Fi Sandbox" claimset that is created by the installation process. The "SIS
Vendor" claimset, by default, is insufficient. To access the LMSX descriptors,
the client will instead need the "Ed-Fi Sandbox" or the "Bootstrap Descriptors
and EdOrgs" permission. See _Bulk-Loading Default Descriptors_ below for
additional notes on how to create an API client key and secret.

## Loading Descriptors

### Manually Loading Descriptors

Once the extension is loaded into the ODS/API, the descriptor endpoints are
available in the API and a user with authorization to create new descriptors can
utilize it directly. For examples, see
[extension-tests.http](../extension/extension-tests.http).

### Bulk-Loading Default Descriptors

This automated upload utilize the API Client Bulk Load utility from the
[Ed-Fi-ODS](https://github.com/Ed-Fi-Alliance-OSS/Ed-Fi-ODS) repository.

1. Acquire a key and secret for bulk upload:
   1. Using Sandbox Admin:
      1. Open the `appsettings.development.json` file in Visual Studio, under
         the SandboxAdmin project
      1. Use the key and secret found there for either the minimal or populated template
   1. Using Admin App: If using something other than Sandbox mode, then use Admin App to create a
      new key and secret using the Sandbox or Descriptor Bootstrap claimset.
   1. Direct database setup: see [How To: Configure
      Key/Secret](https://techdocs.ed-fi.org/pages/viewpage.action?pageId=95260307);
      the default uses claimset "SIS Vendor". Change this to "Ed-Fi Sandbox".
1. Customize [LoadDescriptors.ps1](../extension/LoadDescriptors.ps1) by pasting your
   key and secret into it. * _caution: do not commit these changes to source control_
1. Review other parameters in that script and adjust as necessary.
1. Compile the client side bulk loader in the `Ed-Fi-ODS` directory. Either:
   1. Open `Ed-Fi-ODS\Utilities\DataLoading\LoadTools.sln` and compile with Visual Studio, or
   1. At a command prompt, run:

      ```powershell
       cd Ed-Fi-ODS\Utilities\DataLoading
       dotnet restore LoadTools.sln
       dotnet build LoadTools.sln
      ```

1. At a command prompt, run the bulk load script:

   ```powershell
   cd LMS-Toolkit\extension
   ./LoadDescriptor.sps1
   ```

## Installing LMS Harmonizer Support

Pre-requisites:

1. You have successfully run `initdev` following the instructions above.
1. You have run the [LMS Data Store Loader](../src/lms-ds-loader) once
   against the desired ODS database, thus creating the LMS Toolkit tables.

There is a set of SQL files in
[EdFi.Ods.Extensions.LMSX\LMS-Harmonizer](../extension/EdFi.Ods.Extensions.LMSX/LMS-Harmonizer)
that need to be installed into the ODS. For now this is a manual install
process. The files are named in sequence order and should be installed into
the ODS database in that order. After that, you will be able to run the [LMS
Harmonizer](../src/lms-harmonizer) to move data from LMS Toolkit tables into
the Ed-Fi extension tables.
