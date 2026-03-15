#!/bin/bash
# Script to create a new job application directory

if [ $# -lt 2 ]; then
    echo "Usage: $0 <Company_Name> <Job_Title> [template_type] [OPTIONS]"
    echo ""
    echo "Example: $0 Google 'Senior_Engineer' developer"
    echo "         $0 Meta 'Engineering_Manager' manager"
    echo "         $0 Apple 'Staff_Engineer' developer --job-url='https://...' --location='Boston, MA'"
    echo ""
    echo "Template types: base, manager, director, developer (default: base)"
    echo ""
    echo "Optional flags (passed to database):"
    echo "  --job-url=<url>           Job posting URL"
    echo "  --location=<location>     Job location"
    echo "  --priority=<P1-P4>        Priority level (default: P4)"
    echo "  --status=<status>         Initial status (default: Pipeline)"
    echo "  --remote-policy=<policy>  Remote work policy"
    echo "  --salary-range=<range>    Salary range"
    exit 1
fi

COMPANY=$1
JOB_TITLE=$2
TEMPLATE=${3:-base}

# Parse optional arguments
DB_ARGS=""
shift 3 2>/dev/null || shift 2
for arg in "$@"; do
    case $arg in
        --job-url=*|--location=*|--priority=*|--status=*|--remote-policy=*|--salary-range=*)
            DB_ARGS="$DB_ARGS $arg"
            ;;
    esac
done

# Sanitize directory name
DIR_NAME="${COMPANY}_${JOB_TITLE}"
DIR_NAME=$(echo "$DIR_NAME" | sed 's/[^a-zA-Z0-9_-]/_/g')

# Determine base directory (Docker or local)
DATA_DIR="${DATA_DIR:-.}"
APP_DIR="${DATA_DIR}/applications/${DIR_NAME}"

if [ -d "$APP_DIR" ]; then
    echo "Error: Directory $APP_DIR already exists"
    exit 1
fi

# Validate template type
case "$TEMPLATE" in
    base|manager|director|developer)
        ;;
    *)
        echo "Error: Invalid template type '$TEMPLATE'"
        echo "Valid options: base, manager, director, developer"
        exit 1
        ;;
esac

# Create directory structure
mkdir -p "$APP_DIR"

# Create config file (will be updated if DB entry succeeds)
cat > "$APP_DIR/config.txt" << EOF
# Application Configuration
Company: $COMPANY
Job Title: $JOB_TITLE
Template Type: $TEMPLATE
Date Created: $(date +%Y-%m-%d)
Status: pending
Company ID: 
Application ID: 
EOF

# Create placeholder job description
cat > "$APP_DIR/job_description.txt" << 'EOF'
# Paste the job description here

## Company Information
[Company background, mission, values]

## Role Description
[Role summary]

## Responsibilities
- [Responsibility 1]
- [Responsibility 2]

## Requirements
- [Requirement 1]
- [Requirement 2]

## Nice to Have
- [Nice to have 1]
- [Nice to have 2]

## Benefits
[Benefits information]
EOF

# Copy base templates
case "$TEMPLATE" in
    base)
        RESUME_TEMPLATE="base_master_resume"
        COVER_TEMPLATE="base_master_cover_letter"
        ;;
    manager)
        RESUME_TEMPLATE="manager_resume"
        COVER_TEMPLATE="manager_cover_letter"
        ;;
    director)
        RESUME_TEMPLATE="director_resume"
        COVER_TEMPLATE="director_cover_letter"
        ;;
    developer)
        RESUME_TEMPLATE="senior_engineer_resume"
        COVER_TEMPLATE="senior_engineer_cover_letter"
        ;;
esac

# Determine templates directory (check custom first, then fallback to default)
if [ -f "${DATA_DIR}/templates/${RESUME_TEMPLATE}.tex" ]; then
    TEMPLATES_DIR="${DATA_DIR}/templates"
elif [ -f "/app/templates/${RESUME_TEMPLATE}.tex" ]; then
    TEMPLATES_DIR="/app/templates"
else
    # Fallback to relative path (for local execution)
    TEMPLATES_DIR="templates"
fi

cp "${TEMPLATES_DIR}/${RESUME_TEMPLATE}.tex" "$APP_DIR/resume.tex"
cp "${TEMPLATES_DIR}/${COVER_TEMPLATE}.tex" "$APP_DIR/cover_letter.tex"

echo "✓ Created application directory: $APP_DIR"

# Try to create database entry
if command -v python3 &> /dev/null; then
    DB_RESULT=$(python3 job_tracker/create_app_db_entry.py "$COMPANY" "$JOB_TITLE" "$DIR_NAME" $DB_ARGS 2>&1)
    
    if [ $? -eq 0 ] && [[ $DB_RESULT == SUCCESS* ]]; then
        # Parse the result: SUCCESS|company_id|application_id
        IFS='|' read -r status company_id app_id <<< "$DB_RESULT"
        
        # Update config with IDs
        sed -i.bak "s/^Company ID:.*/Company ID: $company_id/" "$APP_DIR/config.txt"
        sed -i.bak "s/^Application ID:.*/Application ID: $app_id/" "$APP_DIR/config.txt"
        rm "$APP_DIR/config.txt.bak"
        
        echo "✓ Created database entry (Company ID: $company_id, Application ID: $app_id)"
        echo "  You can view and edit this application in the job tracker UI"
    else
        echo "⚠ Could not create database entry (tracker may not be running)"
        echo "  Continuing with file-based workflow only"
        if [[ $DB_RESULT == ERROR* ]]; then
            echo "  Error: ${DB_RESULT#ERROR|}"
        fi
    fi
else
    echo "⚠ Python3 not found, skipping database entry"
fi

echo ""
echo "Next steps:"
echo "1. Edit $APP_DIR/job_description.txt with the full job posting"
echo "2. Run: ./customize_application.sh $DIR_NAME"
echo "   This will customize the resume and cover letter based on the job description"
echo "3. Review and refine the customized documents"
echo "4. Generate PDFs with: cd $APP_DIR && pdflatex resume.tex && pdflatex cover_letter.tex"
