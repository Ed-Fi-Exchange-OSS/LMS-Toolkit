# We need to copy the LMS-DS loader and sample files to a local directory so
# that they can be copied into the Docker image.
$tmp = New-Item -Type Directory -Path tmp -Force

Copy-Item -Recurse -Path "../../src/lms-ds-loader" -Destination $tmp -Force
Copy-Item -Recurse -Path "../../docs/sample-out" -Destination $tmp -Force

# Now we can build the image
docker build -t test-lms-ds-loader:latest .
