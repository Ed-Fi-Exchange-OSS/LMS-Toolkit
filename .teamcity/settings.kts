import jetbrains.buildServer.configs.kotlin.v2019_2.*
import jetbrains.buildServer.configs.kotlin.v2019_2.buildFeatures.PullRequests
import jetbrains.buildServer.configs.kotlin.v2019_2.buildFeatures.commitStatusPublisher
import jetbrains.buildServer.configs.kotlin.v2019_2.buildFeatures.freeDiskSpace
import jetbrains.buildServer.configs.kotlin.v2019_2.buildFeatures.pullRequests
import jetbrains.buildServer.configs.kotlin.v2019_2.buildFeatures.swabra
import jetbrains.buildServer.configs.kotlin.v2019_2.buildSteps.script
import jetbrains.buildServer.configs.kotlin.v2019_2.triggers.VcsTrigger
import jetbrains.buildServer.configs.kotlin.v2019_2.triggers.vcs

/*
The settings script is an entry point for defining a TeamCity
project hierarchy. The script should contain a single call to the
project() function with a Project instance or an init function as
an argument.

VcsRoots, BuildTypes, Templates, and subprojects can be
registered inside the project using the vcsRoot(), buildType(),
template(), and subProject() methods respectively.

To debug settings scripts in command-line, run the

    mvnDebug org.jetbrains.teamcity:teamcity-configs-maven-plugin:generate

command and attach your debugger to the port 8000.

To debug in IntelliJ Idea, open the 'Maven Projects' tool window (View
-> Tool Windows -> Maven Projects), find the generate task node
(Plugins -> teamcity-configs -> teamcity-configs:generate), the
'Debug' option is available in the context menu for the task.
*/

version = "2019.2"

project {
    description = "Project Fizz Utilities for Learning Management System Data"

    template(TestTemplateBranch)
    template(TestTemplatePullRequest)

    params {
        param("git.branch.default", "main")
        param("build.feature.freeDiskSpace", "2gb")
        param("git.branch.specification", """
            refs/heads/(*)
            refs/(pull/*)/head
        """.trimIndent())
    }

    subProject(SchoologyProject)
    subProject(FileUtilsProject)
    subProject(GoogleClassroomProject)
    subProject(FileTesterProject)
}

object TestTemplateBranch : Template({
    name = "Python Test Template for Branches"

    artifactRules = "+:%project.directory%/htmlcov => coverage.zip"

    vcs {
        root(DslContext.settingsRoot, "%vcs.checkout.rules%")
    }

    steps {
        script {
            name = "Install"
            id = "TEMPLATE_RUNNER_1"
            executionMode = BuildStep.ExecutionMode.RUN_ON_SUCCESS
            workingDir = "eng"
            scriptContent = "python ./build.py install ../%project.directory%"
            formatStderrAsError = true
        }
        script {
            name = "Run Tests with Coverage"
            id = "TEMPLATE_RUNNER_2"
            executionMode = BuildStep.ExecutionMode.RUN_ON_SUCCESS
            workingDir = "eng"
            scriptContent = "python ./build.py coverage:html ../%project.directory%"
            formatStderrAsError = true
        }
        script {
            name = "Type Check"
            id = "TEMPLATE_RUNNER_3"
            executionMode = BuildStep.ExecutionMode.RUN_ON_FAILURE
            workingDir = "eng"
            scriptContent = "python ./build.py typecheck:xml ../%project.directory%"
            formatStderrAsError = true
        }
        script {
            name = "Style Check"
            id = "TEMPLATE_RUNNER_4"
            executionMode = BuildStep.ExecutionMode.RUN_ON_FAILURE
            workingDir = "eng"
            scriptContent = "python ./build.py lint ../%project.directory%"
            formatStderrAsError = true
        }
    }

    triggers {
        vcs {
            id = "vcsTrigger"
            quietPeriodMode = VcsTrigger.QuietPeriodMode.USE_CUSTOM
            quietPeriod = 120
            branchFilter = "+:<default>"
        }
    }

    failureConditions {
        errorMessage = true
    }

    features {
        freeDiskSpace {
            id = "jetbrains.agent.free.space"
            requiredSpace = "%build.feature.freeDiskSpace%"
            failBuild = true
        }
        swabra {
            id = "TEMPLATE_BUILD_EXT_1"
            forceCleanCheckout = true
        }
        feature {
            id = "TEMPLATE_BUILD_EXT_2"
            type = "xml-report-plugin"
            param("xmlReportParsing.reportType", "junit")
            param("xmlReportParsing.reportDirs", "+:%project.directory%/mypy.xml")
        }
    }
})

object TestTemplatePullRequest : Template({
    name = "Python Test Template for Pull Requests"

    artifactRules = "+:%project.directory%/htmlcov => coverage.zip"

    vcs {
        root(DslContext.settingsRoot, "%vcs.checkout.rules%")
    }

    steps {
        script {
            name = "Install"
            id = "TEMPLATE_RUNNER_5"
            executionMode = BuildStep.ExecutionMode.RUN_ON_SUCCESS
            workingDir = "eng"
            scriptContent = "python ./build.py install ../%project.directory%"
            formatStderrAsError = true
        }
        script {
            name = "Run Tests with Coverage"
            id = "TEMPLATE_RUNNER_6"
            executionMode = BuildStep.ExecutionMode.RUN_ON_SUCCESS
            workingDir = "eng"
            scriptContent = "python ./build.py coverage:html ../%project.directory%"
            formatStderrAsError = true
        }
        script {
            name = "Type Check"
            id = "TEMPLATE_RUNNER_7"
            executionMode = BuildStep.ExecutionMode.RUN_ON_FAILURE
            workingDir = "eng"
            scriptContent = "python ./build.py typecheck:xml ../%project.directory%"
            formatStderrAsError = true
        }
        script {
            name = "Style Check"
            id = "TEMPLATE_RUNNER_8"
            executionMode = BuildStep.ExecutionMode.RUN_ON_FAILURE
            workingDir = "eng"
            scriptContent = "python ./build.py lint ../%project.directory%"
            formatStderrAsError = true
        }
    }

    triggers {
        vcs {
            id = "vcsTrigger"
            quietPeriodMode = VcsTrigger.QuietPeriodMode.USE_CUSTOM
            quietPeriod = 120
            branchFilter = "+:pull/*"
        }
    }

    failureConditions {
        errorMessage = true
    }

    features {
        freeDiskSpace {
            id = "jetbrains.agent.free.space"
            requiredSpace = "%build.feature.freeDiskSpace%"
            failBuild = true
        }
        swabra {
            id = "TEMPLATE_BUILD_EXT_3"
            forceCleanCheckout = true
        }
        feature {
            id = "TEMPLATE_BUILD_EXT_4"
            type = "xml-report-plugin"
            param("xmlReportParsing.reportType", "junit")
            param("xmlReportParsing.reportDirs", "+:%project.directory%/mypy.xml")
        }
        commitStatusPublisher {
            id = "TEMPLATE_BUILD_EXT_5"
            publisher = github {
                githubUrl = "https://api.github.com"
                authType = personalToken {
                    token = "credentialsJSON:581aea0c-1320-4500-b82e-7cecbf4251be"
                }
            }
        }
        pullRequests {
            id = "TEMPLATE_BUILD_EXT_6"
            vcsRootExtId = "EdFi_RDTeam_Exchange_Fizz"
            provider = github {
                authType = token {
                    token = "credentialsJSON:581aea0c-1320-4500-b82e-7cecbf4251be"
                }
                filterTargetBranch = "+:<default>"
                filterAuthorRole = PullRequests.GitHubRoleFilter.MEMBER_OR_COLLABORATOR
            }
        }
    }
})


object FileTesterProject : Project({
    name = "File Tester"
    description = "Python scripts for validating the output from an extractor"

    buildType(FileTester_TestBranch)
    buildType(FileTester_TestPullRequest)

    params {
        param("project.directory", "./utils/file-tester")
        param("vcs.checkout.rules", """
            +:.teamcity => .teamcity
            +:%project.directory% => %project.directory%
            +:eng => eng
            +:src/file-utils => src/file-utils
        """.trimIndent())
    }
})

object FileTester_TestBranch : BuildType({
    templates(TestTemplateBranch)
    name = "Branch Testing"
})

object FileTester_TestPullRequest : BuildType({
    templates(TestTemplatePullRequest)
    name = "Pull Request Testing"
})


object FileUtilsProject : Project({
    name = "File Utilities"
    description = "Python scripts for interacting the LMS filesystem created by the extractors"

    buildType(TestBranch)
    buildType(FileUtils_TestPullRequest)

    params {
        param("project.directory", "./src/file-utils")
        param("vcs.checkout.rules", """
            +:.teamcity => .teamcity
            +:%project.directory% => %project.directory%
            +:eng => eng
        """.trimIndent())
    }
})

object FileUtils_TestPullRequest : BuildType({
    templates(TestTemplatePullRequest)
    name = "Pull Request Testing"
})

object TestBranch : BuildType({
    templates(TestTemplateBranch)
    name = "Branch Testing"
})


object GoogleClassroomProject : Project({
    name = "Google Classroom Utilities"
    description = "Python scripts for interacting with Google Classroom"

    buildType(GoogleClassRoom_TestPullRequest)
    buildType(GoogleClassRoom_TestBranch)

    params {
        param("project.directory", "./src/google-classroom-extractor")
        param("vcs.checkout.rules", """
            +:.teamcity => .teamcity
            +:%project.directory% => %project.directory%
            +:eng => eng
            +:./src/lib => ./src/lib
        """.trimIndent())
    }
})

object GoogleClassRoom_TestBranch : BuildType({
    templates(TestTemplateBranch)
    name = "Branch Testing"
})

object GoogleClassRoom_TestPullRequest : BuildType({
    templates(TestTemplatePullRequest)
    name = "Pull Request Testing"
})


object SchoologyProject : Project({
    name = "Schoology Utilities"
    description = "Python scripts for interacting with Schoology"

    buildType(Schoology_TestPullRequest)
    buildType(Schoology_TestBranch)

    params {
        param("project.directory", "./src/schoology-extractor")
        param("vcs.checkout.rules", """
            +:.teamcity => .teamcity
            +:%project.directory% => %project.directory%
            +:eng => eng
        """.trimIndent())
    }
})

object Schoology_TestBranch : BuildType({
    templates(TestTemplateBranch)
    name = "Branch Testing"
})

object Schoology_TestPullRequest : BuildType({
    templates(TestTemplatePullRequest)
    name = "Pull Request Testing"
})
