
# CreativeFlow — Flask Application

This directory contains the Python Flask application
developed for the CreativeFlow AWS cybersecurity lab.

## Components

- `app.py` — Flask application and AWS S3 operations
- `requirements.txt` — Python dependencies
- `templates/index.html` — Web interface

## Security

The application uses Boto3 with temporary AWS
credentials provided by an EC2 IAM instance profile.

Developer and Contributor roles were tested separately
to validate S3 access restrictions.

## Disclaimer

This application is an educational proof of concept,
not a production-ready deployment.
