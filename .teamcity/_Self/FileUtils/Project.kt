// SPDX-License-Identifier: Apache-2.0
// Licensed to the Ed-Fi Alliance under one or more agreements.
// The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
// See the LICENSE and NOTICES files in the project root for more information.

package fileUtils

import jetbrains.buildServer.configs.kotlin.v2019_2.*

object FileUtilsProject : Project({
    RelativeId("FileUtils")
    name = "File Utilities"
    description = "Python scripts for interacting the LMS filesystem created by the extractors"

    buildType(fileUtils.buildTypes.TestPullRequest)
    buildType(fileUtils.buildTypes.TestBranch)

    params{
        param("project.directory", "./src/file-utils");
        param("vcs.checkout.rules","""
            +:.teamcity => .teamcity
            +:%project.directory% => %project.directory%
            +:eng => eng
        """.trimIndent())
    }
})
