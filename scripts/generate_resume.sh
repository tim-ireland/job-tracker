#!/bin/bash
# Script to generate PDF from LaTeX resume

TEMPLATES_DIR="/Users/tim/Development/my-job-search-2026/templates"

# Function to generate a resume
generate_resume() {
    local template=$1
    echo "Generating ${template}.pdf..."
    pdflatex -interaction=nonstopmode "${template}.tex" > /dev/null
    pdflatex -interaction=nonstopmode "${template}.tex" > /dev/null
    echo "✓ ${template}.pdf generated"
}

# Function to generate a cover letter
generate_cover_letter() {
    local template=$1
    echo "Generating ${template}_cover_letter.pdf..."
    pdflatex -interaction=nonstopmode "${template}_cover_letter.tex" > /dev/null
    pdflatex -interaction=nonstopmode "${template}_cover_letter.tex" > /dev/null
    echo "✓ ${template}_cover_letter.pdf generated"
}

# Parse flags
GENERATE_BASE=false
GENERATE_MANAGER=false
GENERATE_DIRECTOR=false
GENERATE_DEVELOPER=false

if [ $# -eq 0 ]; then
    # No arguments - generate all
    GENERATE_BASE=true
    GENERATE_MANAGER=true
    GENERATE_DIRECTOR=true
    GENERATE_DEVELOPER=true
else
    # Process flags
    while [ $# -gt 0 ]; do
        case "$1" in
            base)
                GENERATE_BASE=true
                ;;
            manager)
                GENERATE_MANAGER=true
                ;;
            director)
                GENERATE_DIRECTOR=true
                ;;
            developer)
                GENERATE_DEVELOPER=true
                ;;
            *)
                echo "Unknown option: $1"
                echo "Usage: $0 [base] [manager] [director] [developer]"
                echo "  No arguments generates all resumes"
                exit 1
                ;;
        esac
        shift
    done
fi

cd "$TEMPLATES_DIR"

# Generate requested resumes and cover letters
if [ "$GENERATE_BASE" = true ]; then
    generate_resume "base_master_resume"
    generate_cover_letter "base_master"
fi

if [ "$GENERATE_MANAGER" = true ]; then
    generate_resume "manager_resume"
    generate_cover_letter "manager"
fi

if [ "$GENERATE_DIRECTOR" = true ]; then
    generate_resume "director_resume"
    generate_cover_letter "director"
fi

if [ "$GENERATE_DEVELOPER" = true ]; then
    generate_resume "senior_engineer_resume"
    generate_cover_letter "senior_engineer"
fi

# Clean up auxiliary files
rm -f *.aux *.log *.out

echo ""
echo "Done! Resumes and cover letters generated in: templates/"
