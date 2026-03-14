#!/usr/bin/env python3
"""
Sync applications from filesystem to database.
Scans the applications directory and adds any missing entries to the database.
"""
import sys
import os
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from job_tracker.database import SessionLocal, init_db
from job_tracker.crud import get_company_by_name, create_company, create_application, get_applications
from job_tracker.models import CompanyCreate, ApplicationCreate


def parse_directory_name(dir_name):
    """
    Parse directory name to extract company and role.
    Format: Company_Role_With_Underscores
    """
    parts = dir_name.split('_')
    if len(parts) < 2:
        return None, None
    
    # First part is company, rest is role
    company = parts[0]
    role = ' '.join(parts[1:]).replace('_', ' ')
    
    return company, role


def get_config_value(config_path, key):
    """Extract a value from config.txt if it exists."""
    if not config_path.exists():
        return None
    
    try:
        with open(config_path, 'r') as f:
            for line in f:
                if line.startswith(f'{key}:'):
                    return line.split(':', 1)[1].strip()
    except Exception:
        pass
    return None


def scan_applications_directory(applications_dir):
    """Scan the applications directory and return list of application data."""
    apps = []
    
    for dir_path in applications_dir.iterdir():
        if not dir_path.is_dir() or dir_path.name.startswith('.'):
            continue
        
        # Parse directory name
        company_name, role = parse_directory_name(dir_path.name)
        if not company_name or not role:
            print(f"⚠️  Skipping {dir_path.name} - couldn't parse name")
            continue
        
        # Check if it has key files
        has_job_desc = (dir_path / 'job_description.txt').exists()
        has_resume = (dir_path / 'resume.tex').exists() or (dir_path / 'resume.pdf').exists()
        
        if not has_job_desc and not has_resume:
            print(f"⚠️  Skipping {dir_path.name} - no job description or resume found")
            continue
        
        # Read config if available
        config_path = dir_path / 'config.txt'
        priority = get_config_value(config_path, 'priority') or 'P3'
        status = get_config_value(config_path, 'status') or 'Pipeline'
        location = get_config_value(config_path, 'location')
        remote_policy = get_config_value(config_path, 'remote_policy')
        salary_range = get_config_value(config_path, 'salary_range')
        job_url = get_config_value(config_path, 'job_url')
        
        # Set filenames - look for any PDF files
        resume_filename = None
        cover_letter_filename = None
        
        # Look for resume PDF (various naming patterns)
        for pdf in dir_path.glob('*.pdf'):
            if 'resume' in pdf.name.lower():
                resume_filename = f"{dir_path.name}/{pdf.name}"
            elif 'cover' in pdf.name.lower():
                cover_letter_filename = f"{dir_path.name}/{pdf.name}"
        
        apps.append({
            'dir_name': dir_path.name,
            'company': company_name,
            'role': role,
            'priority': priority,
            'status': status,
            'location': location,
            'remote_policy': remote_policy,
            'salary_range': salary_range,
            'job_url': job_url,
            'resume_filename': resume_filename,
            'cover_letter_filename': cover_letter_filename
        })
    
    return apps


def sync_to_database(db: Session, filesystem_apps):
    """Add missing applications to database and update existing ones with PDF info."""
    # Get existing applications
    db_apps = get_applications(db)
    
    # Create a dict of existing (company, role) -> app for lookup
    existing = {(app.company.name, app.role): app for app in db_apps}
    
    added_count = 0
    updated_count = 0
    skipped_count = 0
    
    for app_data in filesystem_apps:
        company_name = app_data['company']
        role = app_data['role']
        
        # Check if already exists
        if (company_name, role) in existing:
            existing_app = existing[(company_name, role)]
            
            # Update PDF filenames if they're missing but we found them
            needs_update = False
            if not existing_app.resume_filename and app_data['resume_filename']:
                existing_app.resume_filename = app_data['resume_filename']
                needs_update = True
            if not existing_app.cover_letter_filename and app_data['cover_letter_filename']:
                existing_app.cover_letter_filename = app_data['cover_letter_filename']
                needs_update = True
            
            if needs_update:
                db.commit()
                print(f"✓ Updated PDFs: {company_name} - {role}")
                updated_count += 1
            else:
                print(f"✓ Already exists: {company_name} - {role}")
                skipped_count += 1
            continue
        
        try:
            # Get or create company
            company = get_company_by_name(db, company_name)
            if not company:
                company_create = CompanyCreate(name=company_name)
                company = create_company(db, company_create)
                print(f"  + Created company: {company_name}")
            
            # Create application
            application_create = ApplicationCreate(
                company_id=company.id,
                role=role,
                priority=app_data['priority'],
                status=app_data['status'],
                location=app_data['location'],
                remote_policy=app_data['remote_policy'],
                salary_range=app_data['salary_range'],
                job_url=app_data['job_url'],
                resume_filename=app_data['resume_filename'],
                cover_letter_filename=app_data['cover_letter_filename']
            )
            
            application = create_application(db, application_create)
            print(f"✓ Added: {company_name} - {role}")
            added_count += 1
            
        except Exception as e:
            print(f"✗ Error adding {company_name} - {role}: {e}")
    
    return added_count, updated_count, skipped_count


def main():
    print("🔍 Scanning applications directory...\n")
    
    # Initialize database
    init_db()
    
    # Get applications directory from environment or default
    data_dir = os.environ.get('DATA_DIR', '.')
    applications_dir = Path(data_dir) / 'applications'
    if not applications_dir.exists():
        print("❌ Applications directory not found!")
        print(f"   Looking for: {applications_dir}")
        return 1
    
    # Scan filesystem
    filesystem_apps = scan_applications_directory(applications_dir)
    print(f"\n📁 Found {len(filesystem_apps)} applications in filesystem\n")
    
    # Sync to database
    db = SessionLocal()
    try:
        added, updated, skipped = sync_to_database(db, filesystem_apps)
        
        print(f"\n{'='*50}")
        print(f"✅ Sync complete!")
        print(f"   Added: {added}")
        print(f"   Updated: {updated}")
        print(f"   Skipped (already exists): {skipped}")
        print(f"   Total: {added + updated + skipped}")
        print(f"{'='*50}")
        
    finally:
        db.close()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
