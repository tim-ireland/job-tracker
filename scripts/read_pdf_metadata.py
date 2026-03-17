#!/usr/bin/env python3
"""
Read and display metadata from PDF files.
Usage: python3 read_pdf_metadata.py <pdf_file>
"""
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    print("Error: pypdf library not installed")
    print("Install with: pip install pypdf")
    sys.exit(1)


def read_pdf_metadata(pdf_path):
    """Read and display PDF metadata."""
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        return 1
    
    try:
        reader = PdfReader(pdf_path)
        metadata = reader.metadata
        
        if not metadata:
            print(f"No metadata found in {pdf_path.name}")
            return 0
        
        print(f"\nMetadata for: {pdf_path.name}")
        print("=" * 60)
        
        # Display all metadata fields
        for key, value in metadata.items():
            # Remove leading slash from key for display
            display_key = key[1:] if key.startswith('/') else key
            print(f"{display_key:25} : {value}")
        
        print("=" * 60)
        return 0
        
    except Exception as e:
        print(f"Error reading PDF: {e}", file=sys.stderr)
        return 1


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 read_pdf_metadata.py <pdf_file>")
        return 1
    
    return read_pdf_metadata(sys.argv[1])


if __name__ == "__main__":
    sys.exit(main())
