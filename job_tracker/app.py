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


# ==================== BULK JOB SCORING ENDPOINTS ====================

from .scoring import JobScorer

class BulkScoreRequest(BaseModel):
    status_filter: Optional[str] = "Pipeline"
    use_api: bool = False

class ParseScoresRequest(BaseModel):
    ai_response: str


@app.post("/api/applications/bulk-score")
def bulk_score_applications(request: BulkScoreRequest, db: Session = Depends(get_db)):
    """
    Generate bulk scoring prompt for Pipeline applications.
    
    Returns prompt to copy-paste into AI, or (future) calls AI API directly.
    """
    
    # Get applications with specified status
    applications = crud.get_applications(db, status=request.status_filter, limit=1000)
    
    if not applications:
        raise HTTPException(
            status_code=404, 
            detail=f"No applications found with status '{request.status_filter}'"
        )
    
    # Load job descriptions and build application data
    app_data = []
    for app in applications:
        # Get application directory
        company_name = app.company.name.replace(' ', '_')
        role = app.role.replace(' ', '_').replace('/', '_')
        app_dir = APPLICATIONS_DIR / f"{company_name}_{role}"
        job_desc_path = app_dir / "job_description.txt"
        
        # Load job description if exists
        job_description = ""
        if job_desc_path.exists():
            with open(job_desc_path, 'r') as f:
                job_description = f.read()
        
        app_data.append({
            'id': app.id,
            'company': app.company.name,
            'role': app.role,
            'location': app.location or 'Not specified',
            'job_url': app.job_url or 'Not provided',
            'job_description': job_description or 'No job description found'
        })
    
    # Generate prompt
    scorer = JobScorer(data_dir=DATA_DIR)
    prompt = scorer.generate_bulk_prompt(app_data)
    
    if request.use_api:
        # Future: Call AI API here
        return {
            "message": "API integration not yet implemented",
            "prompt": prompt,
            "application_count": len(app_data)
        }
    
    # Return prompt for manual copy-paste
    return {
        "prompt": prompt,
        "application_count": len(app_data),
        "applications": [{'id': a['id'], 'company': a['company'], 'role': a['role']} for a in app_data]
    }


@app.post("/api/applications/parse-scores")
def parse_scoring_response(request: ParseScoresRequest, db: Session = Depends(get_db)):
    """
    Parse AI scoring response and update database with scores.
    
    Expects JSON response from AI with evaluations array.
    """
    
    try:
        scorer = JobScorer(data_dir=DATA_DIR)
        results = scorer.parse_scores(request.ai_response)
        
        if not results:
            raise HTTPException(status_code=400, detail="No evaluations found in response")
        
        # Update database
        updated = 0
        failed = 0
        errors = []
        
        for result in results:
            try:
                app_id = result['application_id']
                
                # Get application
                application = crud.get_application(db, app_id)
                if not application:
                    errors.append(f"Application {app_id} not found")
                    failed += 1
                    continue
                
                # Update with scores
                application.match_score = result['match_score']
                application.match_reasoning = result['match_reasoning']
                application.match_strengths = result['match_strengths']
                application.match_gaps = result['match_gaps']
                application.match_recommendation = result['match_recommendation']
                application.evaluated_at = datetime.fromisoformat(result['evaluated_at'])
                
                db.commit()
                updated += 1
                
            except Exception as e:
                errors.append(f"Application {result.get('application_id', 'unknown')}: {str(e)}")
                failed += 1
                db.rollback()
        
        return {
            "updated": updated,
            "failed": failed,
            "errors": errors if errors else None
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse scores: {str(e)}")


@app.post("/api/applications/{application_id}/score")
def score_single_application(application_id: int, db: Session = Depends(get_db)):
    """
    Generate scoring prompt for a single application.
    
    Useful for re-scoring individual jobs or scoring new applications.
    """
    
    application = crud.get_application(db, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Get job description
    company_name = application.company.name.replace(' ', '_')
    role = application.role.replace(' ', '_').replace('/', '_')
    app_dir = APPLICATIONS_DIR / f"{company_name}_{role}"
    job_desc_path = app_dir / "job_description.txt"
    
    job_description = ""
    if job_desc_path.exists():
        with open(job_desc_path, 'r') as f:
            job_description = f.read()
    
    app_data = [{
        'id': application.id,
        'company': application.company.name,
        'role': application.role,
        'location': application.location or 'Not specified',
        'job_url': application.job_url or 'Not provided',
        'job_description': job_description or 'No job description found'
    }]
    
    # Generate prompt for single application
    scorer = JobScorer(data_dir=DATA_DIR)
    prompt = scorer.generate_bulk_prompt(app_data)
    
    return {
        "prompt": prompt,
        "application": {
            "id": application.id,
            "company": application.company.name,
            "role": application.role
        }
    }


@app.post("/api/applications/bulk-import")
def bulk_import_applications(urls: List[str] = Body(..., embed=True), db: Session = Depends(get_db)):
    """
    Bulk import applications from a list of URLs.
    
    Validates URLs and skips LinkedIn job posting URLs.
    Creates application entries and directories for valid URLs.
    """
    import re
    import urllib.request
    from bs4 import BeautifulSoup
    
    results = {
        "created": [],
        "skipped": [],
        "failed": []
    }
    
    # LinkedIn URL patterns to skip
    linkedin_patterns = [
        r'linkedin\.com/jobs/',
        r'linkedin\.com/job/',
        r'linkedin\.com/.*jobs/view/'
    ]
    
    for url in urls:
        url = url.strip()
        if not url:
            continue
            
        # Check if it's a LinkedIn URL
        is_linkedin = any(re.search(pattern, url, re.IGNORECASE) for pattern in linkedin_patterns)
        if is_linkedin:
            results["skipped"].append({
                "url": url,
                "reason": "LinkedIn job posting URLs are not supported. Please use the company's direct application page."
            })
            continue
        
        try:
            # Try to fetch the page and extract company name and role
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Try to extract title (role)
                title = soup.find('title')
                role = title.get_text().strip() if title else "Unknown Role"
                
                # Clean up common title patterns
                role = re.sub(r'\s*[-|]\s*.*$', '', role)  # Remove "- Company Name" suffix
                role = role[:100]  # Limit length
                
                # Try to extract company from URL domain
                from urllib.parse import urlparse
                domain = urlparse(url).netloc
                company_name = domain.replace('www.', '').split('.')[0].title()
                
            # Check if company exists, create if not
            company = crud.get_company_by_name(db, company_name)
            if not company:
                company = crud.create_company(db, models.CompanyCreate(name=company_name))
            
            # Create application
            application = crud.create_application(db, models.ApplicationCreate(
                company_id=company.id,
                role=role,
                job_url=url,
                status="Pipeline",
                priority="Medium"
            ))
            
            # Create application directory
            company_name_clean = company_name.replace(' ', '_')
            role_clean = role.replace(' ', '_').replace('/', '_')
            app_dir = APPLICATIONS_DIR / f"{company_name_clean}_{role_clean}"
            app_dir.mkdir(parents=True, exist_ok=True)
            
            # Save job description URL
            job_desc_path = app_dir / "job_description.txt"
            with open(job_desc_path, 'w') as f:
                f.write(f"Job URL: {url}\n\n")
                f.write("# Paste the job description here\n\n")
                f.write("## Company Information\n")
                f.write("[Company background, mission, values]\n\n")
                f.write("## Role Description\n")
                f.write("[Role summary]\n\n")
                f.write("## Responsibilities\n")
                f.write("- [Responsibility 1]\n")
                f.write("- [Responsibility 2]\n\n")
                f.write("## Requirements\n")
                f.write("- [Requirement 1]\n")
                f.write("- [Requirement 2]\n\n")
                f.write("## Nice to Have\n")
                f.write("- [Nice to have 1]\n")
                f.write("- [Nice to have 2]\n\n")
                f.write("## Benefits\n")
                f.write("[Benefits information]\n")
            
            results["created"].append({
                "id": application.id,
                "company": company_name,
                "role": role,
                "url": url,
                "directory": str(app_dir.relative_to(APPLICATIONS_DIR))
            })
            
        except Exception as e:
            results["failed"].append({
                "url": url,
                "error": str(e)
            })
    
    return {
        "summary": {
            "created": len(results["created"]),
            "skipped": len(results["skipped"]),
            "failed": len(results["failed"])
        },
        "details": results
    }
