
# CreativeFlow — IAM Security Test Report

**Project:** CreativeFlow AWS Cloud Security Lab  
**Date:** 29 October 2026  
**Environment:** AWS eu-west-3 (Paris)  
**Tools:** AWS CLI, Flask, Boto3, Amazon EC2, Amazon S3

## 1. Objective

Verify that the AWS IAM roles enforce different
access permissions following the principle of
least privilege.

Two roles were tested:

- EC2-Developer-Role
- EC2-Contributor-Role

The roles were assigned to the EC2 instance
separately during testing.

## 2. Test Environment

- Amazon Linux 2023
- Python Flask web application
- Amazon S3 private bucket
- AWS CLI and Boto3
- IAM instance profiles
- SSH tunnel for secure browser access

## 3. Developer Role Tests

| Test | Expected | Actual |
|---|---|---|
| Assume Developer role | Allowed | PASS |
| List S3 bucket root | Allowed | PASS |
| List uploads folders | Allowed | PASS |
| Upload document | Allowed | PASS |
| Download document | Allowed | PASS |
| Upload application log | Allowed | PASS |
| Read application log | Allowed | PASS |

### Evidence

The AWS CLI successfully identified:

`assumed-role/EC2-Developer-Role/`

The Developer successfully uploaded and read
a test log in the protected app-logs/ prefix.

The Flask application displayed:

`Log access granted - Developer role confirmed`

## 4. Contributor Role Tests

| Test | Expected | Actual |
|---|---|---|
| Assume Contributor role | Allowed | PASS |
| List uploads/drafts/ | Allowed | PASS |
| Download draft document | Allowed | PASS |
| Upload draft document | Allowed | PASS |
| Read application log | Denied | PASS |
| List S3 bucket root | Denied | PASS |
| Upload through Flask | Allowed | PASS |
| Download through Flask | Allowed | PASS |

### Evidence

The AWS CLI confirmed:

`assumed-role/EC2-Contributor-Role/`

Attempting to read the protected application
log returned:

`403 Forbidden (HeadObject)`

Attempting to list the S3 bucket root returned:

`AccessDenied (ListObjectsV2)`

The Flask application displayed:

`Log access denied - Contributor role detected`

These results match the expected IAM restrictions.

## 5. Application Functionality

The following features were verified:

- Web interface accessible through SSH forwarding
- Document upload to Amazon S3
- S3 object listing
- Document download
- IAM role identification
- Developer and Contributor access behavior

The downloaded test files matched the
original uploaded files.

## 6. Troubleshooting

### Problem

A document download initially returned:

`SignatureDoesNotMatch`

### Resolution

For the lab, the presigned-URL download flow
was replaced with server-side object retrieval
through Boto3 and Flask.

### Result

The application successfully downloaded
documents without the previous signature error.

## 7. Security Controls

- S3 Block Public Access enabled
- Default SSE-S3 encryption
- IAM role-based AWS permissions
- Temporary credentials via EC2 instance profile
- SSH access restricted to an authorized source
- Flask bound to localhost
- Flask debug mode disabled
- Application accessed through an SSH tunnel

## 8. Security Limitations

This was an educational proof of concept.

The web application did not authenticate individual
users. Each request used the IAM role assigned to
the EC2 instance.

The Flask role-status message was an application
check, whereas the AWS CLI denial responses
provided independent evidence of S3 authorization.

Additional controls would be required for production,
including user authentication, server-side user
authorization, HTTPS, monitoring, and a production
WSGI server.

## 9. Cleanup Verification

The following project resources were deleted:

- EC2 instance
- S3 bucket and objects
- IAM roles and custom policies
- EC2 SSH key pair
- Project security group

Checks also confirmed no remaining EBS volumes,
owned EBS snapshots, or Elastic IP allocations
in the test Region.

## 10. Conclusion

The tested IAM permissions and restrictions
behaved as expected.

The exercise demonstrated practical experience in:

- AWS Identity and Access Management
- Least privilege
- S3 access-control testing
- Linux and AWS CLI
- Python and Boto3 integration
- Cloud security troubleshooting
