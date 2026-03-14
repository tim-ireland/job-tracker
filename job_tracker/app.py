"""
FastAPI application for job tracking
"""
from fastapi import FastAPI, Depends, HTTPException, Request, Body
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pathlib import Path
from pydantic import BaseModel
import os

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
    
    if not dir_name:
        return {"pdfs": []}
    
    app_dir = APPLICATIONS_DIR / dir_name
    if not app_dir.exists():
        return {"pdfs": []}
    
    # Find all PDF files
    pdfs = []
    for pdf_file in app_dir.glob("*.pdf"):
        pdfs.append({
            "name": pdf_file.name,
            "path": str(pdf_file.relative_to(APPLICATIONS_DIR)),
            "size": pdf_file.stat().st_size,
            "modified": pdf_file.stat().st_mtime
        })
    
    return {"pdfs": sorted(pdfs, key=lambda x: x["modified"], reverse=True)}


@app.get("/api/files/pdf/{file_path:path}")
def get_pdf_file(file_path: str):
    """Serve a PDF file from the applications directory"""
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
    
    if not full_path.suffix.lower() == '.pdf':
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    return FileResponse(
        full_path,
        media_type="application/pdf",
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
