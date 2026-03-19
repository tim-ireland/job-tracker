"""
Database models for job tracking application
"""
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Use environment variable for database path, fallback to local default
DATA_DIR = os.environ.get('DATA_DIR', '.')
SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL', f"sqlite:///{DATA_DIR}/job_applications.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Company(Base):
    """Company information"""
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    website = Column(String)
    size = Column(String)
    tech_stack = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    applications = relationship("Application", back_populates="company")
    contacts = relationship("Contact", back_populates="company")


class Application(Base):
    """Job application tracking"""
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    role = Column(String, nullable=False)
    priority = Column(String, default="P4")
    status = Column(String, default="Pipeline")
    job_url = Column(String)
    location = Column(String)
    remote_policy = Column(String)
    salary_range = Column(String)
    resume_filename = Column(String)
    cover_letter_filename = Column(String)
    hiring_manager_name = Column(String)
    hiring_manager_email = Column(String)
    date_applied = Column(DateTime)
    date_screening = Column(DateTime)
    date_interview = Column(DateTime)
    date_offer = Column(DateTime)
    date_closed = Column(DateTime)
    notes = Column(Text)
    
    # Match scoring fields for bulk job evaluation
    match_score = Column(Integer)
    match_reasoning = Column(Text)
    match_strengths = Column(Text)  # JSON array as string
    match_gaps = Column(Text)  # JSON array as string
    match_recommendation = Column(String)  # Apply|Skip|Reach
    evaluated_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    company = relationship("Company", back_populates="applications")
    interactions = relationship("Interaction", back_populates="application")
    interviews = relationship("Interview", back_populates="application")
    offers = relationship("Offer", back_populates="application")


class Contact(Base):
    """Contact information for companies"""
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String, nullable=False)
    role = Column(String)
    email = Column(String)
    phone = Column(String)
    linkedin = Column(String)
    rel_type = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    company = relationship("Company", back_populates="contacts")


class Interaction(Base):
    """Track interactions for each application"""
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    type = Column(String)
    contact_person = Column(String)
    summary = Column(Text)
    next_steps = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="interactions")


class Interview(Base):
    """Track interview schedules for applications"""
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    scheduled_date = Column(DateTime)
    interview_type = Column(String)  # Phone, Video, On-site, Technical, Behavioral
    interviewer_name = Column(String)
    interviewer_email = Column(String)
    interviewer_title = Column(String)
    location = Column(String)
    meeting_link = Column(String)
    notes = Column(Text)
    completed = Column(String, default="No")  # Yes/No
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    application = relationship("Application", back_populates="interviews")


class Offer(Base):
    """Track job offers"""
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    offer_date = Column(DateTime)
    response_deadline = Column(DateTime)
    
    # Compensation
    base_salary = Column(Integer)
    bonus_target = Column(Integer)
    signing_bonus = Column(Integer)
    equity_value = Column(Integer)
    equity_details = Column(String)
    total_comp = Column(Integer)
    
    # Benefits
    pto_days = Column(Integer)
    sick_days = Column(Integer)
    holidays = Column(Integer)
    health_insurance = Column(String)
    retirement_match = Column(String)
    other_benefits = Column(Text)
    
    # Work Details
    start_date = Column(DateTime)
    remote_policy = Column(String)
    relocation_assistance = Column(String)
    
    # Status
    status = Column(String, default="Pending")  # Pending, Accepted, Declined, Negotiating
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    application = relationship("Application", back_populates="offers")


def init_db():
    """Initialize database with tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for getting DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
