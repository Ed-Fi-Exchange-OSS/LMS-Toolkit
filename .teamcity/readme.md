# Getting Started

To apply these build configuration settings on a new TeamCity environment (min
version: `2019.2.x`):

1. Create a "root" project that will contain this work as a sub-project, e.g.
   `Exchange` below `R&D`
1. Ensure these parameters are set:

    ```none
    github.organization = <org name or username>
    github.username = <username>
    github.accessToken.protected (password type) = <access token>
    github.accessToken = %github.accessToken.protected%
    git.branch.default = main
    git.branch.specification = +:refs/heads/(*)
                               +:(refs/pull/*/head)
    ```

    If pull from an organization, use that organization's name. Else use own
    GitHub user name to pull from your fork.

1. Create a VCS Root:
    * Type: `Git`
    * Name: `Fizz`
    * Fetch Url: `https://github.com/%github.organization%/Ed-Fi-X-Fizz`
    * Default Branch: `%git.branch.default%`
    * Branch Specification: `%git.branch.specification%`
    * Authentication method: `password`
    * Username: `%github.username%`
    * Password: `%github.accessToken%`
1. Create a sub-project named "Fizz"
1. Turn on Versioned Settings:
    * Synchronization enabled: `true`
    * Project settings VCS root: `Fizz`
    * When build starts: `use settings from VCS`
    * Store secure values outside of VCS: `true`
    * Settings format: `kotlin`
    * Generate portable DSL scripts: `true`
1. Click Apply.
1. If prompted to choose either committing current changes or reading from the
   VCS root, then choose to read from the VCS root.
1. Else click on the "Load project settings from VCS..." button.
