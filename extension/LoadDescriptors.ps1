# Requires the bulk load utility from the Ed-Fi-ODS repository
$args = @(
    # Uncomment the line below and set your year if you are using the
    # year-specific mode in the ODS / API.
    # "--year", "2021"
    "--retries", 0,
    "--data",  ".\descriptors",
    "--baseUrl", "http://localhost:54746/",
    "--working", "C:\temp\bulkd-upload-client",
    # Replace with valid key and secrete from your installation
    "--key", "5RUEXTjlDL8HebpyY2Gzg",
    "--secret", "HB3pt2Y9D4MCG0AmRLPrc",
    "--maxRequests", 1,
    "--include-stats",
    "--force",
    "--novalidation",
    "--extension", "ed-fi-lms"
)
$exe = "..\..\Ed-Fi-ODS\Utilities\DataLoading\EdFi.BulkLoadClient.Console\bin\Debug\netcoreapp3.1\EdFi.BulkLoadClient.Console.exe"
&$exe @args

