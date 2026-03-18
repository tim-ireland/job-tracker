#!/bin/bash
# Script to list all job applications and their status

# Container detection - warn if running outside container
if [ ! -f "/.dockerenv" ] && [ "${FORCE_RUN:-0}" != "1" ]; then
    echo "⚠️  WARNING: This script should be run inside the Docker container"
    echo ""
    echo "Or run in container:"
    echo "  docker exec -it job-search-tracker scripts/$(basename $0)"
    echo ""
    echo "To force run anyway: FORCE_RUN=1 $0 $*"
    echo ""
    exit 1
fi

DATA_DIR="${DATA_DIR:-.}"
APPS_DIR="${DATA_DIR}/applications"

if [ ! -d "$APPS_DIR" ]; then
    echo "No applications directory found"
    exit 1
fi

echo "=========================================="
echo "Job Applications Summary"
echo "=========================================="
echo ""

# Count applications
APP_COUNT=$(find "$APPS_DIR" -mindepth 1 -maxdepth 1 -type d ! -name ".*" | wc -l | tr -d ' ')

if [ "$APP_COUNT" -eq 0 ]; then
    echo "No applications found."
    echo ""
    echo "Create a new application with:"
    echo "  ./create_application.sh <Company> <Job_Title> [template_type]"
    exit 0
fi

echo "Total applications: $APP_COUNT"
echo ""

# List each application
for app_dir in "$APPS_DIR"/*/; do
    if [ ! -d "$app_dir" ]; then
        continue
    fi
    
    app_name=$(basename "$app_dir")
    
    echo "📁 $app_name"
    
    # Show config if exists
    if [ -f "$app_dir/config.txt" ]; then
        grep -E "^(Company|Job Title|Template Type|Status):" "$app_dir/config.txt" | sed 's/^/   /'
    fi
    
    # Show file status
    echo -n "   Files: "
    has_resume_tex=$( [ -f "$app_dir/resume.tex" ] && echo "✓" || echo "✗" )
    has_resume_pdf=$( [ -f "$app_dir/resume.pdf" ] && echo "✓" || echo "✗" )
    has_cover_tex=$( [ -f "$app_dir/cover_letter.tex" ] && echo "✓" || echo "✗" )
    has_cover_pdf=$( [ -f "$app_dir/cover_letter.pdf" ] && echo "✓" || echo "✗" )
    
    echo "resume.tex[$has_resume_tex] resume.pdf[$has_resume_pdf] cover_letter.tex[$has_cover_tex] cover_letter.pdf[$has_cover_pdf]"
    
    echo ""
done

echo "=========================================="
echo ""
echo "Commands:"
echo "  ./create_application.sh <Company> <Job_Title> [type]  - Create new"
echo "  ./customize_application.sh <app_name>                 - Prepare for customization"
echo "  ./compile_application.sh <app_name>                   - Generate PDFs"
