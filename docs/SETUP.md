# Setup Guide

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/job-search-toolkit.git
cd job-search-toolkit
```

### 2. Set Up Your Personal Data Directory

Create a separate directory for your personal job search data:

```bash
# Create directory outside the project
cd ..
mkdir my-job-search-2026

# Initialize as a private git repository (optional but recommended)
cd my-job-search-2026
git init
```

### 3. Start the Application

```bash
cd job-search-toolkit
docker-compose up -d
```

The first time you run this, it will:
- Build the Docker image (may take a few minutes)
- Initialize your data directory structure
- Create example files
- Start the web server

### 4. Access the Application

Open your browser to: **http://localhost:8000**

## Directory Structure After Setup

```
Development/
├── job-search-toolkit/       # Public repo (this project)
│   ├── .git/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── job_tracker/          # Web app code
│   ├── templates/            # LaTeX templates
│   └── scripts/              # Helper scripts
│
└── my-job-search-2026/       # Private repo (your data)
    ├── .git/                 # Your private git
    ├── applications/         # Job applications
    ├── source_material/      # Your resume content
    └── job_applications.db   # Database
```

## Configuration

### Using a Different Data Directory

By default, docker-compose looks for `../my-job-search-2026`. To use a different path:

**Option 1: Set environment variable**
```bash
export DATA_PATH=/path/to/your/data
docker-compose up -d
```

**Option 2: Edit docker-compose.yml**
```yaml
volumes:
  - /absolute/path/to/your/data:/data
```

### Environment Variables

The application supports these environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `DATA_DIR` | `/data` | Path to data directory |
| `DATABASE_URL` | `sqlite:///data/job_applications.db` | Database connection |
| `TEMPLATES_DIR` | `/app/templates` | Path to LaTeX templates |

## Working with Files

### Editing Resume/Cover Letters

Your application files are accessible on your host filesystem:

```bash
# Edit with your favorite editor
code my-job-search-2026/applications/Company_Role/resume.tex

# Compile to PDF inside Docker
docker-compose exec job-tracker bash
cd /data/applications/Company_Role
pdflatex resume.tex
exit
```

The PDF will appear in your local filesystem immediately!

### Creating Applications

**Via Web UI:**
1. Click "Add Application" 
2. Fill in company and role details
3. Save

**Via Command Line:**
```bash
docker-compose exec job-tracker python scripts/create_application.sh "Company Name" "Job Title"
```

**Manually:**
1. Create directory: `my-job-search-2026/applications/Company_Role/`
2. Add `job_description.txt`
3. Add `config.txt`
4. Run sync: `docker-compose exec job-tracker python scripts/sync_applications.py`

## Managing Your Private Data

### Initialize Git Tracking

```bash
cd my-job-search-2026
git add .
git commit -m "Initial job search data"
```

### Create Private GitHub Repo

```bash
# Create repo on GitHub (make it PRIVATE!)
git remote add origin git@github.com:yourusername/my-job-search-2026.git
git push -u origin main
```

### Regular Workflow

```bash
# After making changes
git add .
git commit -m "Updated applications"
git push
```

## Docker Commands

### View Logs
```bash
docker-compose logs -f
```

### Stop Application
```bash
docker-compose down
```

### Restart Application
```bash
docker-compose restart
```

### Rebuild After Code Changes
```bash
docker-compose up -d --build
```

### Execute Commands Inside Container
```bash
docker-compose exec job-tracker bash
```

### Sync Applications
```bash
docker-compose exec job-tracker python scripts/sync_applications.py
```

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, edit `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"  # Use 8080 on host
```

### Permission Issues
If you get permission errors on mounted volumes:
```bash
# Check ownership
ls -la ../my-job-search-2026

# Fix if needed (Linux)
sudo chown -R $USER:$USER ../my-job-search-2026
```

### Database Locked
If you get "database is locked" errors:
```bash
# Stop any other processes accessing the DB
docker-compose restart
```

### LaTeX Compilation Fails
Make sure your `.tex` files are valid LaTeX. Check logs:
```bash
docker-compose exec job-tracker bash
cd /data/applications/Company_Role
pdflatex resume.tex
# Check the .log file for errors
```

## Backup

### Backup Your Data
```bash
# Your data is in my-job-search-2026/
tar -czf job-search-backup-$(date +%Y%m%d).tar.gz my-job-search-2026/
```

### Restore from Backup
```bash
tar -xzf job-search-backup-20260312.tar.gz
```

## Migrating from Existing Setup

If you have an existing non-Docker setup:

1. Copy your data to the new structure:
   ```bash
   cp -r old-setup/applications my-job-search-2026/
   cp -r old-setup/source_material my-job-search-2026/
   cp old-setup/job_applications.db my-job-search-2026/
   ```

2. Start Docker:
   ```bash
   cd job-search-toolkit
   docker-compose up -d
   ```

3. Your data will be preserved and used automatically!

## Next Steps

- [Contributing Guide](../CONTRIBUTING.md)
- [API Documentation](http://localhost:8000/docs)
- [Template Customization](TEMPLATES.md)
