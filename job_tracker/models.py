"""
Pydantic models for API validation
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    website: Optional[str] = None
    size: Optional[str] = None
    tech_stack: Optional[str] = None
    notes: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    website: Optional[str] = None
    size: Optional[str] = None
    tech_stack: Optional[str] = None
    notes: Optional[str] = None


class Company(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApplicationBase(BaseModel):
    company_id: int
    role: str
    priority: str = "P4"
    status: str = "Pipeline"
    job_url: Optional[str] = None
    location: Optional[str] = None
    remote_policy: Optional[str] = None
    salary_range: Optional[str] = None
    resume_filename: Optional[str] = None
    cover_letter_filename: Optional[str] = None
    hiring_manager_name: Optional[str] = None
    hiring_manager_email: Optional[str] = None
    notes: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    company_id: Optional[int] = None
    role: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    job_url: Optional[str] = None
    location: Optional[str] = None
    remote_policy: Optional[str] = None
    salary_range: Optional[str] = None
    resume_filename: Optional[str] = None
    cover_letter_filename: Optional[str] = None
    hiring_manager_name: Optional[str] = None
    hiring_manager_email: Optional[str] = None
    date_applied: Optional[datetime] = None
    date_screening: Optional[datetime] = None
    date_interview: Optional[datetime] = None
    date_offer: Optional[datetime] = None
    date_closed: Optional[datetime] = None
    notes: Optional[str] = None
    personal_rank: Optional[int] = None


class Application(ApplicationBase):
    id: int
    date_applied: Optional[datetime] = None
    date_screening: Optional[datetime] = None
    date_interview: Optional[datetime] = None
    date_offer: Optional[datetime] = None
    date_closed: Optional[datetime] = None
    personal_rank: Optional[int] = None
    match_score: Optional[int] = None
    match_reasoning: Optional[str] = None
    match_strengths: Optional[str] = None
    match_gaps: Optional[str] = None
    match_recommendation: Optional[str] = None
    evaluated_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ContactBase(BaseModel):
    company_id: int
    name: str
    role: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    relationship: Optional[str] = None
    notes: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    company_id: Optional[int] = None
    name: Optional[str] = None
    role: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    relationship: Optional[str] = None
    notes: Optional[str] = None


class Contact(ContactBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InteractionBase(BaseModel):
    application_id: int
    type: str
    contact_person: Optional[str] = None
    summary: Optional[str] = None
    next_steps: Optional[str] = None


class InteractionCreate(InteractionBase):
    pass


class Interaction(InteractionBase):
    id: int
    date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    total_applications: int
    by_status: dict
    by_priority: dict
    recent_applications: List[Application]
    upcoming_interviews: List[Application]


class InterviewBase(BaseModel):
    application_id: int
    scheduled_date: Optional[datetime] = None
    interview_type: Optional[str] = None
    interviewer_name: Optional[str] = None
    interviewer_email: Optional[str] = None
    interviewer_title: Optional[str] = None
    location: Optional[str] = None
    meeting_link: Optional[str] = None
    notes: Optional[str] = None
    completed: str = "No"


class InterviewCreate(InterviewBase):
    pass


class InterviewUpdate(BaseModel):
    scheduled_date: Optional[datetime] = None
    interview_type: Optional[str] = None
    interviewer_name: Optional[str] = None
    interviewer_email: Optional[str] = None
    interviewer_title: Optional[str] = None
    location: Optional[str] = None
    meeting_link: Optional[str] = None
    notes: Optional[str] = None
    completed: Optional[str] = None


class Interview(InterviewBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OfferBase(BaseModel):
    application_id: int
    offer_date: Optional[datetime] = None
    response_deadline: Optional[datetime] = None
    base_salary: Optional[int] = None
    bonus_target: Optional[int] = None
    signing_bonus: Optional[int] = None
    equity_value: Optional[int] = None
    equity_details: Optional[str] = None
    total_comp: Optional[int] = None
    pto_days: Optional[int] = None
    sick_days: Optional[int] = None
    holidays: Optional[int] = None
    health_insurance: Optional[str] = None
    retirement_match: Optional[str] = None
    other_benefits: Optional[str] = None
    start_date: Optional[datetime] = None
    remote_policy: Optional[str] = None
    relocation_assistance: Optional[str] = None
    status: str = "Pending"
    notes: Optional[str] = None


class OfferCreate(OfferBase):
    pass


class OfferUpdate(BaseModel):
    offer_date: Optional[datetime] = None
    response_deadline: Optional[datetime] = None
    base_salary: Optional[int] = None
    bonus_target: Optional[int] = None
    signing_bonus: Optional[int] = None
    equity_value: Optional[int] = None
    equity_details: Optional[str] = None
    total_comp: Optional[int] = None
    pto_days: Optional[int] = None
    sick_days: Optional[int] = None
    holidays: Optional[int] = None
    health_insurance: Optional[str] = None
    retirement_match: Optional[str] = None
    other_benefits: Optional[str] = None
    start_date: Optional[datetime] = None
    remote_policy: Optional[str] = None
    relocation_assistance: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class Offer(OfferBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OfferComparison(BaseModel):
    """Model for comparing multiple offers"""
    offers: List[Offer]
    companies: dict  # company_id -> company_name mapping
    applications: dict  # application_id -> role mapping
