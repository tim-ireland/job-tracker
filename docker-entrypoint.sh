#!/bin/bash
set -e

# Initialize data directory if empty
if [ ! -f "/data/.initialized" ]; then
    echo "🚀 First-time setup detected. Initializing data directory..."
    
    # Create directory structure
    mkdir -p /data/applications
    mkdir -p /data/source_material
    mkdir -p /data/custom_templates
    
    # Create example application
    mkdir -p /data/applications/Example_Company_Software_Engineer
    cat > /data/applications/Example_Company_Software_Engineer/job_description.txt << 'EOF'
Software Engineer Position

We are looking for a talented software engineer to join our team...

Requirements:
- 3+ years of experience
- Python, JavaScript
- Cloud platforms (AWS/GCP/Azure)
EOF

    cat > /data/applications/Example_Company_Software_Engineer/config.txt << 'EOF'
template: base
priority: P3
status: Pipeline
EOF

    # Create README in applications directory
    cat > /data/applications/README.md << 'EOF'
# Job Applications

This directory contains your job applications. Each application should be in its own directory.

## Structure

```
Company_JobTitle/
  job_description.txt     # The job posting
  config.txt              # Configuration (template, priority, status)
  resume.tex              # Customized resume (generated)
  resume.pdf              # PDF output
  cover_letter.tex        # Customized cover letter (generated)
  cover_letter.pdf        # PDF output
```

## Creating a New Application

From the host machine:
```bash
docker-compose exec job-tracker python scripts/create_application.sh "Company Name" "Job Title"
```

Or manually create the directory and files.
EOF

    # Create example source material
    cat > /data/source_material/README.md << 'EOF'
# Source Material

This directory contains your personal resume content that will be used to generate customized resumes.

Add your:
- experience.tex - Work experience
- skills.tex - Technical skills
- education.tex - Education background
- projects.tex - Notable projects

These files will be included in the generated resumes.
EOF

    # Create config file
    cat > /data/config.env << 'EOF'
# Job Search Toolkit Configuration

# Paths (relative to /data inside container)
APPLICATIONS_DIR=/data/applications
SOURCE_MATERIAL_DIR=/data/source_material
TEMPLATES_DIR=/app/templates
CUSTOM_TEMPLATES_DIR=/data/custom_templates

# Database
DATABASE_URL=sqlite:////data/job_applications.db
EOF

    # Mark as initialized
    touch /data/.initialized
    echo "✅ Data directory initialized successfully!"
else
    echo "✅ Using existing data directory"
fi

# Execute the main command
exec "$@"
