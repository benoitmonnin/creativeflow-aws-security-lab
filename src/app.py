"""CreativeFlow demo portal — lab only, accessed via an SSH tunnel.

This app deliberately has no end-user authentication. The instance's single
IAM role applies to every request. Do not make this endpoint public.
"""
import logging
import os
from io import BytesIO
from pathlib import PurePosixPath

import boto3
from botocore.exceptions import ClientError
from flask import Flask, jsonify, render_template, request, send_file
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB lab limit

BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
AWS_REGION = os.environ.get('AWS_REGION', 'eu-west-3')
CATEGORIES = {'drafts', 'final', 'client-assets'}
s3_client = boto3.client('s3', region_name=AWS_REGION)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Cache-Control'] = 'no-store'
    return response


@app.errorhandler(RequestEntityTooLarge)
def upload_too_large(error):
    return jsonify(error='File exceeds 10 MB lab limit'), 413


def current_role():
    try:
        return boto3.client('sts').get_caller_identity().get('Arn', 'Unknown')
    except Exception:
        logger.exception('Could not identify current IAM role')
        return 'Unknown'


def list_uploaded_files():
    result = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix='uploads/')
    return [
        {
            'name': item['Key'].rsplit('/', 1)[-1],
            'key': item['Key'],
            'size': item['Size'],
            'last_modified': item['LastModified'].isoformat(),
        }
        for item in result.get('Contents', [])
        if not item['Key'].endswith('/')
    ]


@app.get('/')
def index():
    try:
        files = list_uploaded_files()
        error = None
    except ClientError:
        logger.exception('Failed to list uploaded files')
        files, error = [], 'Unable to list files: check the EC2 IAM role.'
    return render_template('index.html', files=files, role=current_role(), error=error)


@app.post('/upload')
def upload_file():
    f = request.files.get('file')
    category = request.form.get('category', 'drafts')
    if f is None or not f.filename:
        return jsonify(error='Select a file'), 400
    if category not in CATEGORIES:
        return jsonify(error='Invalid upload category'), 400
    filename = secure_filename(f.filename)
    if not filename:
        return jsonify(error='Invalid filename'), 400
    key = f'uploads/{category}/{filename}'
    try:
        s3_client.upload_fileobj(f, BUCKET_NAME, key)
        logger.info('Uploaded %s using IAM role %s', key, current_role())
        return jsonify(message='File uploaded successfully', file=filename, category=category)
    except ClientError:
        logger.exception('S3 upload failed')
        return jsonify(error='Upload failed: check S3 permissions'), 403


@app.get('/download/<path:filename>')
def download_file(filename):
    # Only allow CATEGORY/BASENAME beneath uploads/ (no app-logs/ access).
    pieces = PurePosixPath(filename).parts
    if len(pieces) != 2 or pieces[0] not in CATEGORIES or pieces[1] in ('.', '..') or secure_filename(pieces[1]) != pieces[1]:
        return jsonify(error='Invalid document path'), 400
    key = f'uploads/{pieces[0]}/{pieces[1]}'
    # Fetch through the EC2 instance role instead of redirecting the browser
    # to a presigned S3 URL (the latter failed in the original lab).
    # This route is intended for localhost + SSH tunneling only.
    max_bytes = 10 * 1024 * 1024
    try:
        obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
        body = obj['Body']
        try:
            if obj.get('ContentLength', 0) > max_bytes:
                return jsonify(error='Document exceeds the 10 MB lab limit'), 413
            data = body.read(max_bytes + 1)
        finally:
            body.close()
        if len(data) > max_bytes:
            return jsonify(error='Document exceeds the 10 MB lab limit'), 413
        return send_file(
            BytesIO(data),
            as_attachment=True,
            download_name=pieces[1],
            mimetype='application/octet-stream',
        )
    except ClientError as exc:
        code = exc.response.get('Error', {}).get('Code', '')
        if code in ('AccessDenied', 'AllAccessDisabled', '403'):
            return jsonify(error='Access denied: check S3 permissions'), 403
        if code in ('NoSuchKey', 'NotFound', '404'):
            return jsonify(error='Document not found'), 404
        logger.exception('S3 download failed')
        return jsonify(error='Unable to download document'), 502


@app.get('/files')
def list_files():
    try:
        return jsonify(files=list_uploaded_files())
    except ClientError:
        logger.exception('S3 listing failed')
        return jsonify(error='Unable to list files'), 403


@app.get('/logs')
def view_logs():
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix='app-logs/')
        return jsonify(logs=[x['Key'] for x in response.get('Contents', [])], access='granted')
    except ClientError as e:
        if e.response.get('Error', {}).get('Code') in ('AccessDenied', 'AllAccessDisabled'):
            return jsonify(error='Access denied: Developer role required', access='denied'), 403
        logger.exception('Log listing failed')
        return jsonify(error='Log listing failed'), 500


if __name__ == '__main__':
    if not BUCKET_NAME:
        raise SystemExit('Set S3_BUCKET_NAME before running CreativeFlow')
    # Never open the development server to the internet.
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
