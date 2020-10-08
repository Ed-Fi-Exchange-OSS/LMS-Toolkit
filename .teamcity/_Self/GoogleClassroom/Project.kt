// SPDX-License-Identifier: Apache-2.0
// Licensed to the Ed-Fi Alliance under one or more agreements.
// The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
// See the LICENSE and NOTICES files in the project root for more information.

package googleClassroom

import jetbrains.buildServer.configs.kotlin.v2019_2.*

object GoogleClassroomProject : Project({
    RelativeId("GoogleClassroom")
    name = "Google Classroom Utilities"
    description = "Python scripts for interacting with Google Classroom"

    buildType(googleClassroom.buildTypes.TestPullRequest)
    buildType(googleClassroom.buildTypes.TestBranch)

    params{
        param("project.directory", "google-classroom-extractor");
        param("vcs.checkout.rules","""
            +:.teamcity => .teamcity
            +:%project.directory% => %project.directory%
            +:eng => eng
        """.trimIndent())
    }
})
