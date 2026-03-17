"""
FastAPI application for job tracking
"""
from fastapi import FastAPI, Depends, HTTPException, Request, Body, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse, StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pathlib import Path
from pydantic import BaseModel
from datetime import datetime, timedelta
import os
import io
import csv
import shutil

from . import crud, models
from . import database as db_models
from .database import get_db, init_db

init_db()

app = FastAPI(title="Job Application Tracker", version="1.0.0")

app.mount("/static", StaticFiles(directory="job_tracker/static"), name="static")
templates = Jinja2Templates(directory="job_tracker/templates")

# Base directory for applications
DATA_DIR = os.environ.get('DATA_DIR', '.')
APPLICATIONS_DIR = Path(DATA_DIR) / "applications"


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/health")
async def health_check():
    """Health check endpoint for Docker"""
    return {"status": "healthy", "data_dir": DATA_DIR}


@app.get("/api/dashboard", response_model=models.DashboardStats)
def get_dashboard(db: Session = Depends(get_db)):
    return crud.get_dashboard_stats(db)


@app.get("/api/companies", response_model=List[models.Company])
def list_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_companies(db, skip=skip, limit=limit)


@app.get("/api/companies/{company_id}", response_model=models.Company)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = crud.get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@app.post("/api/companies", response_model=models.Company)
def create_company(company: models.CompanyCreate, db: Session = Depends(get_db)):
    existing = crud.get_company_by_name(db, company.name)
    if existing:
        raise HTTPException(status_code=400, detail="Company already exists")
    return crud.create_company(db, company)


@app.put("/api/companies/{company_id}", response_model=models.Company)
def update_company(company_id: int, company: models.CompanyUpdate, db: Session = Depends(get_db)):
    updated = crud.update_company(db, company_id, company)
    if not updated:
        raise HTTPException(status_code=404, detail="Company not found")
    return updated


@app.delete("/api/companies/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    if not crud.delete_company(db, company_id):
        raise HTTPException(status_code=404, detail="Company not found")
    return {"message": "Company deleted"}


@app.get("/api/applications", response_model=List[models.Application])
def list_applications(
    skip: int = 0, 
    limit: int = 100, 
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_applications(db, skip=skip, limit=limit, status=status, priority=priority)


@app.get("/api/applications/{application_id}", response_model=models.Application)
def get_application(application_id: int, db: Session = Depends(get_db)):
    application = crud.get_application(db, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@app.post("/api/applications", response_model=models.Application)
def create_application(application: models.ApplicationCreate, db: Session = Depends(get_db)):
    return crud.create_application(db, application)


@app.put("/api/applications/{application_id}", response_model=models.Application)
def update_application(
    application_id: int, 
    application: models.ApplicationUpdate, 
    db: Session = Depends(get_db)
):
    updated = crud.update_application(db, application_id, application)
    if not updated:
        raise HTTPException(status_code=404, detail="Application not found")
    return updated


@app.delete("/api/applications/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    if not crud.delete_application(db, application_id):
        raise HTTPException(status_code=404, detail="Application not found")
    return {"message": "Application deleted"}


@app.get("/api/contacts", response_model=List[models.Contact])
def list_contacts(company_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_contacts(db, company_id=company_id)


@app.post("/api/contacts", response_model=models.Contact)
def create_contact(contact: models.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)


@app.get("/api/applications/{application_id}/interactions", response_model=List[models.Interaction])
def list_interactions(application_id: int, db: Session = Depends(get_db)):
    return crud.get_interactions(db, application_id)


@app.post("/api/interactions", response_model=models.Interaction)
def create_interaction(interaction: models.InteractionCreate, db: Session = Depends(get_db)):
    return crud.create_interaction(db, interaction)


# Interview endpoints
@app.get("/api/applications/{application_id}/interviews", response_model=List[models.Interview])
def list_interviews(application_id: int, db: Session = Depends(get_db)):
    return crud.get_interviews(db, application_id)


@app.post("/api/interviews", response_model=models.Interview)
def create_interview(interview: models.InterviewCreate, db: Session = Depends(get_db)):
    return crud.create_interview(db, interview)


@app.put("/api/interviews/{interview_id}", response_model=models.Interview)
def update_interview(interview_id: int, interview: models.InterviewUpdate, db: Session = Depends(get_db)):
    updated = crud.update_interview(db, interview_id, interview)
    if not updated:
        raise HTTPException(status_code=404, detail="Interview not found")
    return updated


@app.delete("/api/interviews/{interview_id}")
def delete_interview(interview_id: int, db: Session = Depends(get_db)):
    if not crud.delete_interview(db, interview_id):
        raise HTTPException(status_code=404, detail="Interview not found")
    return {"message": "Interview deleted"}


# Offer endpoints
@app.get("/api/offers", response_model=List[models.Offer])
def list_offers(application_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_offers(db, application_id=application_id)


@app.get("/api/offers/{offer_id}", response_model=models.Offer)
def get_offer(offer_id: int, db: Session = Depends(get_db)):
    offer = crud.get_offer(db, offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer


@app.post("/api/offers", response_model=models.Offer)
def create_offer(offer: models.OfferCreate, db: Session = Depends(get_db)):
    return crud.create_offer(db, offer)


@app.put("/api/offers/{offer_id}", response_model=models.Offer)
def update_offer(offer_id: int, offer: models.OfferUpdate, db: Session = Depends(get_db)):
    updated = crud.update_offer(db, offer_id, offer)
    if not updated:
        raise HTTPException(status_code=404, detail="Offer not found")
    return updated


@app.delete("/api/offers/{offer_id}")
def delete_offer(offer_id: int, db: Session = Depends(get_db)):
    if not crud.delete_offer(db, offer_id):
        raise HTTPException(status_code=404, detail="Offer not found")
    return {"message": "Offer deleted"}


@app.get("/api/offers/compare/all", response_model=models.OfferComparison)
def compare_offers(db: Session = Depends(get_db)):
    return crud.get_offer_comparison(db)


# PDF file endpoints
@app.get("/api/applications/{application_id}/pdfs")
def list_application_pdfs(application_id: int, db: Session = Depends(get_db)):
    """List all PDF files in the application directory"""
    application = crud.get_application(db, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Extract directory name from resume_filename or cover_letter_filename
    dir_name = None
    if application.resume_filename:
        dir_name = Path(application.resume_filename).parent
    elif application.cover_letter_filename:
        dir_name = Path(application.cover_letter_filename).parent
    else:
        # Try to construct directory name from company and role
        company = application.company
        if company:
            dir_name_str = f"{company.name}_{application.role}".replace(' ', '_')
            # Remove special characters that might have been sanitized
            dir_name_str = ''.join(c if c.isalnum() or c in ['_', '-'] else '_' for c in dir_name_str)
            dir_name = Path(dir_name_str)
    
    if not dir_name:
        return {"pdfs": []}
    
    app_dir = APPLICATIONS_DIR / dir_name
    if not app_dir.exists():
        return {"pdfs": []}
    
    # Find all PDF files
    pdfs = []
    for file_path in app_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() == '.pdf' and not file_path.name.startswith('.'):
            pdfs.append({
                "name": file_path.name,
                "path": str(file_path.relative_to(APPLICATIONS_DIR)),
                "size": file_path.stat().st_size,
                "modified": file_path.stat().st_mtime
            })
    
    return {"pdfs": sorted(pdfs, key=lambda x: x["modified"], reverse=True)}


@app.post("/api/applications/{application_id}/upload")
async def upload_application_file(
    application_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a file to an application directory"""
    application = crud.get_application(db, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Determine application directory
    dir_name = None
    if application.resume_filename:
        dir_name = Path(application.resume_filename).parent
    elif application.cover_letter_filename:
        dir_name = Path(application.cover_letter_filename).parent
    else:
        # Create a directory name based on company and role
        company = application.company
        dir_name_str = f"{company.name}_{application.role}".replace(' ', '_')
        dir_name = Path(dir_name_str)
    
    app_dir = APPLICATIONS_DIR / dir_name
    app_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the uploaded file
    file_path = app_dir / file.filename
    
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "success": True,
            "filename": file.filename,
            "path": str(file_path.relative_to(APPLICATIONS_DIR))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")


@app.get("/api/files/pdf/{file_path:path}")
def get_pdf_file(file_path: str):
    """Serve a file from the applications directory"""
    full_path = APPLICATIONS_DIR / file_path
    
    # Security check: ensure the path is within applications directory
    try:
        full_path = full_path.resolve()
        APPLICATIONS_DIR.resolve()
        if not str(full_path).startswith(str(APPLICATIONS_DIR.resolve())):
            raise HTTPException(status_code=403, detail="Access denied")
    except:
        raise HTTPException(status_code=403, detail="Invalid path")
    
    if not full_path.exists() or not full_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Determine media type based on extension
    media_type = "application/octet-stream"
    suffix = full_path.suffix.lower()
    if suffix == '.pdf':
        media_type = "application/pdf"
    elif suffix in ['.doc', '.docx']:
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif suffix == '.txt':
        media_type = "text/plain"
    
    return FileResponse(
        full_path,
        media_type=media_type,
        filename=full_path.name
    )


# Job import endpoints
class ImportJobsRequest(BaseModel):
    urls: str

@app.post("/api/jobs/import-urls")
def import_job_urls(request: ImportJobsRequest, db: Session = Depends(get_db)):
    """Import jobs from LinkedIn URLs"""
    from . import linkedin_parser
    
    jobs = linkedin_parser.parse_job_urls(request.urls)
    
    created_apps = []
    errors = []
    
    for job_data in jobs:
        try:
            existing = db.query(db_models.Application).filter(
                db_models.Application.job_url == job_data['url']
            ).first()
            
            if existing:
                errors.append({
                    'url': job_data['url'],
                    'error': 'Job already exists in tracker'
                })
                continue
            
            company_name = job_data.get('company') or 'Unknown Company'
            company = crud.get_company_by_name(db, company_name)
            
            if not company:
                company_data = models.CompanyCreate(name=company_name)
                company = crud.create_company(db, company_data)
            
            app_data = models.ApplicationCreate(
                company_id=company.id,
                role=job_data.get('title', 'Unknown Role'),
                priority='P3',
                status='Pipeline',
                job_url=job_data['url'],
                location=job_data.get('location'),
                notes=job_data.get('description', '')[:1000] if job_data.get('description') else None
            )
            
            application = crud.create_application(db, app_data)
            created_apps.append({
                'id': application.id,
                'company': company.name,
                'role': application.role,
                'url': application.job_url
            })
            
        except Exception as e:
            errors.append({
                'url': job_data.get('url', 'unknown'),
                'error': str(e)
            })
    
    return {
        'success': len(created_apps),
        'failed': len(errors),
        'created': created_apps,
        'errors': errors
    }


# MA DUA Weekly Activity Report
@app.get("/api/reports/dua-weekly", response_class=PlainTextResponse)
def get_dua_weekly_report(week_start: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Generate Massachusetts DUA weekly activity report
    Week runs Sunday through Saturday
    Format: "Date: Position Pay rate Employer name and address Job ID or person contacted Contact email, website, or phone Result"
    """
    # Parse or calculate week start (Sunday)
    if week_start:
        start_date = datetime.strptime(week_start, '%Y-%m-%d')
    else:
        # Default to previous week starting last Sunday
        today = datetime.now()
        days_since_sunday = (today.weekday() + 1) % 7
        start_date = today - timedelta(days=days_since_sunday + 7)
    
    # Ensure start_date is a Sunday (weekday 6 in Python)
    if start_date.weekday() != 6:
        days_since_sunday = (start_date.weekday() + 1) % 7
        start_date = start_date - timedelta(days=days_since_sunday)
    
    start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + timedelta(days=6, hours=23, minutes=59, seconds=59)
    
    # Get all activity for the week using the new crud function
    activities = crud.get_weekly_activity(db, start_date, end_date)
    
    # Format report
    report_lines = []
    report_lines.append(f"Week starting Sunday {start_date.strftime('%m/%d/%Y')} through Saturday {end_date.strftime('%m/%d/%Y')}:\n")
    
    if not activities:
        report_lines.append("No job search activities recorded for this week.\n")
    else:
        for activity in activities:
            # Date
            date_str = activity['date'].strftime('%m/%d/%Y')
            
            # Position
            position = activity['position']
            
            # Pay rate
            pay_rate = activity['pay_rate']
            
            # Employer name and address
            employer_name = activity['employer_name']
            employer_address = activity['employer_address']
            employer_info = employer_name
            if employer_address:
                employer_info += f" {employer_address}"
            
            # Job ID or person contacted
            job_id = activity['job_id']
            contact_person = activity['contact_person']
            person_or_id = contact_person if contact_person else job_id
            
            # Contact email, website, or phone
            contact_info = activity['contact_email'] if activity['contact_email'] else employer_address
            
            # Result
            result = activity['result']
            
            # Format line per MA DUA requirements
            line = f"{date_str}: {position} {pay_rate} {employer_info} {person_or_id} {contact_info} {result}"
            report_lines.append(line)
    
    return "\n".join(report_lines)


@app.get("/api/reports/dua-weekly-csv")
def get_dua_weekly_report_csv(week_start: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Generate Massachusetts DUA weekly activity report in CSV format
    Week runs Sunday through Saturday
    """
    # Parse or calculate week start (Sunday)
    if week_start:
        start_date = datetime.strptime(week_start, '%Y-%m-%d')
    else:
        # Default to previous week starting last Sunday
        today = datetime.now()
        days_since_sunday = (today.weekday() + 1) % 7
        start_date = today - timedelta(days=days_since_sunday + 7)
    
    # Ensure start_date is a Sunday (weekday 6 in Python)
    if start_date.weekday() != 6:
        days_since_sunday = (start_date.weekday() + 1) % 7
        start_date = start_date - timedelta(days=days_since_sunday)
    
    start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + timedelta(days=6, hours=23, minutes=59, seconds=59)
    
    # Get all activity for the week
    activities = crud.get_weekly_activity(db, start_date, end_date)
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header with week range
    writer.writerow([f"Week starting Sunday {start_date.strftime('%m/%d/%Y')} through Saturday {end_date.strftime('%m/%d/%Y')}"])
    writer.writerow([])  # Empty row
    
    # Write column headers
    writer.writerow(['Date', 'Position', 'Pay Rate', 'Employer Name', 'Employer Address', 
                     'Job ID or Person Contacted', 'Contact Email/Website/Phone', 'Result'])
    
    # Write data
    if not activities:
        writer.writerow(['No job search activities recorded for this week'])
    else:
        for activity in activities:
            writer.writerow([
                activity['date'].strftime('%m/%d/%Y'),
                activity['position'],
                activity['pay_rate'],
                activity['employer_name'],
                activity['employer_address'],
                activity['contact_person'] if activity['contact_person'] else activity['job_id'],
                activity['contact_email'] if activity['contact_email'] else activity['employer_address'],
                activity['result']
            ])
    
    # Return as streaming response
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=dua_weekly_{start_date.strftime('%Y%m%d')}.csv"
        }
    )


@app.get("/api/reports/dua-range", response_class=PlainTextResponse)
def get_dua_range_report(start_date: str, end_date: str, db: Session = Depends(get_db)):
    """
    Generate Massachusetts DUA activity report for a custom date range
    Breaks down by week (Sunday-Saturday)
    
    Parameters:
    - start_date: ISO format YYYY-MM-DD
    - end_date: ISO format YYYY-MM-DD
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    if start > end:
        raise HTTPException(status_code=400, detail="Start date must be before end date")
    
    # Find the Sunday before or on start_date
    days_since_sunday = (start.weekday() + 1) % 7
    week_start = start - timedelta(days=days_since_sunday)
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    
    report_lines = []
    report_lines.append(f"Massachusetts DUA Activity Report")
    report_lines.append(f"Date Range: {start.strftime('%m/%d/%Y')} through {end.strftime('%m/%d/%Y')}")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    total_activities = 0
    
    # Process each week
    current_week_start = week_start
    while current_week_start <= end:
        week_end = current_week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
        
        # Get activities for this week
        activities = crud.get_weekly_activity(db, current_week_start, week_end)
        
        # Only show weeks that overlap with the requested range
        if current_week_start <= end and week_end >= start:
            report_lines.append(f"\nWeek starting Sunday {current_week_start.strftime('%m/%d/%Y')} through Saturday {week_end.strftime('%m/%d/%Y')}:")
            report_lines.append("-" * 80)
            
            if not activities:
                report_lines.append("No job search activities recorded for this week.")
            else:
                week_count = 0
                for activity in activities:
                    # Only include activities within the requested range
                    if start <= activity['date'] <= end:
                        date_str = activity['date'].strftime('%m/%d/%Y')
                        position = activity['position']
                        pay_rate = activity['pay_rate']
                        employer_name = activity['employer_name']
                        employer_address = activity['employer_address']
                        employer_info = employer_name
                        if employer_address:
                            employer_info += f" {employer_address}"
                        
                        person_or_id = activity['contact_person'] if activity['contact_person'] else activity['job_id']
                        contact_info = activity['contact_email'] if activity['contact_email'] else employer_address
                        result = activity['result']
                        
                        line = f"{date_str}: {position} {pay_rate} {employer_info} {person_or_id} {contact_info} {result}"
                        report_lines.append(line)
                        week_count += 1
                        total_activities += 1
                
                if week_count == 0:
                    report_lines.append("No job search activities recorded for this week.")
        
        # Move to next week
        current_week_start += timedelta(days=7)
    
    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append(f"Total activities recorded: {total_activities}")
    
    return "\n".join(report_lines)


@app.get("/api/reports/dua-range-csv")
def get_dua_range_report_csv(start_date: str, end_date: str, db: Session = Depends(get_db)):
    """
    Generate Massachusetts DUA activity report for a custom date range in CSV format
    
    Parameters:
    - start_date: ISO format YYYY-MM-DD
    - end_date: ISO format YYYY-MM-DD
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    if start > end:
        raise HTTPException(status_code=400, detail="Start date must be before end date")
    
    # Find the Sunday before or on start_date
    days_since_sunday = (start.weekday() + 1) % 7
    week_start = start - timedelta(days=days_since_sunday)
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([f"Massachusetts DUA Activity Report"])
    writer.writerow([f"Date Range: {start.strftime('%m/%d/%Y')} through {end.strftime('%m/%d/%Y')}"])
    writer.writerow([])
    
    # Process each week
    current_week_start = week_start
    while current_week_start <= end:
        week_end = current_week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
        
        # Get activities for this week
        activities = crud.get_weekly_activity(db, current_week_start, week_end)
        
        # Only show weeks that overlap with the requested range
        if current_week_start <= end and week_end >= start:
            # Write week header
            writer.writerow([f"Week starting Sunday {current_week_start.strftime('%m/%d/%Y')} through Saturday {week_end.strftime('%m/%d/%Y')}"])
            writer.writerow(['Date', 'Position', 'Pay Rate', 'Employer Name', 'Employer Address', 
                           'Job ID or Person Contacted', 'Contact Email/Website/Phone', 'Result'])
            
            if not activities:
                writer.writerow(['No job search activities recorded for this week'])
            else:
                for activity in activities:
                    # Only include activities within the requested range
                    if start <= activity['date'] <= end:
                        writer.writerow([
                            activity['date'].strftime('%m/%d/%Y'),
                            activity['position'],
                            activity['pay_rate'],
                            activity['employer_name'],
                            activity['employer_address'],
                            activity['contact_person'] if activity['contact_person'] else activity['job_id'],
                            activity['contact_email'] if activity['contact_email'] else activity['employer_address'],
                            activity['result']
                        ])
            
            writer.writerow([])  # Empty row between weeks
        
        # Move to next week
        current_week_start += timedelta(days=7)
    
    # Return as streaming response
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=dua_range_{start.strftime('%Y%m%d')}_{end.strftime('%Y%m%d')}.csv"
        }
    )
