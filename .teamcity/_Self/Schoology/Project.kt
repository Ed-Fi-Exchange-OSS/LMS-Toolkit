// SPDX-License-Identifier: Apache-2.0
// Licensed to the Ed-Fi Alliance under one or more agreements.
// The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
// See the LICENSE and NOTICES files in the project root for more information.

package schoology

import jetbrains.buildServer.configs.kotlin.v2019_2.*

object SchoologyProject : Project({
    id("EdFi_RandD_Exchange_Fizz_Schoology")
    name = "Schoology Utilities"
    description = "Python scripts for interacting with Schoology"

    buildType(schoology.buildTypes.TestPullRequest)
    buildType(schoology.buildTypes.TestBranch)

    params{
        param("project.directory", "./src/schoology-extractor");
        param("vcs.checkout.rules","""
            +:.teamcity => .teamcity
            +:%project.directory% => %project.directory%
            +:eng => eng
        """.trimIndent())
    }
})
