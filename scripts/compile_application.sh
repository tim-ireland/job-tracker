#!/bin/bash
# Script to compile resume and cover letter PDFs for an application

if [ $# -lt 1 ]; then
    echo "Usage: $0 <application_directory_name>"
    echo ""
    echo "Example: $0 Google_Senior_Engineer"
    exit 1
fi

DIR_NAME=$1
APP_DIR="applications/${DIR_NAME}"

if [ ! -d "$APP_DIR" ]; then
    echo "Error: Directory $APP_DIR does not exist"
    exit 1
fi

cd "$APP_DIR" || exit 1

echo "Compiling documents in $APP_DIR..."
echo ""

# Compile resume
if [ -f "resume.tex" ]; then
    echo "📄 Compiling resume..."
    pdflatex -interaction=nonstopmode resume.tex > /dev/null
    pdflatex -interaction=nonstopmode resume.tex > /dev/null
    if [ -f "resume.pdf" ]; then
        echo "   ✓ resume.pdf generated"
    else
        echo "   ✗ Failed to generate resume.pdf"
    fi
else
    echo "   ⚠️  resume.tex not found"
fi

echo ""

# Compile cover letter
if [ -f "cover_letter.tex" ]; then
    echo "📝 Compiling cover letter..."
    pdflatex -interaction=nonstopmode cover_letter.tex > /dev/null
    pdflatex -interaction=nonstopmode cover_letter.tex > /dev/null
    if [ -f "cover_letter.pdf" ]; then
        echo "   ✓ cover_letter.pdf generated"
    else
        echo "   ✗ Failed to generate cover_letter.pdf"
    fi
else
    echo "   ⚠️  cover_letter.tex not found"
fi

# Clean up auxiliary files
rm -f *.aux *.log *.out

echo ""
echo "Done! PDFs are in: $APP_DIR"
echo ""

# List generated PDFs
if [ -f "resume.pdf" ] || [ -f "cover_letter.pdf" ]; then
    echo "Generated files:"
    ls -lh *.pdf 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
fi
