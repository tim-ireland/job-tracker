"""
CRUD operations for database
"""
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from . import database as db
from . import models


def get_companies(session: Session, skip: int = 0, limit: int = 100):
    return session.query(db.Company).offset(skip).limit(limit).all()


def get_company(session: Session, company_id: int):
    return session.query(db.Company).filter(db.Company.id == company_id).first()


def get_company_by_name(session: Session, name: str):
    return session.query(db.Company).filter(db.Company.name == name).first()


def create_company(session: Session, company: models.CompanyCreate):
    db_company = db.Company(**company.model_dump())
    session.add(db_company)
    session.commit()
    session.refresh(db_company)
    return db_company


def update_company(session: Session, company_id: int, company: models.CompanyUpdate):
    db_company = get_company(session, company_id)
    if db_company:
        update_data = company.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_company, key, value)
        db_company.updated_at = datetime.utcnow()
        session.commit()
        session.refresh(db_company)
    return db_company


def delete_company(session: Session, company_id: int):
    db_company = get_company(session, company_id)
    if db_company:
        session.delete(db_company)
        session.commit()
        return True
    return False


def get_applications(session: Session, skip: int = 0, limit: int = 100, 
                     status: Optional[str] = None, priority: Optional[str] = None):
    query = session.query(db.Application)
    if status:
        query = query.filter(db.Application.status == status)
    if priority:
        query = query.filter(db.Application.priority == priority)
    return query.offset(skip).limit(limit).all()


def get_application(session: Session, application_id: int):
    return session.query(db.Application).filter(db.Application.id == application_id).first()


def create_application(session: Session, application: models.ApplicationCreate):
    db_application = db.Application(**application.model_dump())
    
    if db_application.status == 'Applied' and not db_application.date_applied:
        db_application.date_applied = datetime.utcnow()
    
    session.add(db_application)
    session.commit()
    session.refresh(db_application)
    return db_application


def update_application(session: Session, application_id: int, application: models.ApplicationUpdate):
    db_application = get_application(session, application_id)
    if db_application:
        update_data = application.model_dump(exclude_unset=True)
        
        if 'status' in update_data:
            status = update_data['status']
            if status == 'Applied' and not db_application.date_applied:
                db_application.date_applied = datetime.utcnow()
            elif status == 'Screening' and not db_application.date_screening:
                db_application.date_screening = datetime.utcnow()
            elif status == 'Interview' and not db_application.date_interview:
                db_application.date_interview = datetime.utcnow()
            elif status == 'Offer' and not db_application.date_offer:
                db_application.date_offer = datetime.utcnow()
            elif status in ['Rejected', 'Withdrawn', 'Accepted'] and not db_application.date_closed:
                db_application.date_closed = datetime.utcnow()
        
        for key, value in update_data.items():
            setattr(db_application, key, value)
        
        db_application.updated_at = datetime.utcnow()
        session.commit()
        session.refresh(db_application)
    return db_application


def delete_application(session: Session, application_id: int):
    db_application = get_application(session, application_id)
    if db_application:
        session.delete(db_application)
        session.commit()
        return True
    return False


def get_contacts(session: Session, company_id: Optional[int] = None):
    query = session.query(db.Contact)
    if company_id:
        query = query.filter(db.Contact.company_id == company_id)
    return query.all()


def get_contact(session: Session, contact_id: int):
    return session.query(db.Contact).filter(db.Contact.id == contact_id).first()


def create_contact(session: Session, contact: models.ContactCreate):
    db_contact = db.Contact(**contact.model_dump())
    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)
    return db_contact


def update_contact(session: Session, contact_id: int, contact: models.ContactUpdate):
    db_contact = get_contact(session, contact_id)
    if db_contact:
        update_data = contact.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_contact, key, value)
        db_contact.updated_at = datetime.utcnow()
        session.commit()
        session.refresh(db_contact)
    return db_contact


def delete_contact(session: Session, contact_id: int):
    db_contact = get_contact(session, contact_id)
    if db_contact:
        session.delete(db_contact)
        session.commit()
        return True
    return False


def get_interactions(session: Session, application_id: int):
    return session.query(db.Interaction).filter(
        db.Interaction.application_id == application_id
    ).order_by(db.Interaction.date.desc()).all()


def create_interaction(session: Session, interaction: models.InteractionCreate):
    db_interaction = db.Interaction(**interaction.model_dump())
    session.add(db_interaction)
    session.commit()
    session.refresh(db_interaction)
    return db_interaction


# Interview CRUD
def get_interviews(session: Session, application_id: int):
    return session.query(db.Interview).filter(
        db.Interview.application_id == application_id
    ).order_by(db.Interview.scheduled_date).all()


def get_interview(session: Session, interview_id: int):
    return session.query(db.Interview).filter(db.Interview.id == interview_id).first()


def create_interview(session: Session, interview: models.InterviewCreate):
    db_interview = db.Interview(**interview.model_dump())
    session.add(db_interview)
    session.commit()
    session.refresh(db_interview)
    return db_interview


def update_interview(session: Session, interview_id: int, interview: models.InterviewUpdate):
    db_interview = get_interview(session, interview_id)
    if db_interview:
        update_data = interview.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_interview, key, value)
        db_interview.updated_at = datetime.utcnow()
        session.commit()
        session.refresh(db_interview)
    return db_interview


def delete_interview(session: Session, interview_id: int):
    db_interview = get_interview(session, interview_id)
    if db_interview:
        session.delete(db_interview)
        session.commit()
        return True
    return False


# Offer CRUD
def get_offers(session: Session, application_id: Optional[int] = None):
    query = session.query(db.Offer)
    if application_id:
        query = query.filter(db.Offer.application_id == application_id)
    return query.all()


def get_offer(session: Session, offer_id: int):
    return session.query(db.Offer).filter(db.Offer.id == offer_id).first()


def create_offer(session: Session, offer: models.OfferCreate):
    db_offer = db.Offer(**offer.model_dump())
    session.add(db_offer)
    session.commit()
    session.refresh(db_offer)
    return db_offer


def update_offer(session: Session, offer_id: int, offer: models.OfferUpdate):
    db_offer = get_offer(session, offer_id)
    if db_offer:
        update_data = offer.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_offer, key, value)
        db_offer.updated_at = datetime.utcnow()
        session.commit()
        session.refresh(db_offer)
    return db_offer


def delete_offer(session: Session, offer_id: int):
    db_offer = get_offer(session, offer_id)
    if db_offer:
        session.delete(db_offer)
        session.commit()
        return True
    return False


def get_offer_comparison(session: Session):
    """Get all offers with related company and application info for comparison"""
    offers = session.query(db.Offer).all()
    
    companies = {}
    applications = {}
    
    for offer in offers:
        app = session.query(db.Application).filter(db.Application.id == offer.application_id).first()
        if app:
            applications[app.id] = app.role
            company = session.query(db.Company).filter(db.Company.id == app.company_id).first()
            if company:
                companies[company.id] = company.name
    
    return models.OfferComparison(
        offers=offers,
        companies=companies,
        applications=applications
    )


def get_dashboard_stats(session: Session):
    applications = session.query(db.Application).all()
    
    total = len(applications)
    
    by_status = {}
    for app in applications:
        by_status[app.status] = by_status.get(app.status, 0) + 1
    
    by_priority = {}
    for app in applications:
        by_priority[app.priority] = by_priority.get(app.priority, 0) + 1
    
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent = session.query(db.Application).filter(
        db.Application.created_at >= seven_days_ago
    ).order_by(db.Application.created_at.desc()).limit(10).all()
    
    upcoming = session.query(db.Application).filter(
        db.Application.status == 'Interview',
        db.Application.date_interview.isnot(None)
    ).order_by(db.Application.date_interview).limit(10).all()
    
    return models.DashboardStats(
        total_applications=total,
        by_status=by_status,
        by_priority=by_priority,
        recent_applications=recent,
        upcoming_interviews=upcoming
    )
