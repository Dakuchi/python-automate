# AWS Automation Scripts

This project provides a collection of Python scripts designed to automate interactions with AWS services. These scripts facilitate various tasks, from managing EC2 and EKS resources to monitoring and performing backups, making it easier to handle routine AWS operations.

## Table of Contents

- [Scripts Overview](#scripts-overview)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Scripts Overview

### 1. Add_env_tag/
Adds environment-specific tags to AWS resources for better identification and management.

### 2. Cleanup_Snapshot/
Cleans up old or unused snapshots to reduce storage costs by removing outdated backups.

### 3. Create_VPC/
Automates the creation of a Virtual Private Cloud (VPC), subnets, route tables, and other networking components.

### 4. EC2_status_check/
Checks the status of EC2 instances across various regions, ensuring instances are running or reporting issues if they’re not.

### 5. EKS_status_check/
Verifies the status of EKS clusters and their associated nodes, ensuring Kubernetes workloads are operating as expected.

### 6. Monitor_Website/
Monitors a specified website’s uptime and availability, logging results and notifying if downtime occurs.

### 7. Restore_Volume/
Restores EBS volumes from snapshots, aiding in disaster recovery and data restoration processes.

### 8. Schedule_status_check/
Schedules regular status checks for specified AWS resources, ensuring consistent monitoring without manual intervention.

### 9. Volumes_Backup/
Backs up EC2 volumes by creating EBS snapshots on a scheduled or ad-hoc basis to protect against data loss.

## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your_username/aws-automation-scripts.git
   cd aws-automation-scripts
