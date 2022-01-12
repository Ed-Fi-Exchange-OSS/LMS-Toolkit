# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

#requires -modules "path-resolver"

Import-Module (Get-RepositoryResolvedPath 'logistics\scripts\modules\packaging\nuget-helper.psm1')
Import-Module (Get-RepositoryResolvedPath "logistics\scripts\modules\tools\ToolsHelper.psm1")

$configuration = @{
    PackageName = "EdFi.Ods.Extensions.LMSX.1.0.0"
    ## Uncomment the appropriate line below
    # For ODS/API Suite 3, version 5.2:
    #PackageVersion = "5.2.1"
    # For ODS/API Suite 3, version 5.3:
    PackageVersion = "5.3.2"
    PackageSource = "https://pkgs.dev.azure.com/ed-fi-alliance/Ed-Fi-Alliance-OSS/_packaging/EdFi/nuget/v3/index.json"
}

$pluginPaths = @()

$parameters = @{
    packageName     = $configuration.packageName
    packageVersion  = $configuration.packageVersion
    packageSource   = $configuration.packageSource
    outputDirectory = "$PSScriptRoot"
    toolsPath       = (Get-ToolsPath)
}
$pluginPaths += Get-NuGetPackage @parameters

return $pluginPaths
