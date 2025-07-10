import boto3
from datetime import datetime, timezone, timedelta

# Replace this with your actual bucket name
BUCKET_NAME = 's3-cleanup-assignment-rahulk'

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    deleted_files = []

    # List all files in the bucket
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' in response:
        for obj in response['Contents']:
            last_modified = obj['LastModified']
            file_age = datetime.now(timezone.utc) - last_modified

            # If older than 30 days, delete it
            if file_age > timedelta(days=30):
                s3.delete_object(Bucket=BUCKET_NAME, Key=obj['Key'])
                deleted_files.append(obj['Key'])

    if deleted_files:
        print("Deleted files:")
        for key in deleted_files:
            print(key)
    else:
        print("No old files found.")

    return {
        'statusCode': 200,
        'body': f'Deleted files: {deleted_files}'
    }
