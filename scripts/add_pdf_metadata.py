#!/usr/bin/env python3
"""
Add metadata to PDF files, including resume version hash and other custom fields.
Usage: python3 add_pdf_metadata.py <pdf_file> [options]
"""
import sys
import argparse
import hashlib
from pathlib import Path
from datetime import datetime

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("Error: pypdf library not installed")
    print("Install with: pip install pypdf")
    sys.exit(1)


def calculate_file_hash(file_path):
    """Calculate SHA256 hash of file content."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def add_metadata_to_pdf(pdf_path, metadata):
    """Add custom metadata to a PDF file."""
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    # Read the PDF
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    
    # Copy all pages
    for page in reader.pages:
        writer.add_page(page)
    
    # Copy existing metadata and add new fields
    if reader.metadata:
        for key, value in reader.metadata.items():
            writer.add_metadata({key: value})
    
    # Add custom metadata
    writer.add_metadata(metadata)
    
    # Write to temporary file first
    temp_path = pdf_path.with_suffix('.pdf.tmp')
    with open(temp_path, 'wb') as output_file:
        writer.write(output_file)
    
    # Replace original file
    temp_path.replace(pdf_path)
    
    return True


def main():
    parser = argparse.ArgumentParser(description='Add metadata to PDF files')
    parser.add_argument('pdf_file', help='Path to PDF file')
    parser.add_argument('--resume-version', help='Resume version identifier')
    parser.add_argument('--source-tex', help='Path to source .tex file (for hash calculation)')
    parser.add_argument('--company', help='Company name')
    parser.add_argument('--role', help='Job role')
    parser.add_argument('--application-id', help='Application ID from database')
    parser.add_argument('--custom-field', action='append', nargs=2, metavar=('KEY', 'VALUE'),
                       help='Add custom metadata field (can be used multiple times)')
    
    args = parser.parse_args()
    
    metadata = {}
    
    # Standard metadata
    metadata['/Producer'] = 'Job Search Toolkit'
    metadata['/CreationDate'] = datetime.now().strftime('D:%Y%m%d%H%M%S')
    
    # Resume version hash
    if args.source_tex:
        tex_path = Path(args.source_tex)
        if tex_path.exists():
            tex_hash = calculate_file_hash(tex_path)
            metadata['/ResumeSourceHash'] = tex_hash[:16]  # First 16 chars
            if args.resume_version:
                metadata['/ResumeVersion'] = args.resume_version
        else:
            print(f"Warning: Source .tex file not found: {tex_path}")
    
    # Job application info
    if args.company:
        metadata['/Company'] = args.company
    if args.role:
        metadata['/Role'] = args.role
    if args.application_id:
        metadata['/ApplicationID'] = args.application_id
    
    # Custom fields
    if args.custom_field:
        for key, value in args.custom_field:
            if not key.startswith('/'):
                key = '/' + key
            metadata[key] = value
    
    try:
        add_metadata_to_pdf(args.pdf_file, metadata)
        print(f"✓ Metadata added to {args.pdf_file}")
        
        # Display added metadata
        if metadata:
            print("\nAdded metadata:")
            for key, value in metadata.items():
                print(f"  {key}: {value}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
