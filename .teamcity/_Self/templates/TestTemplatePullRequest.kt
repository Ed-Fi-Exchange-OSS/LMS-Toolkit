// SPDX-License-Identifier: Apache-2.0
// Licensed to the Ed-Fi Alliance under one or more agreements.
// The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
// See the LICENSE and NOTICES files in the project root for more information.

package _self.templates

import jetbrains.buildServer.configs.kotlin.v2019_2.*
import jetbrains.buildServer.configs.kotlin.v2019_2.buildFeatures.commitStatusPublisher
import jetbrains.buildServer.configs.kotlin.v2019_2.buildFeatures.PullRequests
import jetbrains.buildServer.configs.kotlin.v2019_2.buildFeatures.pullRequests
import jetbrains.buildServer.configs.kotlin.v2019_2.triggers.VcsTrigger
import jetbrains.buildServer.configs.kotlin.v2019_2.triggers.vcs

object TestTemplatePullRequest : TestTemplateBase() {
    init {
        name = "Python Test Template for Pull Requests"
        id = RelativeId("TestTemplatePullRequest")

        features {
            commitStatusPublisher {
                publisher = github {
                    githubUrl = "https://api.github.com"
                    authType = personalToken {
                        token = "%github.accessToken%"
                    }
                }
            }
            pullRequests {
                vcsRootExtId = "${DslContext.settingsRoot.id}"
                provider = github {
                    authType = token {
                        token = "%github.accessToken%"
                    }
                    filterTargetBranch = "+:<default>"
                    filterAuthorRole = PullRequests.GitHubRoleFilter.MEMBER_OR_COLLABORATOR
                }
            }
        }

        triggers {
            vcs {
                id ="vcsTrigger"
                quietPeriodMode = VcsTrigger.QuietPeriodMode.USE_CUSTOM
                quietPeriod = 120
                // This allows triggering on "anything" and then removes
                // triggering on the default branch and in feature branches,
                // thus leaving only the pull requests.
                branchFilter = """
                    +:pull/*
                """.trimIndent()
            }
        }
    }
}
