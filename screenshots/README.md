
# CreativeFlow — Security Evidence

This folder contains screenshots from the AWS
CreativeFlow cybersecurity lab.

## Evidence

1. Developer access granted
2. Developer S3 log access
3. Contributor document upload
4. Contributor log access denied
5. AWS CLI AccessDenied security tests

Screenshots are sanitized to remove personal
information and AWS account identifiers.

The project infrastructure was deleted after testing.

## Contributor — Access Denied

The following screenshot shows the CreativeFlow application
detecting the Contributor role and denying access
to the developer-only log feature.

![Contributor access denied](04-contributor-access-denied-original.png)

**Result:** PASS — Contributor log access denied.

The AWS CLI independently confirmed S3 access restrictions
with a 403 Forbidden response.
