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
