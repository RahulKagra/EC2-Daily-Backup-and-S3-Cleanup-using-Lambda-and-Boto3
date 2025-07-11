
# 🛡️ EC2 Daily Backup Automation – Assignment 11

This project automates daily backups of an EC2 instance using AWS Lambda, EventBridge Scheduler, and S3. The solution includes IAM roles and scheduled tasks to back up and store configuration files/logs securely.

---

## 📁 Project Components

### ✅ 1. Lambda Function
- **Function Name:** `EC2DailyBackupFunctionRahulk`
- **Region:** `us-west-2`
- **Status:** Successfully tested and deployed.
- **Purpose:** Executes daily to backup specified EC2 instance files to S3.
- **Test Result:** ✅ *Execution succeeded* (`logs available in CloudWatch`)

### ✅ 2. IAM Roles
#### A. `LambdaEC2BackupRoleRahulk`
- **Attached Policies:**
  - `AmazonEC2ReadOnlyAccess`
  - `AmazonS3FullAccess`
  - `CloudWatchLogsFullAccess`
- **Purpose:** Assigned to Lambda to allow EC2 metadata access, upload to S3, and log to CloudWatch.

#### B. `EC2SSMAccessRoleRahuk`
- **Attached Policy:** `AmazonSSMManagedInstanceCore`
- **Instance Profile:** Attached to EC2 instance for SSM access.

#### C. `EC2AutoTagLambdaRoleRahulk`
- **Attached Policies:**
  - `AmazonEC2FullAccess`
  - `LambdaSSMBackupAccess` (custom)
- **Purpose:** Supports automated EC2 tagging and SSM access.

---

## 🖥️ EC2 Instance
- **Name:** `EC2 Daily backup Rahulk`
- **Instance ID:** `i-0105a550c4e07a640`
- **Status:** Running and healthy (`2/2 checks passed`)
- **Role Attached:** `EC2SSMAccessRoleRahuk`

---

## 🕒 EventBridge Scheduler
- **Schedule Name:** `daily-ec2-backup-scheduler`
- **Schedule Rate:** `1 day` (runs daily)
- **Status:** Enabled
- **Time Zone:** Asia/Calcutta
- **Target:** Triggers `EC2DailyBackupFunctionRahulk`

---

## 🪣 S3 Bucket
- **Bucket Name:** `ec2-daily-backups-rahulk`
- **Region:** `us-west-2`
- **Purpose:** Stores daily backup files from EC2 via Lambda.
- **Current Files Uploaded:**
  - `Logs Ajni switch 14.txt`
  - `root@PAQSLAMSW2300-4 show configura.txt`

---

## ✅ Status Summary
| Component               | Status       | Remarks                                 |
|------------------------|--------------|------------------------------------------|
| Lambda Function        | ✅ Created   | Backup logic implemented and tested     |
| IAM Roles              | ✅ Configured | Correct policies attached               |
| EC2 Instance           | ✅ Running   | Role assigned, system ready             |
| EventBridge Scheduler  | ✅ Enabled   | Runs Lambda daily at fixed rate         |
| S3 Bucket              | ✅ Active    | Receives and stores backup files        |

---

## 📌 Notes
- Execution logs are available in **CloudWatch Logs**.
- IAM policy boundary restrictions were detected in some roles but do not affect this Lambda's functionality.
- Ensure EC2 instance has required file access and command execution rights.
