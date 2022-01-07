# Building and Using the Extension

## Build NuGet Package

After successful initdev following normal instructions:

```powershell
nuget pack *.nuspec -properties configuration=release -version 5.2.0
nuget push *.5.2.0.nupkg -source https://pkgs.dev.azure.com/ed-fi-alliance/Ed-Fi-Alliance-OSS/_packaging/EdFi/nuget/v3/index.json -apikey az
```

## Install Into Source Code

In `Ed-Fi-ODS-Implementation/logistics/scripts`, edit file `configuration.package.json`, 
adding the following at the end:

```json
    "lmsx": {
      "PackageName": "EdFi.Ods.Extensions.LMSX.1.0.0",
      "PackageVersion": "5.2.1",
      "PackageSource": "https://pkgs.dev.azure.com/ed-fi-alliance/Ed-Fi-Alliance-OSS/_packaging/EdFi/nuget/v3/index.json"
    }
```

In `Ed-Fi-ODS-Implementation/Plugins`, copy `tpdm.ps1` to `lmsx.ps1` and adjust contents as necessary.

