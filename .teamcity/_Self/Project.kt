// SPDX-License-Identifier: Apache-2.0
// Licensed to the Ed-Fi Alliance under one or more agreements.
// The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
// See the LICENSE and NOTICES files in the project root for more information.

package _self

import jetbrains.buildServer.configs.kotlin.v2019_2.*

object FizzProject : Project({
    name = "Fizz"
    description = "Project Fizz Utilities for Learning Management System Data"

    params {
        param("teamcity.ui.settings.readOnly","true")
        param("build.feature.freeDiskSpace", "2gb")
        param("git.branch.default", "main")
        param("git.branch.specification", """
            refs/heads/(*)
            refs/(pull/*)/head
        """.trimIndent())
    }

    subProject(schoology.SchoologyProject)

    template(_self.templates.TestTemplateBranch)
    template(_self.templates.TestTemplatePullRequest)
})
