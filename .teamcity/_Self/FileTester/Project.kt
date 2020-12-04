// SPDX-License-Identifier: Apache-2.0
// Licensed to the Ed-Fi Alliance under one or more agreements.
// The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
// See the LICENSE and NOTICES files in the project root for more information.

package fileTester

import jetbrains.buildServer.configs.kotlin.v2019_2.*

object FileTesterProject : Project({
    RelativeId("FileTester")
    name = "File Tester"
    description = "Python scripts for validating the output from an extractor"

    buildType(fileTester.buildTypes.TestPullRequest)
    buildType(fileTester.buildTypes.TestBranch)

    params{
        param("project.directory", "./utils/file-tester");
        param("vcs.checkout.rules","""
            +:.teamcity => .teamcity
            +:%project.directory% => %project.directory%
            +:eng => eng
            +:src/file-utils => src/file-utils
        """.trimIndent())
    }
})
