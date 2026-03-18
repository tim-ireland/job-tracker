# Data Directory Configuration Guide

**Last Updated:** March 18, 2026

---

## Overview

The Job Search Toolkit separates your personal job search data from the application code. Your data directory can be located anywhere on your system and is mounted into the Docker container at `/data`.

---

## Quick Start

### Default Setup
By default, the data directory is expected at `../my-job-search-2026` (one level up from the repo):

```
/Users/yourname/Development/
├── job-search-toolkit/        # This repo (code)
└── my-job-search-2026/         # Your data (private)
    ├── applications/
    ├── source_material/
    └── job_applications.db
```

**Start with defaults:**
```bash
docker-compose up -d
```

---

## Custom Data Directory Location

### Option 1: Environment Variable (Recommended)

Set `DATA_PATH` environment variable before starting:

```bash
# Linux/macOS
export DATA_PATH=/path/to/your/job-search-data
docker-compose up -d

# Or inline
DATA_PATH=/path/to/your/job-search-data docker-compose up -d
```

```powershell
# Windows PowerShell
$env:DATA_PATH="C:\Users\YourName\JobSearch"
docker-compose up -d
```

### Option 2: .env File (Persistent)

Create a `.env` file in the repository root:

```bash
# Copy example
cp .env.example .env

# Edit .env
DATA_PATH=/absolute/path/to/your/data
HOST_PORT=8000
```

Then start normally:
```bash
docker-compose up -d
```

### Option 3: Edit docker-compose.yml Directly

Modify `docker-compose.yml`:

```yaml
services:
  job-tracker:
    volumes:
      # Change this line:
      - /absolute/path/to/your/data:/data
```

---

## Data Directory Structure

Your data directory should contain:

```
your-job-search-data/
├── applications/                    # Job application directories
│   ├── Company1_Role1/
│   │   ├── job_description.txt
│   │   ├── config.txt
│   │   ├── resume.tex
│   │   ├── resume.pdf
│   │   ├── cover_letter.tex
│   │   └── cover_letter.pdf
│   └── Company2_Role2/
│       └── ...
│
├── source_material/                 # Your documented experience (single source of truth)
│   ├── experiences/
│   │   ├── company1.md
│   │   ├── company2.md
│   │   └── company3.md
│   ├── achievements/
│   │   ├── achievement1.md
│   │   └── achievement2.md
│   ├── skills/
│   │   ├── technical_skills.md
│   │   └── leadership_skills.md
│   ├── projects/
│   │   └── notable_projects.md
│   └── metrics/
│       └── quantified_results.md
│
├── custom_templates/                # Optional: Your custom LaTeX templates
│   ├── my_resume_template.tex
│   └── my_cover_letter_template.tex
│
└── job_applications.db              # SQLite database
```

---

## First-Time Setup

### Automatic Initialization

On first run, the container will create the data directory structure if it doesn't exist:

```bash
docker-compose up -d
# Creates: applications/, source_material/, job_applications.db
```

### Manual Initialization

Create the structure yourself:

```bash
# Set your data path
export DATA_PATH=/path/to/your/data

# Create directories
mkdir -p $DATA_PATH/{applications,source_material/{experiences,achievements,skills,projects,metrics},custom_templates}

# Start container
docker-compose up -d
```

---

## Environment Variables Reference

### Host Environment (docker-compose)

| Variable | Default | Description |
|----------|---------|-------------|
| `DATA_PATH` | `../my-job-search-2026` | Absolute or relative path to your data directory on the host |
| `HOST_PORT` | `8000` | Port to expose the web application on |

### Container Environment (inside Docker)

| Variable | Value | Description |
|----------|-------|-------------|
| `DATA_DIR` | `/data` | Path to data directory inside container (fixed) |
| `DATABASE_URL` | `sqlite:////data/job_applications.db` | Database connection string |
| `PYTHONUNBUFFERED` | `1` | Python output buffering disabled |

---

## Common Scenarios

### Scenario 1: Multiple Users on Same Machine

Each user has their own data directory:

```bash
# User 1
DATA_PATH=/home/user1/my-job-search docker-compose up -d

# User 2 (use different port)
DATA_PATH=/home/user2/my-job-search HOST_PORT=8001 docker-compose up -d
```

### Scenario 2: Network Storage / Cloud Sync

Use data directory on synced storage:

```bash
# Dropbox
DATA_PATH=~/Dropbox/JobSearch docker-compose up -d

# OneDrive
DATA_PATH=~/OneDrive/JobSearch docker-compose up -d

# NAS
DATA_PATH=/mnt/nas/JobSearch docker-compose up -d
```

**⚠️ Warning:** Ensure only one container accesses the database at a time to avoid corruption.

### Scenario 3: Development vs Production Data

Separate data directories for testing:

```bash
# Production
DATA_PATH=~/my-job-search docker-compose up -d

# Development/Testing
DATA_PATH=~/my-job-search-test docker-compose -f docker-compose.test.yml up -d
```

### Scenario 4: Backup and Restore

```bash
# Backup
tar -czf job-search-backup-$(date +%Y%m%d).tar.gz $DATA_PATH

# Restore
tar -xzf job-search-backup-20260318.tar.gz -C /path/to/restore/
DATA_PATH=/path/to/restore/my-job-search docker-compose up -d
```

---

## Scripts and Data Directory

All scripts respect the `DATA_DIR` environment variable inside the container:

```bash
# Inside container, DATA_DIR is always /data
docker-compose exec job-tracker bash

# Scripts use DATA_DIR automatically
./scripts/create_application.sh Company JobTitle
# Creates: /data/applications/Company_JobTitle/

# Check environment
echo $DATA_DIR
# Output: /data
```

### Script Behavior

| Script | Data Directory Usage |
|--------|---------------------|
| `create_application.sh` | Creates `${DATA_DIR}/applications/Company_JobTitle/` |
| `compile_application.sh` | Looks for apps in `${DATA_DIR}/applications/` |
| `sync_applications.py` | Syncs `${DATA_DIR}/applications/` to database |
| `customize_application.sh` | Reads from `${DATA_DIR}/applications/` |

---

## Troubleshooting

### Problem: "Directory does not exist"

**Symptom:** Error when running scripts or starting container

**Solutions:**
1. Check `DATA_PATH` is set correctly:
   ```bash
   echo $DATA_PATH
   ```

2. Verify directory exists on host:
   ```bash
   ls -la $DATA_PATH
   ```

3. Recreate if needed:
   ```bash
   mkdir -p $DATA_PATH/applications
   ```

### Problem: "Permission denied"

**Symptom:** Cannot write to data directory

**Solutions:**
1. Check directory permissions:
   ```bash
   ls -ld $DATA_PATH
   ```

2. Ensure your user owns the directory:
   ```bash
   sudo chown -R $USER:$USER $DATA_PATH
   ```

3. Check Docker volume mount permissions:
   ```bash
   docker-compose exec job-tracker ls -la /data
   ```

### Problem: "Database is locked"

**Symptom:** SQLite database errors

**Causes:**
- Multiple containers accessing same data directory
- Network storage latency (NFS, SMB)
- File sync conflicts (Dropbox, OneDrive)

**Solutions:**
1. Ensure only one container is running:
   ```bash
   docker ps | grep job-tracker
   ```

2. Stop all containers:
   ```bash
   docker-compose down
   ```

3. For network storage, use local database:
   - Keep data directory on network storage
   - But override DATABASE_URL to local disk

### Problem: "Different data directory in container"

**Symptom:** Scripts work differently inside vs outside container

**Explanation:** 
- **Outside container:** Use `DATA_PATH` (host path)
- **Inside container:** Use `DATA_DIR` (always `/data`)

**Example:**
```bash
# On host
export DATA_PATH=~/my-job-search
ls $DATA_PATH/applications

# Inside container
docker-compose exec job-tracker bash
ls $DATA_DIR/applications  # Same files, different path
```

---

## Best Practices

### 1. Use Absolute Paths
```bash
# Good
DATA_PATH=/home/user/my-job-search

# Avoid relative paths (context-dependent)
DATA_PATH=../my-job-search
```

### 2. Version Control Data Directory Separately
```bash
# In your data directory
cd $DATA_PATH
git init
git remote add origin git@github.com:yourname/my-job-search-private.git
git add .
git commit -m "Initial job search data"
git push
```

### 3. Keep Data Directory Private
- Use private git repository
- Don't share data directory path publicly
- Exclude from cloud sharing if containing sensitive info

### 4. Regular Backups
```bash
# Weekly backup script
#!/bin/bash
BACKUP_DIR=~/backups/job-search
mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/backup-$(date +%Y%m%d).tar.gz $DATA_PATH
```

### 5. Consistent Naming
Use consistent directory names across machines:
```bash
# Same path on all machines
DATA_PATH=~/my-job-search
```

---

## Migration Guide

### Moving Data to New Location

```bash
# Stop container
docker-compose down

# Move data
mv $DATA_PATH /new/location/my-job-search

# Update configuration
export DATA_PATH=/new/location/my-job-search
# Or update .env file

# Start container
docker-compose up -d
```

### Switching Between Data Directories

```bash
# Current job search
DATA_PATH=~/job-search-2026 docker-compose up -d

# Stop and switch to archived search
docker-compose down
DATA_PATH=~/job-search-2025 docker-compose up -d
```

---

## Security Considerations

### Sensitive Data
Your data directory contains:
- Personal information (resume, contact details)
- Salary expectations and offers
- Company contacts and communications
- Interview notes

### Recommendations
1. **Encryption at rest** (if on cloud storage)
2. **Private git repository** for version control
3. **Restrict file permissions**:
   ```bash
   chmod 700 $DATA_PATH
   ```
4. **Secure backups** (encrypted, access-controlled)
5. **Don't share DATA_PATH publicly**

---

## Summary

✅ **Flexible:** Data directory can be anywhere  
✅ **Configurable:** Via environment variable or .env file  
✅ **Default:** Works out-of-box with sensible defaults  
✅ **Documented:** All scripts respect DATA_DIR  
✅ **Secure:** Keeps personal data separate from code

**Default setup just works:**
```bash
docker-compose up -d
# Uses ../my-job-search-2026 automatically
```

**Custom setup is easy:**
```bash
DATA_PATH=/my/custom/path docker-compose up -d
```

---

*See also: [README.md](../README.md), [PROJECT_CONTEXT.md](../PROJECT_CONTEXT.md)*
