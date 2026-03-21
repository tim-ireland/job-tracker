"""
Seed a demo SQLite database with fictional job application data.
Run with:  DATA_DIR=/tmp/demo-job-tracker python scripts/seed_demo_data.py
"""
import os
import sys
import json
from datetime import datetime, timedelta

# Point at demo data dir before importing anything that reads DATA_DIR
DATA_DIR = os.environ.get("DATA_DIR", "/tmp/demo-job-tracker")
os.makedirs(DATA_DIR, exist_ok=True)
os.environ["DATA_DIR"] = DATA_DIR
os.environ["DATABASE_URL"] = f"sqlite:///{DATA_DIR}/job_applications.db"

# Add project root to path so job_tracker is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from job_tracker.database import init_db, SessionLocal, Company, Application, Interview, Offer

init_db()
db = SessionLocal()

# Wipe existing demo data
db.query(Offer).delete()
db.query(Interview).delete()
db.query(Application).delete()
db.query(Company).delete()
db.commit()

# ── Companies ────────────────────────────────────────────────────────────────
companies_data = [
    {"name": "Axiom Cloud",     "website": "https://axiomcloud.io",    "size": "501-1000",   "tech_stack": "Go, Kubernetes, Postgres, gRPC"},
    {"name": "Helix AI",        "website": "https://helixai.com",      "size": "51-200",     "tech_stack": "Python, PyTorch, FastAPI, Redis"},
    {"name": "Novu Systems",    "website": "https://novusystems.com",  "size": "1001-5000",  "tech_stack": "Java, Spring Boot, Kafka, AWS"},
    {"name": "Lattice Labs",    "website": "https://laticelabs.dev",   "size": "11-50",      "tech_stack": "Rust, WebAssembly, TypeScript"},
    {"name": "Meridian Health", "website": "https://meridianhealth.io","size": "5001-10000", "tech_stack": "C#, .NET, Azure, SQL Server"},
    {"name": "Crestline Data",  "website": "https://crestlinedata.com","size": "201-500",    "tech_stack": "Scala, Spark, dbt, Snowflake"},
    {"name": "Orion Finance",   "website": "https://orionfinance.com", "size": "1001-5000",  "tech_stack": "Python, React, PostgreSQL, Terraform"},
    {"name": "Stratum Dev",     "website": "https://stratumdev.io",    "size": "51-200",     "tech_stack": "Ruby on Rails, React, Heroku"},
]

companies = {}
for c in companies_data:
    obj = Company(**c)
    db.add(obj)
    db.flush()
    companies[c["name"]] = obj.id

db.commit()

# ── Applications ─────────────────────────────────────────────────────────────
today = datetime.utcnow()

def d(days_ago):
    return today - timedelta(days=days_ago)

apps_data = [
    {
        "company": "Axiom Cloud",
        "role": "Staff Software Engineer, Platform",
        "priority": "P1",
        "status": "Interview",
        "remote_policy": "Remote",
        "salary_range": "$200,000 - $240,000",
        "location": "San Francisco, CA",
        "date_applied": d(18),
        "match_score": 92,
        "personal_rank": 5,
        "match_recommendation": "Apply",
        "match_strengths": json.dumps(["Deep distributed systems experience", "Go expertise matches stack", "Prior platform eng leadership"]),
        "match_gaps": json.dumps(["No direct Kubernetes operator authorship"]),
        "match_reasoning": "Strong alignment on platform eng background and Go. Minor gap in operator patterns but overall excellent fit.",
        "notes": "Recruiter reached out on LinkedIn. Loop starts next week.",
        "job_url": "https://axiomcloud.io/careers/staff-swe-platform",
    },
    {
        "company": "Helix AI",
        "role": "Engineering Manager, ML Infrastructure",
        "priority": "P1",
        "status": "Screening",
        "remote_policy": "Hybrid",
        "salary_range": "$210,000 - $250,000",
        "location": "New York, NY",
        "date_applied": d(10),
        "match_score": 87,
        "personal_rank": 4,
        "match_recommendation": "Apply",
        "match_strengths": json.dumps(["Managed ML infra teams before", "Experience scaling training pipelines", "Python/FastAPI fluency"]),
        "match_gaps": json.dumps(["PyTorch internals depth expected"]),
        "match_reasoning": "Good match for the EM scope. Technical depth on ML frameworks is a soft gap but manageable.",
        "notes": "Phone screen with VP Eng scheduled.",
        "job_url": "https://helixai.com/jobs/em-ml-infra",
    },
    {
        "company": "Novu Systems",
        "role": "Senior Principal Engineer",
        "priority": "P2",
        "status": "Applied",
        "remote_policy": "On-site",
        "salary_range": "$195,000 - $225,000",
        "location": "Austin, TX",
        "date_applied": d(7),
        "match_score": 74,
        "personal_rank": 3,
        "match_recommendation": "Apply",
        "match_strengths": json.dumps(["Enterprise-scale architecture experience", "Java/Kafka familiarity"]),
        "match_gaps": json.dumps(["On-site only is a stretch", "Spring Boot depth limited"]),
        "match_reasoning": "Solid on architecture scope but on-site requirement and Java depth are notable gaps.",
        "notes": "Applied via company portal.",
        "job_url": "https://novusystems.com/careers/sr-principal-eng",
    },
    {
        "company": "Lattice Labs",
        "role": "Director of Engineering",
        "priority": "P1",
        "status": "Offer",
        "remote_policy": "Remote",
        "salary_range": "$230,000 - $270,000",
        "location": "Remote",
        "date_applied": d(35),
        "match_score": 95,
        "personal_rank": 5,
        "match_recommendation": "Apply",
        "match_strengths": json.dumps(["Built eng orgs from Series A to C", "Systems programming background fits Rust culture", "Excited by Wasm platform thesis"]),
        "match_gaps": json.dumps([]),
        "match_reasoning": "Near-perfect fit. Strong culture alignment and technical overlap.",
        "notes": "Verbal offer received. Waiting on written comp package.",
        "job_url": "https://laticelabs.dev/jobs/dir-eng",
    },
    {
        "company": "Meridian Health",
        "role": "VP of Engineering, Platform",
        "priority": "P3",
        "status": "Pipeline",
        "remote_policy": "Hybrid",
        "salary_range": "$220,000 - $260,000",
        "location": "Chicago, IL",
        "date_applied": None,
        "match_score": 68,
        "personal_rank": 2,
        "match_recommendation": "Apply",
        "match_strengths": json.dumps(["Large org management experience", "Cloud migration background"]),
        "match_gaps": json.dumps(["Healthcare domain unfamiliar", ".NET stack mismatch", "Chicago hybrid is a stretch"]),
        "match_reasoning": "Reach role. Healthcare compliance and .NET culture are significant gaps.",
        "notes": "Sourced from LinkedIn. Not yet applied.",
        "job_url": "https://meridianhealth.io/careers/vp-eng-platform",
    },
    {
        "company": "Crestline Data",
        "role": "Staff Engineer, Data Platform",
        "priority": "P2",
        "status": "Rejected",
        "remote_policy": "Remote",
        "salary_range": "$185,000 - $215,000",
        "location": "Remote",
        "date_applied": d(45),
        "match_score": 71,
        "personal_rank": 3,
        "match_recommendation": "Apply",
        "match_strengths": json.dumps(["Data pipeline architecture at scale", "Cloud-native infra background"]),
        "match_gaps": json.dumps(["Scala required, limited exposure", "Spark internals gap"]),
        "match_reasoning": "Decent fit on data infra patterns but Scala/Spark depth was the blocker.",
        "notes": "Rejected after technical screen. Feedback: Scala depth insufficient.",
        "job_url": "https://crestlinedata.com/jobs/staff-eng-data",
    },
    {
        "company": "Orion Finance",
        "role": "Engineering Manager, Core Platform",
        "priority": "P2",
        "status": "Interview",
        "remote_policy": "Hybrid",
        "salary_range": "$190,000 - $220,000",
        "location": "Boston, MA",
        "date_applied": d(14),
        "match_score": 83,
        "personal_rank": 4,
        "match_recommendation": "Apply",
        "match_strengths": json.dumps(["Platform eng leadership", "Python/Terraform familiarity", "FinTech-adjacent experience"]),
        "match_gaps": json.dumps(["Financial compliance domain new"]),
        "match_reasoning": "Strong on the eng management and tech side. Compliance domain is learnable.",
        "notes": "Technical loop with two staff engineers this Thursday.",
        "job_url": "https://orionfinance.com/careers/em-core-platform",
    },
    {
        "company": "Stratum Dev",
        "role": "Head of Engineering",
        "priority": "P3",
        "status": "Withdrawn",
        "remote_policy": "Remote",
        "salary_range": "$170,000 - $195,000",
        "location": "Remote",
        "date_applied": d(30),
        "match_score": 79,
        "personal_rank": 2,
        "match_recommendation": "Apply",
        "match_strengths": json.dumps(["Early-stage leadership experience", "Full-stack team management"]),
        "match_gaps": json.dumps(["Comp below target", "Ruby/Rails not in background"]),
        "match_reasoning": "Good culture match but comp and stack were misaligned with goals.",
        "notes": "Withdrew after offer discussion — comp too low.",
        "job_url": "https://stratumdev.io/jobs/head-of-eng",
    },
    {
        "company": "Axiom Cloud",
        "role": "Principal Engineer, Networking",
        "priority": "P2",
        "status": "Pipeline",
        "remote_policy": "Remote",
        "salary_range": "$210,000 - $240,000",
        "location": "Remote",
        "date_applied": None,
        "match_score": 81,
        "personal_rank": 3,
        "match_recommendation": "Apply",
        "match_strengths": json.dumps(["SDN and overlay network design", "Go + eBPF background", "Cloud-native infra at scale"]),
        "match_gaps": json.dumps(["SR-IOV hardware offload unfamiliar"]),
        "match_reasoning": "Strong overlap on software-defined networking. One hardware-specific gap.",
        "notes": "Identified as a second role at Axiom to explore during loop.",
        "job_url": "https://axiomcloud.io/careers/principal-eng-networking",
    },
    {
        "company": "Helix AI",
        "role": "Staff Engineer, Developer Experience",
        "priority": "P2",
        "status": "Screening",
        "remote_policy": "Remote",
        "salary_range": "$195,000 - $225,000",
        "location": "Remote",
        "date_applied": d(5),
        "match_score": 88,
        "personal_rank": 4,
        "match_recommendation": "Apply",
        "match_strengths": json.dumps(["Built internal dev tooling platforms", "CI/CD and build system expertise", "Strong Python + TypeScript background"]),
        "match_gaps": json.dumps(["Helix-specific ML toolchain unfamiliar"]),
        "match_reasoning": "Developer experience background is an excellent match. ML toolchain context is quickly learnable.",
        "notes": "Recruiter intro call done. Moving to hiring manager screen.",
        "job_url": "https://helixai.com/jobs/staff-eng-devex",
    },
]

for a in apps_data:
    obj = Application(
        company_id=companies[a["company"]],
        role=a["role"],
        priority=a["priority"],
        status=a["status"],
        remote_policy=a["remote_policy"],
        salary_range=a["salary_range"],
        location=a["location"],
        date_applied=a.get("date_applied"),
        match_score=a.get("match_score"),
        personal_rank=a.get("personal_rank"),
        match_recommendation=a.get("match_recommendation"),
        match_strengths=a.get("match_strengths"),
        match_gaps=a.get("match_gaps"),
        match_reasoning=a.get("match_reasoning"),
        notes=a.get("notes"),
        job_url=a.get("job_url"),
        evaluated_at=today if a.get("match_score") else None,
    )
    db.add(obj)
    db.flush()

    # Add an interview for Interview-status apps
    if a["status"] == "Interview":
        db.add(Interview(
            application_id=obj.id,
            scheduled_date=today + timedelta(days=3),
            interview_type="Technical",
            interviewer_name="Alex Rivera",
            interviewer_title="Staff Engineer",
            meeting_link="https://meet.example.com/loop",
            completed="No",
        ))

    # Add an offer for Offer-status app
    if a["status"] == "Offer":
        db.add(Offer(
            application_id=obj.id,
            offer_date=today - timedelta(days=2),
            response_deadline=today + timedelta(days=5),
            base_salary=245000,
            bonus_target=25000,
            signing_bonus=30000,
            equity_value=400000,
            equity_details="0.4% over 4 years, 1-year cliff",
            total_comp=300000,
            pto_days=25,
            health_insurance="Full coverage, no premium",
            retirement_match="4% 401k match",
            remote_policy="Remote",
            status="Pending",
            notes="Waiting on written offer letter.",
        ))

db.commit()
db.close()

print(f"Demo data seeded in {DATA_DIR}/job_applications.db")
print(f"  {len(apps_data)} applications across {len(companies_data)} companies")
