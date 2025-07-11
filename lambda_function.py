import boto3
import datetime
import time

# AWS clients
ssm = boto3.client('ssm')
s3 = boto3.client('s3')

# Configuration
INSTANCE_ID = 'i-0105a550c4e07a640'  # ✅ Your EC2 instance ID
S3_BUCKET = 'ec2-daily-backups-rahulk'  # ✅ Your S3 bucket
BACKUP_FOLDER = '/home/ec2-user/mydata'  # ✅ EC2 folder to backup

def lambda_handler(event, context):
    # 1. Prepare zip file name
    date_str = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
    backup_name = f"backup-{date_str}.zip"
    zip_path = f"/tmp/{backup_name}"
    s3_key = f"backups/{backup_name}"

    # 2. Run zip command on EC2 via SSM
    zip_command = f"cd {BACKUP_FOLDER} && zip -r {zip_path} ."
    print(f"Running zip command: {zip_command}")
    try:
        response = ssm.send_command(
            InstanceIds=[INSTANCE_ID],
            DocumentName='AWS-RunShellScript',
            Parameters={'commands': [zip_command]},
            TimeoutSeconds=60,
        )
        command_id = response['Command']['CommandId']

        # Wait a few seconds for the command to finish
        time.sleep(5)
        result = ssm.get_command_invocation(CommandId=command_id, InstanceId=INSTANCE_ID)

        if result['Status'] != 'Success':
            print("Zip failed:", result['StandardErrorContent'])
            return {"error": "Zip command failed"}
        else:
            print("Zip Success:", result['StandardOutputContent'])

    except Exception as e:
        print("Error running zip command:", str(e))
        return {"error": str(e)}

    # 3. Upload the zip to S3
    s3_upload_command = f"aws s3 cp {zip_path} s3://{S3_BUCKET}/{s3_key}"
    print(f"Uploading zip to S3: {s3_upload_command}")
    try:
        response = ssm.send_command(
            InstanceIds=[INSTANCE_ID],
            DocumentName='AWS-RunShellScript',
            Parameters={'commands': [s3_upload_command]},
            TimeoutSeconds=60,
        )
        command_id = response['Command']['CommandId']
        time.sleep(5)
        result = ssm.get_command_invocation(CommandId=command_id, InstanceId=INSTANCE_ID)

        if result['Status'] != 'Success':
            print("Upload failed:", result['StandardErrorContent'])
            return {"error": "Upload command failed"}
        else:
            print("Upload Success:", result['StandardOutputContent'])

    except Exception as e:
        print("Error uploading to S3:", str(e))
        return {"error": str(e)}

    # 4. Delete old backups from S3
    print("Checking for old backups to delete...")
    try:
        retention_days = 30
        cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=retention_days)

        response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix="backups/")
        if 'Contents' in response:
            for obj in response['Contents']:
                if obj['LastModified'] < cutoff:
                    print(f"Deleting: {obj['Key']} (last modified: {obj['LastModified']})")
                    s3.delete_object(Bucket=S3_BUCKET, Key=obj['Key'])
    except Exception as e:
        print("Error during cleanup:", str(e))
        return {"error": str(e)}

    return {"status": "Backup and cleanup completed successfully"}
