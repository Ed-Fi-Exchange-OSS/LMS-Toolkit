# Extension

## Deployment

See [installing-the-extension.md](../docs/installing-the-extension.md)

## Build

### Version Numbers and ODS/API Support

There are two version numbers for the extension: the _extension version_ (e.g.
`1.0.0`) and the _package version_ (e.g. `5.2.1`). The extension needs to be
compiled separately for each ODS/API version, and the package version's
major.minor number should match the targeted ODS/API version. The _patch_ number
on the package version is just a build counter.

In this situation we prefer to simply increment the patch / build counter rather
than use a pre-release versioning scheme. Thus the first build for ODS/API Suite
3 version 5.3, even if experimental, will be `5.3.1`. If that build has a
problem and you need to try again, it will be `5.3.2`. That is fine. In Azure
Artifacts, we will never label `5.3.1` as a release and eventually it will be
purged by retention rules.

1. Retrieve the `Ed-Fi-ODS` and `Ed-Fi-ODS-Implementation` repositories and
   checkout the desired tag or branch.
   * New to the Ed-Fi ODS/API build process? See [Tech
     Docs](https://techdocs.ed-fi.org) for information on getting started.
2. Copy this repository's `EdFi.Ods.Extensions.LMSX` folder into
   `Ed-Fi-ODS-Implementation/Application`.
3. Using PowerShell, add the project to the Ed-Fi-ODS solution file and as a
   reference in the WebAPI project.

     ```powershell
     cd  Ed-Fi-ODS-Implementation/Application
     dotnet sln add ./EdFi.Ods.Extensions.LMSX -s "Ed-Fi Extensions"
     cd EdFi.Ods.WebApi
     dotnet add reference ../EdFi.Ods.Extensions.LMSX/EdFi.Ods.Extensions.LMSX.csproj
     ```

4. Unlike with the end-user install instructions, "LMSX" _should not_ be listed
   in the Plugins in `appsettings.json`.
5. Run `initdev` in the usual way to build the entire solution. Watch for errors.
6. Build, package, and publish a NuGet package, substituting the appropriate version numbers:

   ```powershell
   cd EdFi.Ods.Extensions.LMSX
   ./build_package.ps1 -ExtensionVersion 1.0.1 -PackageVersion 5.2.1
   ```

## Notes on Use in Docker

SF: I have not been able to get the plugin working in Docker yet, though I was
probably very close. Rough notes on what I have done:

* Prep for database installation: in `configuration.json`, use the following
  * connection strings:

    ```json
    {
      "EdFi_Ods": "Host=localhost; Port=5402; Username=postgres; Database=EdFi_{0};",
      "EdFi_Admin": "Host=localhost; Port=5401; Username=postgres; Database=EdFi_Admin;",
      "EdFi_Security": "Host=localhost; Port=5401; Username=postgres; Database=EdFi_Security;",
      "EdFi_Master": "Host=localhost; Port=5401; Username=postgres; Database=postgres;"
    }
    ```

  * ApiSettings:
    * Mode: `SharedInstance`
    * Engine: `postgresql`
  * Plugin:
    * Folder: `./Plugin`
    * Scripts: `["lmsx"]
  * Copy the `lmsx.ps1` script into a `Plugin` directory _under_ the unzipped
    RestApi.Databases directory.
* Get the Docker repository
  * Run the shared-instance environment file `compose-shared-instance-env.yml`
* Run the database deployment.
* Create a local version of the appsettings file:
  * Grab the appsettings template from the running container:

    ```powershell
    docker cp ed-fi-ods-api:/app/appsettings.template.json .
    ```

  * Modify that appsettings file to add "lmsx" to the scripts list
  * Modify the docker compose yml file. Need to load the extension and the
    modified appsettings file into the container at runtime. UNder the
    `api: volumes: ` structure, add these two volumes:

    ```yml
     - C:/Temp/EdFi.Suite3.RestApi.Databases.5.2.14406/Plugin/EdFi.Ods.Extensions.LMSX.1.0.0.5.2.1:/app/Plugin/EdFi.Ods.Extensions.LMSX.1.0.0.5.2.1
    - c:/Temp/EdFi.Suite3.RestApi.Databases.5.2.14406/appsettings.template.json:/app/appsettings.template.json
    ```

* Stop and restart the Docker containers.
  * --> LMSX didn't work. Maybe because the DLL was not compiled for Linux?
    Didn't find a clear error message anywhere.
