#!/bin/bash
# Script to prepare customization of resume and cover letter for a specific job

# Container detection - warn if running outside container
if [ ! -f "/.dockerenv" ] && [ "${FORCE_RUN:-0}" != "1" ]; then
    echo "⚠️  WARNING: This script should be run inside the Docker container"
    echo ""
    echo "Recommended: Use the wrapper script:"
    echo "  ./job-tracker customize <application_directory_name>"
    echo ""
    echo "Or run in container:"
    echo "  docker exec -it job-search-tracker scripts/$(basename $0) $*"
    echo ""
    echo "To force run anyway: FORCE_RUN=1 $0 $*"
    echo ""
    exit 1
fi

if [ $# -lt 1 ]; then
    echo "Usage: $0 <application_directory_name>"
    echo ""
    echo "Example: $0 Google_Senior_Engineer"
    exit 1
fi

DIR_NAME=$1
DATA_DIR="${DATA_DIR:-.}"
APP_DIR="${DATA_DIR}/applications/${DIR_NAME}"

if [ ! -d "$APP_DIR" ]; then
    echo "Error: Directory $APP_DIR does not exist"
    echo "Run ./create_application.sh first to create the application directory"
    exit 1
fi

if [ ! -f "$APP_DIR/job_description.txt" ]; then
    echo "Error: $APP_DIR/job_description.txt not found"
    exit 1
fi

# Check if job description has been filled out
if grep -q "# Paste the job description here" "$APP_DIR/job_description.txt"; then
    echo "⚠️  Warning: job_description.txt appears to contain placeholder text"
    echo "   Please fill it out with the actual job description before customizing."
    exit 1
fi

echo "=========================================="
echo "Job Application Customization Helper"
echo "=========================================="
echo ""
echo "Application: $DIR_NAME"
echo "Location: $APP_DIR"
echo ""
echo "This script will help you customize the resume and cover letter."
echo ""
echo "--- Job Description Preview (first 20 lines) ---"
head -20 "$APP_DIR/job_description.txt"
echo ""
echo "--- Configuration ---"
cat "$APP_DIR/config.txt"
echo ""
echo "=========================================="
echo ""
echo "NEXT STEPS:"
echo ""
echo "1. Review the job description above to ensure it's complete"
echo ""
echo "2. Ask GitHub Copilot to customize your documents with a prompt like:"
echo ""
echo "   \"Please analyze the job description in $APP_DIR/job_description.txt"
echo "   and customize the resume and cover letter in $APP_DIR/ to highlight"
echo "   relevant experience, match keywords, and align with the company's needs.\""
echo ""
echo "3. After customization, generate PDFs:"
echo "   cd $APP_DIR"
echo "   pdflatex resume.tex && pdflatex resume.tex"
echo "   pdflatex cover_letter.tex && pdflatex cover_letter.tex"
echo ""
echo "4. Review the generated PDFs and iterate as needed"
echo ""
echo "=========================================="
