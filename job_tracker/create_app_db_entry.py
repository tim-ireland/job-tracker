#!/usr/bin/env python3
"""
Helper script to create database entries when creating a new application.
Called by create_application.sh to sync folder structure with database.
"""
import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from job_tracker.database import SessionLocal, init_db
from job_tracker.crud import get_company_by_name, create_company, create_application
from job_tracker.models import CompanyCreate, ApplicationCreate


def main():
    parser = argparse.ArgumentParser(description='Create database entries for new job application')
    parser.add_argument('company', help='Company name')
    parser.add_argument('role', help='Job title/role')
    parser.add_argument('dir_name', help='Application directory name')
    parser.add_argument('--job-url', help='Job posting URL')
    parser.add_argument('--location', help='Job location')
    parser.add_argument('--priority', default='P4', help='Priority (P1-P4)')
    parser.add_argument('--status', default='Pipeline', help='Initial status')
    parser.add_argument('--remote-policy', help='Remote work policy')
    parser.add_argument('--salary-range', help='Salary range')
    
    args = parser.parse_args()
    
    try:
        db = SessionLocal()
        
        # Get or create company
        company = get_company_by_name(db, args.company)
        if not company:
            company_data = CompanyCreate(name=args.company)
            company = create_company(db, company_data)
        
        # Create application
        app_data = ApplicationCreate(
            company_id=company.id,
            role=args.role,
            priority=args.priority,
            status=args.status,
            job_url=args.job_url,
            location=args.location,
            remote_policy=args.remote_policy,
            salary_range=args.salary_range,
            resume_filename=f"{args.dir_name}/resume.pdf",
            cover_letter_filename=f"{args.dir_name}/cover_letter.pdf"
        )
        
        application = create_application(db, app_data)
        
        # Output for shell script to capture
        print(f"SUCCESS|{company.id}|{application.id}")
        
        db.close()
        return 0
        
    except Exception as e:
        print(f"ERROR|{str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
