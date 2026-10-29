# creativeflow-aws-security-lab
Hands-on AWS Cloud Security project implementing IAM least privilege, S3 access controls, EC2, Flask and Boto3.

# CreativeFlow — AWS Cloud Security Lab

**AWS IAM | Amazon S3 | EC2 | Python | Flask | Boto3 | Linux**

**Project type:** Cybersecurity / Cloud Security  
**Training:** Jedha Fullstack Cybersecurity  
**Completed:** October 2026  
**AWS Region:** Europe (Paris), eu-west-3

## 1. Project Overview

CreativeFlow is a practical AWS cloud security project developed during my Jedha cybersecurity training.

The objective was to deploy a secure document management application for a fictional marketing agency and implement differentiated access permissions.

The project demonstrates practical knowledge of AWS identity management, cloud storage security, Python development, and access-control testing.

## 2. Technologies

- AWS IAM — Identity and Access Management
- Amazon EC2 — Cloud computing
- Amazon S3 — Secure document storage
- Python / Flask — Web application
- Boto3 — AWS SDK for Python
- Amazon Linux 2023 — Operating system
- SSH / SCP — Secure administration and file transfers
- AWS CLI — Security verification

## 3. Architecture

The application uses the following architecture:

Windows Browser
    |
    | Encrypted SSH Tunnel
    v
Amazon EC2
    |
    | Flask + Boto3
    v
IAM Instance Role
    |
    v
Amazon S3
    |
    +-- uploads/drafts/
    +-- uploads/final/
    +-- uploads/client-assets/
    +-- app-logs/

## 4. IAM Security Design

Two separate IAM roles were implemented.

### Developer Role

- Upload and download documents
- List S3 bucket contents
- Read and write application logs
- Manage project S3 objects

### Contributor Role

- Upload and download permitted documents
- List permitted uploads folders
- Cannot access application logs
- Cannot list the root of the S3 bucket

The project demonstrates the principle of least privilege.

## 5. Security Tests

| Security Test | Developer | Contributor |
|---|---|---|
| Upload documents | Allowed | Allowed |
| Download documents | Allowed | Allowed |
| List permitted files | Allowed | Allowed |
| Access application logs | Allowed | Denied |
| List S3 bucket root | Allowed | Denied |

Tests were performed using AWS CLI and the Flask web application.

## 6. Troubleshooting

During testing, an S3 SignatureDoesNotMatch error occurred when downloading documents.

The issue was resolved for the lab by replacing the presigned-URL download mechanism with server-side Boto3 object retrieval through Flask.

This demonstrated practical troubleshooting of AWS application integration.

## 7. Security Measures

- IAM instance profiles instead of hardcoded credentials
- Restricted IAM permissions
- Private S3 bucket with public access blocked
- S3 server-side encryption
- SSH access restricted to an authorized IP
- Encrypted SSH tunnel for application access
- Flask debug mode disabled
- Positive and negative authorization testing

## 8. Security Limitations

This project is an educational proof of concept, not a production deployment.

IAM permissions were tested by changing the EC2 instance role. The application does not authenticate individual web users or enforce individual user roles.

Production deployment would require user authentication, server-side authorization, HTTPS, a production WSGI server, monitoring, and additional security hardening.

## 9. AWS Resource Cleanup

After testing, the following project resources were removed:

- EC2 instance
- S3 bucket and objects
- Developer and Contributor IAM roles
- Associated custom IAM policies
- SSH key pair
- Application security group

Verification confirmed no remaining EBS volumes, owned snapshots, or Elastic IP addresses in the test Region.

## 10. Learning Outcomes

This project strengthened my understanding of:

- AWS cloud architecture
- IAM roles and least privilege
- Secure S3 storage
- Python and AWS SDK integration
- Access-control testing
- Linux server administration
- Cloud troubleshooting
- Secure resource lifecycle management

---

**Project completed as part of my Jedha Fullstack Cybersecurity training.**
