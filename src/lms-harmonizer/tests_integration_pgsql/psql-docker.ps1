# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

[CmdLetBinding()]
<#
    .SYNOPSIS
    Orchestrates call to psql running inside of a Docker container, mimicking a
    minimal set of functions from the actual psql interface.
#>
param(
    # Name of a Docker container instance running PostgreSQL
    [string]
    $ContainerName = 'lms_toolkit_pgsql',

    # psql's argument for print failed SQL commands to standard error output
    [switch]
    $b,

    # psql's argument for hostname (server).
    [string]
    $h = "localhost",

    # psql's argument for port number
    [string]
    $p = "5432",

    # psql's argument for username
    [string]
    $U,

    # psql's argument for database name
    [string]
    $d,

    # psql's argument for a SQL command. Only use of [$c, $f].
    [string]
    $c = "",

    # psql's argument for an input file containing SQL commands
    [string]
    $f = "",

    # psql's argument for suppressing prompt for password
    [switch]
    $w
)

$command = "psql -h $h -p $p -U $U -d $d"

if ($env:PGPASSWORD.Length -gt 0) {
    $command = "export PGPASSWORD='$env:PGPASSWORD' && $command"
}

if ($b) {
    $command += " -b"
}

if ($f.Length -gt 0) {
    # Transfer the file into the container for execution
    &docker cp "$f" "$($ContainerName):/opt/temp.sql"
    write-host "&docker cp $f $($ContainerName):/opt/temp.sql"
    $command += " -f /opt/temp.sql"
}
else {
    $command += " -c '$c'"
}

&docker exec $ContainerName /bin/bash -c "$command"
