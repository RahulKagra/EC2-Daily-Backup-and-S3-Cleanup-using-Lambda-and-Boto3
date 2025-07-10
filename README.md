# 📦 EC2 Daily Backup and S3 Cleanup using Lambda and Boto3

This project automates daily file backups from an EC2 instance to an S3 bucket and deletes backup files older than 30 days using AWS Lambda.

---

##  Objective

-  Automatically back up specific folders from an EC2 instance to S3 every day.
-  Automatically delete backup files from S3 that are older than 30 days.

---

##  AWS Services Used

- **EC2** – for source data and running backup cron job
- **S3** – to store backup `.zip` files
- **Lambda** – to clean up old backups from S3
- **EventBridge (CloudWatch Events)** – to schedule Lambda daily
- **IAM** – to grant required permissions to EC2 and Lambda

---

##  Folder Structure
```
ec2-daily-backup-s3/
└── backups/
├── backup-2025-06-28-13-00.zip
├── backup-2025-06-29-13-00.zip
└── ...
```
---

##  Part 1: EC2 Setup (Backup and Upload to S3)

### Create S3 Bucket

- Go to AWS S3 Console
- Create a bucket named: `ec2-daily-backup-s3`
- Create a folder (prefix) inside: `backups/`

---

### Part 2: Attach IAM Role to EC2

Role Name: `jigar-EC2-SSM-Role-Autodelete`

#### Inline Policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::ec2-daily-backup-s3",
        "arn:aws:s3:::ec2-daily-backup-s3/*"
      ]
    }
  ]
}

```
---
### Part 3: Attach IAM Role to EC2
- SSH into your EC2
```bash
  sudo apt install
  crontab -e
  0 15 * * * zip -r /tmp/backup-$(date +\%F-\%H-\%M).zip /home/ubuntu/backupauto && aws s3 sync /tmp/ s3://ec2-daily-backup-s3/backups/ --exclude "*" --include "backup-*.zip"

```
## Lambda Setup (Cleanup Old Backups)
-Create IAM Role for Lambda
  -Role name: auto-backup-30-old-files-role
  ```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": "arn:aws:s3:::ec2-daily-backup-jixxx"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:DeleteObject"],
      "Resource": "arn:aws:s3:::ec2-daily-backup-jixxx/*"
    }
  ]
}
```
### Lambda Code (Python + Boto3)
  - **Please find the lamda code in "lamda_function.py"**
  - Schedule Lambda Daily
      - Go to CloudWatch > Rules
      - Create a rule with:
          - Schedule: rate(1 day)
          - Target: your Lambda function
       
---
## 📸 Screenshots – EC2 Backup and Cleanup Automation

| Description                    | Screenshot |
|-------------------------------|------------|
| EC2 Instance - Cron Job Output | ![](screenshots/EC2%20Instance_Cron%20Job%20Output.png) |
| IAM Role Attached to EC2       | ![](screenshots/IAM%20Role%20Attached%20to%20EC2.png)    |
| Lambda Function                | ![](screenshots/Lambda%20Function.png)                   |
| S3 Bucket                      | ![](screenshots/S3%20Bucket.png)                         |

---
## Notes
  - Ensure timezones (EC2 vs UTC) align.
  - Bucket names and paths must match exactly in IAM policies and code.
  - IAM roles are critical — no permission = no upload/delete.

---
## 📸 Architecture Diagram
```java
EC2 Instance
   |
   | (cron job zips + uploads)
   v
S3 Bucket (ec2-daily-backup-jigar/backups/)
   ^
   | (Lambda deletes backups > 30 days)
   |
Lambda Function (via CloudWatch schedule)
```




       
  
      




  
  

