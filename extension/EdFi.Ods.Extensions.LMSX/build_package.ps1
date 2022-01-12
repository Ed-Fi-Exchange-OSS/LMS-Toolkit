# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

<#
    .SYNOPSIS
        Builds a release version of the extension, creates NuGet package, and
        publishes to Azure Artifacts.

    .DESCRIPTION
        In order for this to work, this directory must have been copied into the
        Ed-Fi-ODS-Implementation/Application directory, and initdev must have
        already been run on the entire project in order to generate both SQL and
        C# code for the extension.

        The Extension Version should be the unique version number for the
        extension itself. This version shows up in the DLL. The major and minor
        numbers for the Package Version should match the targeted ODS/API
        major.minor version plus a build counter (for example,
        $PackageVersion=5.2.1).

        The final command, nuget push, will only work if you have a login to the
        Ed-Fi Azure Artifacts subscription with appropriate permissions.
#>
param(
    # Version of the extension itself.
    [string]
    [Parameter(Mandatory=$True)]
    $ExtensionVersion,

    # Version of the package, where major.minor corresponds to the targeted
    # ODS/API release version.
    [string]
    [Parameter(Mandatory=$True)]
    $PackageVersion
)

$ErrorActionPreference = 'Stop'


dotnet build --configuration release -p:Version=$ExtensionVersion `
    -p:InformationalVersion=$ExtensionVersion -p:FileVersion=$ExtensionVersion

nuget pack .\EdFi.Ods.Extensions.LMSX.nuspec -properties configuration=release `
    -properties id=EdFi.Ods.Extensions.LMSX.$ExtensionVersion -version $PackageVersion `
    -NoPackageAnalysis

$url = 'https://pkgs.dev.azure.com/ed-fi-alliance/Ed-Fi-Alliance-OSS/_packaging/EdFi/nuget/v3/index.json'
nuget push EdFi.Ods.Extensions.LMSX.$ExtensionVersion.$PackageVersion.nupkg -apikey az -source $url
