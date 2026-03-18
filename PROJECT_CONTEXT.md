# Job Search Toolkit - Project Context

**Last Updated:** March 18, 2026  
**Project Status:** Active Development  
**Primary Developer:** Tim Ireland

---

## Project Overview

Job Search Toolkit is a comprehensive web-based application tracking system designed to help job seekers manage their applications, generate customized resumes/cover letters using LaTeX, and track all aspects of their job search journey. The system combines a FastAPI backend with a vanilla JavaScript frontend and Docker-based deployment.

### Core Value Proposition
- **Separation of Code & Data**: Public codebase, private job search data
- **LaTeX-Based Documents**: Professional, version-controlled resumes/cover letters
- **Comprehensive Tracking**: Applications, interviews, offers, contacts, interactions
- **Compliance Support**: MA DUA (Department of Unemployment Assistance) reporting built-in

---

## Architecture

### Technology Stack
- **Backend**: Python 3.9+, FastAPI, SQLAlchemy, Uvicorn
- **Frontend**: Vanilla JavaScript (ES6+), HTML5, CSS3, Font Awesome icons
- **Database**: SQLite (portable, file-based)
- **Document Generation**: LaTeX (pdflatex), PDF metadata manipulation
- **Deployment**: Docker, docker-compose
- **OS Support**: Linux (Docker), macOS (native or Docker)

### Project Structure

```
job-search-toolkit/                    # Main repository (public)
├── job_tracker/                       # Web application
│   ├── app.py                        # FastAPI application (695 lines)
│   ├── crud.py                       # Database operations (379 lines)
│   ├── database.py                   # SQLAlchemy setup
│   ├── models.py                     # Pydantic models (258 lines)
│   ├── linkedin_parser.py            # LinkedIn job posting parser (commented out)
│   ├── create_app_db_entry.py        # CLI tool for DB entry creation
│   ├── templates/
│   │   └── index.html                # Main SPA shell
│   └── static/
│       ├── app.js                    # Main application logic (851 lines)
│       ├── interviews.js             # Interview/calendar logic (407 lines)
│       ├── offers.js                 # Offers comparison UI
│       └── style.css                 # Application styles
│
├── scripts/                          # Helper scripts
│   ├── create_application.sh         # Create new application directory
│   ├── customize_application.sh      # Helper for customization workflow
│   ├── compile_application.sh        # Compile LaTeX to PDF with metadata
│   ├── sync_applications.py          # Sync filesystem to database
│   ├── add_pdf_metadata.py           # Add metadata to PDFs
│   ├── read_pdf_metadata.py          # Read PDF metadata
│   └── export_weekly_activity.py     # DUA export script
│
├── templates/                        # LaTeX resume templates
│   ├── base_master_resume.tex
│   ├── base_master_cover_letter.tex
│   ├── manager_resume.tex
│   ├── manager_cover_letter.tex
│   ├── director_resume.tex
│   ├── director_cover_letter.tex
│   ├── senior_engineer_resume.tex
│   └── senior_engineer_cover_letter.tex
│
├── Dockerfile                        # Container definition
├── docker-compose.yml                # Service orchestration
├── docker-entrypoint.sh              # Container initialization
├── requirements.txt                  # Python dependencies
└── docs/                            # Documentation

../my-job-search-2026/               # User data directory (private)
├── applications/                    # Per-application directories
│   └── Company_JobTitle/
│       ├── config.txt               # Application metadata
│       ├── job_description.txt      # Job posting
│       ├── resume.tex               # Customized resume
│       ├── resume.pdf               # Compiled resume
│       ├── cover_letter.tex         # Customized cover letter
│       └── cover_letter.pdf         # Compiled cover letter
├── source_material/                 # Personal content (experiences, skills)
├── custom_templates/                # User-specific LaTeX templates
└── job_applications.db              # SQLite database
```

---

## Database Schema

### Tables
1. **companies**
   - id (PK), name, website, size, tech_stack, notes
   - created_at, updated_at

2. **applications**
   - id (PK), company_id (FK)
   - role, priority (P1-P4), status (Pipeline/Applied/Screening/Interview/Offer/etc.)
   - job_url, location, remote_policy, salary_range
   - resume_filename, cover_letter_filename
   - hiring_manager_name, hiring_manager_email
   - date_applied, date_screening, date_interview, date_offer, date_closed
   - notes, created_at, updated_at

3. **contacts**
   - id (PK), company_id (FK)
   - name, role, email, phone, linkedin, relationship, notes
   - created_at, updated_at

4. **interactions**
   - id (PK), application_id (FK)
   - type, contact_person, summary, next_steps, date
   - created_at

5. **interviews**
   - id (PK), application_id (FK)
   - scheduled_date, interview_type, interviewer_name, interviewer_email, interviewer_title
   - location, meeting_link, notes, completed (Yes/No/Cancelled)
   - created_at, updated_at

6. **offers**
   - id (PK), application_id (FK)
   - offer_date, response_deadline
   - base_salary, bonus_target, signing_bonus, equity_value, equity_details, total_comp
   - pto_days, sick_days, holidays
   - health_insurance, retirement_match, other_benefits
   - start_date, remote_policy, relocation_assistance
   - status (Pending/Accepted/Rejected/Withdrawn), notes
   - created_at, updated_at

### Key Relationships
- Company → Applications (1:N)
- Company → Contacts (1:N)
- Application → Interactions (1:N)
- Application → Interviews (1:N)
- Application → Offers (1:N)

---

## Key Features & Workflows

### 1. Application Management
**Workflow:**
1. User creates application via UI or CLI (`create_application.sh`)
2. System creates directory structure and copies LaTeX templates
3. Database entry created with company and application records
4. User fills in `job_description.txt` with job posting
5. User customizes `resume.tex` and `cover_letter.tex`
6. Compile PDFs with `compile_application.sh` or pdflatex directly
7. Track status changes: Pipeline → Applied → Screening → Interview → Offer

**Status Values:**
- Pipeline, Applied, Screening, Interview, Offer Received, Offer Accepted, Rejected, Withdrawn, Not Interested

**Priority Values:**
- P1 (Critical), P2 (High), P3 (Medium), P4 (Low)

### 2. Interview Scheduling & Calendar
**Features:**
- Add interviews with date/time, interviewer details, location/meeting link
- Calendar view showing interviews across 5 weeks (last 2 weeks + next 3 weeks)
- List view with filtering and sorting
- Mark interviews as completed/cancelled
- Visual indicators for today and past dates

**Recent Changes:**
- Expanded calendar from "next 4 weeks" to "last 2 weeks & next 3 weeks"

### 3. Offer Comparison
**Features:**
- Track detailed compensation: base, bonus, equity, benefits
- Side-by-side comparison view
- Calculate total compensation
- Track response deadlines
- Status: Pending, Accepted, Rejected, Withdrawn

### 4. PDF Management
**Features:**
- List PDF files in application directories
- View PDFs inline in browser
- Upload additional PDFs
- Add metadata to PDFs (company, role, version, source LaTeX file)

**Recent Changes:**
- File listing now filters to show only `*.pdf` files (excludes .tex, .aux, .log, etc.)

### 5. MA DUA Reporting
**Purpose:** Massachusetts Department of Unemployment Assistance requires weekly job search activity reports.

**Endpoints:**
- `/api/reports/dua-weekly` - Text format for previous week
- `/api/reports/dua-weekly-csv` - CSV format for previous week
- `/api/reports/dua-range` - Text format for date range
- `/api/reports/dua-range-csv` - CSV format for date range

**Export Includes:**
- Date, Position, Pay Rate, Employer, Contact Info, Result
- Captures: Applications, Screenings, Interviews, Offers, Rejections

### 6. LaTeX Resume Generation
**Template Types:**
- `base` - Standard resume
- `manager` - Engineering manager focus
- `director` - Executive-level
- `developer` - Senior engineer focus

**Compilation Process:**
1. Edit `.tex` files
2. Run `pdflatex` twice (resolves references)
3. Add metadata with `add_pdf_metadata.py`
4. Clean up auxiliary files (.aux, .log, .out)

---

## API Endpoints

### Companies
- `GET /api/companies` - List all companies
- `POST /api/companies` - Create company
- `GET /api/companies/{id}` - Get company details
- `PUT /api/companies/{id}` - Update company
- `DELETE /api/companies/{id}` - Delete company

### Applications
- `GET /api/applications` - List applications (with filtering)
- `POST /api/applications` - Create application
- `GET /api/applications/{id}` - Get application details
- `PUT /api/applications/{id}` - Update application
- `DELETE /api/applications/{id}` - Delete application
- `GET /api/applications/{id}/pdfs` - List PDF files (filtered to *.pdf only)
- `POST /api/applications/{id}/upload` - Upload file

### Contacts
- `GET /api/companies/{company_id}/contacts` - List company contacts
- `POST /api/contacts` - Create contact
- `PUT /api/contacts/{id}` - Update contact
- `DELETE /api/contacts/{id}` - Delete contact

### Interactions
- `GET /api/applications/{app_id}/interactions` - List interactions
- `POST /api/interactions` - Create interaction

### Interviews
- `GET /api/interviews` - List all interviews
- `GET /api/applications/{app_id}/interviews` - List application interviews
- `POST /api/interviews` - Create interview
- `GET /api/interviews/{id}` - Get interview details
- `PUT /api/interviews/{id}` - Update interview
- `DELETE /api/interviews/{id}` - Delete interview

### Offers
- `GET /api/offers` - List all offers
- `GET /api/applications/{app_id}/offers` - List application offers
- `POST /api/offers` - Create offer
- `PUT /api/offers/{id}` - Update offer
- `DELETE /api/offers/{id}` - Delete offer
- `GET /api/offers/compare` - Get offer comparison data

### Reports
- `GET /api/reports/dua-weekly` - Weekly DUA report (text)
- `GET /api/reports/dua-weekly-csv` - Weekly DUA report (CSV)
- `GET /api/reports/dua-range` - Date range DUA report (text)
- `GET /api/reports/dua-range-csv` - Date range DUA report (CSV)

### File Operations
- `GET /api/files/pdf/{file_path}` - View/download PDF

---

## Recent Changes & Improvements

### Session: March 17-18, 2026

1. **PDF File Filtering** (March 18)
   - Modified `/api/applications/{id}/pdfs` endpoint to only show `*.pdf` files
   - Previously showed all files (.tex, .aux, .log, etc.)
   - Changed filter from `not file_path.name.startswith('.')` to `file_path.suffix.lower() == '.pdf'`

2. **Calendar View Expansion** (March 18)
   - Expanded calendar from "Next 4 Weeks" to "Last 2 Weeks & Next 3 Weeks"
   - Changed loop from `w < 4` to `w < 5`
   - Adjusted start date to go back 2 weeks: `startOfWeek.setDate(startOfWeek.getDate() - (2 * 7))`
   - Updated header text to reflect new range

3. **Role Column Hyperlinks** (March 18)
   - Made role column in applications table a clickable hyperlink when `job_url` exists
   - Link opens in new tab with `target="_blank"`
   - Uses `event.stopPropagation()` to prevent row click event
   - Styled with underline to indicate it's a link

4. **Klaviyo Application Customization** (March 17)
   - Customized resume and cover letter for Klaviyo Engineering Manager position
   - Emphasized developer infrastructure, CI/CD optimization, platform engineering
   - Aligned with Klaviyo's pillars: speed, quality, AI enablement
   - Highlighted relevant experience: CI/CD transformation (86% build time reduction), AI-assisted development adoption, hands-on Python/TypeScript/Go

---

## Development Workflow

### Setting Up a New Application

```bash
# 1. Create application directory (in container or locally)
./scripts/create_application.sh "Company" "Job_Title" [template_type]

# Example:
./scripts/create_application.sh Klaviyo "Engineering_Manager" developer

# 2. Edit job_description.txt with actual job posting

# 3. Run customize helper (shows guidance)
./scripts/customize_application.sh Company_Job_Title

# 4. Customize resume.tex and cover_letter.tex
# - Can use AI assistance (GitHub Copilot, LLMs)
# - Tailor to job description keywords and requirements

# 5. Compile PDFs
./scripts/compile_application.sh Company_Job_Title
# Or manually:
cd applications/Company_Job_Title
pdflatex resume.tex && pdflatex resume.tex
pdflatex cover_letter.tex && pdflatex cover_letter.tex

# 6. Track in web UI at http://localhost:8000
```

### Syncing Filesystem to Database

```bash
# If applications exist in filesystem but not in database:
python scripts/sync_applications.py
```

### Docker Development

```bash
# Start container
docker-compose up -d

# Access shell
docker-compose exec job-tracker bash

# View logs
docker-compose logs -f job-tracker

# Restart after code changes
docker-compose restart job-tracker

# Stop
docker-compose down
```

### Data Directory Mapping
- Docker maps external directory to `/data` inside container
- Example: `../my-job-search-2026:/data`
- Environment variable `DATA_DIR` controls path
- Applications stored at `${DATA_DIR}/applications/`
- Database at `${DATA_DIR}/job_applications.db`

---

## Frontend Architecture

### Single Page Application (SPA)
- All functionality in single `index.html` page
- Navigation via tabs: Dashboard, Applications, Companies, Interviews, Offers
- Modals for create/edit operations
- Client-side rendering with vanilla JavaScript

### Key JavaScript Modules
1. **app.js** (851 lines) - Main application logic
   - Application CRUD operations
   - Company management
   - Contact management
   - Tab navigation
   - Dashboard statistics
   - Filter/sort functionality
   - Recently made role column clickable when job_url exists

2. **interviews.js** (407 lines) - Interview scheduling
   - List view and calendar view toggle
   - Calendar displays 5 weeks (last 2 weeks + next 3 weeks)
   - Interview CRUD operations
   - Date/time formatting

3. **offers.js** - Offer tracking and comparison
   - Offer CRUD operations
   - Side-by-side comparison view
   - Compensation calculations

### State Management
- Global variables for data caching (`applications`, `companies`, `contacts`, `interviews`, `offers`)
- Periodic refresh on data mutations
- No framework - uses vanilla DOM manipulation

### UI Patterns
- Modal dialogs for forms
- Click outside modal to close
- Stop propagation for nested clickable elements (links, buttons inside table rows)
- Badge system for status/priority visualization
- Font Awesome icons throughout

---

## Backend Architecture

### FastAPI Application (app.py)

**Key Features:**
- CORS enabled for local development
- Serves static files and SPA
- RESTful API design
- Path parameters and query parameters for filtering
- File upload support (multipart/form-data)

**Notable Endpoints:**
- Static file serving: `/`, `/static/*`, `/api/files/pdf/{file_path}`
- CRUD endpoints for all entities
- Report generation with multiple formats (text, CSV)
- PDF listing filtered to `*.pdf` files only

### Database Layer (crud.py)

**Design Patterns:**
- Session-based transactions
- Eager loading with `joinedload()` for related entities
- Timestamp tracking (created_at, updated_at)
- Soft deletes not implemented (hard deletes)

**Key Functions:**
- CRUD operations for all entities
- `get_dashboard_stats()` - Summary statistics
- `get_applications_with_activity()` - DUA report data generation
- `get_offer_comparison()` - Multi-offer analysis

---

## LaTeX Document System

### Template Philosophy
- Master templates stored in repo's `templates/` directory
- Copied to application directory on creation
- User customizes per-application
- Version controlled in data directory (private git repo)

### Template Variables
- Placeholders: `{[}Company Name{]}`, `{[}specific technology{]}`
- Customization done by AI or manual editing
- Compilation produces final PDFs

### Compilation Process
1. Run `pdflatex` twice (first pass, then resolve references)
2. Add metadata with Python script:
   - Company name
   - Role
   - Resume version (timestamp)
   - Source .tex filename
3. Clean up auxiliary files (.aux, .log, .out)

### Metadata Usage
- Embedded in PDF for tracking
- Extractable with `read_pdf_metadata.py`
- Useful for version control and organization

---

## Known Issues & Limitations

### Functional Issues
1. **LinkedIn Parser**: Commented out due to automation detection flags
2. **Sync Script**: May have issues with spaces in role names (recently fixed)
3. **Template Discovery**: Checks multiple paths for template location (Docker vs local)

### Technical Debt
1. No automated tests (pytest setup exists but no test files)
2. No code linting configuration
3. Frontend has no build system (vanilla JS)
4. No TypeScript for type safety
5. Error handling could be more robust
6. No authentication/authorization (single-user assumption)

### Future Enhancements Needed
- [ ] Automated testing (backend and frontend)
- [ ] Better error handling and user feedback
- [ ] Bulk operations (delete, status change)
- [ ] Search functionality across applications
- [ ] Tags/labels system
- [ ] Document versioning/history
- [ ] Email integration (track correspondences)
- [ ] Browser extension for quick job capture
- [ ] Mobile-responsive improvements
- [ ] Export to other formats (JSON, Word)
- [ ] Interview preparation notes/questions
- [ ] Networking/referral tracking

---

## Development Context

### Current Focus
The tool is being actively used for real job search with ongoing refinements based on actual usage patterns.

### Design Decisions

**Why SQLite?**
- Portable, file-based (easy backups)
- No server management
- Sufficient for single-user workload
- Can migrate to PostgreSQL if needed

**Why Vanilla JS?**
- No build step complexity
- Fast development iteration
- Minimal dependencies
- Suitable for project scale

**Why LaTeX?**
- Professional document quality
- Version control friendly (text-based)
- Precise layout control
- Industry standard for technical resumes

**Why Docker?**
- Consistent LaTeX environment
- Easy deployment across machines
- Isolates dependencies
- Works on any OS

### Coding Conventions
- Python: PEP 8 style (no strict enforcement)
- JavaScript: ES6+, camelCase naming
- Bash: Defensive scripting with error checking
- Comments: Minimal, only where needed for clarity

---

## Dependencies

### Python (requirements.txt)
- fastapi - Web framework
- uvicorn - ASGI server
- sqlalchemy - ORM
- pydantic - Data validation
- python-multipart - File upload support
- aiofiles - Async file operations
- PyPDF2 - PDF manipulation

### System (Dockerfile)
- Ubuntu base image
- texlive-latex-base, texlive-latex-extra - LaTeX
- poppler-utils - PDF utilities
- Python 3.9+

### JavaScript
- No npm dependencies
- Uses CDN for Font Awesome icons
- Pure ES6+ features

---

## Testing Strategy

### Current State
- No automated tests currently
- Manual testing during development
- Real-world usage validation

### Recommended Testing Approach
1. **Backend**: pytest with FastAPI test client
2. **Database**: Test CRUD operations, complex queries
3. **LaTeX**: Test template compilation
4. **Scripts**: Test create/compile/sync workflows
5. **Frontend**: Consider Playwright or Cypress for E2E tests

---

## Deployment Notes

### Docker Compose Configuration
```yaml
services:
  job-tracker:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ${DATA_PATH:-../my-job-search}:/data
    environment:
      - DATA_DIR=/data
```

### Volume Mounting
- Maps host data directory to `/data` in container
- Persistent across container restarts
- Allows external editing of .tex files

### Port Mapping
- Container: 8000
- Host: 8000
- Uvicorn serves on 0.0.0.0:8000 inside container

---

## Git History Highlights

Recent commits (newest first):
- `64a0c08` - Only show PDF files (March 18)
- `3114736` - Fix parsing issues
- `41094a2` - Add PDF file upload
- `770dc94` - Fix sync-apps spaces in role name
- `2793a90` - Use mounted data directory in create script
- `c3c9d2c` - Add Applied Jobs filter tab
- `5e9b269` - Click outside modal to close
- `a648aa6` - Fix duplicate record issue
- `846c8a2` - Comment out LinkedIn import (automation flagging)
- `604f1fb` - Add MA DUA weekly activity export
- `058f4a9` - Initial commit

---

## Security & Privacy Considerations

### Data Separation
- Code repository is public (or can be)
- Data directory must remain private
- No credentials in code
- Database uses local file (no network exposure)

### Sensitive Data
- Personal information (email, phone)
- Salary expectations and offers
- Interview notes and feedback
- Company contacts and relationships

### Recommendations
- Keep data directory in private git repo (separate from code)
- Regular backups of SQLite database
- Don't commit data directory to public repos
- Consider encrypting data directory at rest
- Use environment variables for any API keys (if added)

---

## Common Operations

### View Application Files in Browser
1. Navigate to Applications tab
2. Click on application row
3. View details modal shows PDF files
4. Click file name to view inline

### Generate Resume for New Application
```bash
# In container
cd /data/applications/Company_JobTitle
pdflatex resume.tex && pdflatex resume.tex

# Add metadata
python /app/scripts/add_pdf_metadata.py resume.pdf \
  --company "Company" \
  --role "Job Title" \
  --resume-version "20260318-1200"
```

### Export Weekly Activity
```bash
# Via web UI: Reports → DUA Export → Select week

# Via API:
curl http://localhost:8000/api/reports/dua-weekly > this_week.txt
curl http://localhost:8000/api/reports/dua-weekly-csv > this_week.csv
```

### Sync New Applications
```bash
# When creating apps manually in filesystem
docker-compose exec job-tracker python scripts/sync_applications.py
```

---

## Technical Notes

### LaTeX Compilation Issues
- Run pdflatex twice to resolve references
- Suppress warnings for font substitution (silence package)
- Clean up auxiliary files to avoid bloat
- Use `-interaction=nonstopmode` to avoid hanging on errors

### Database Migrations
- No migration framework currently (Alembic not used)
- Schema changes require manual SQL or recreation
- Consider adding Alembic for production use

### File Path Handling
- Use `pathlib.Path` for cross-platform compatibility
- Relative paths based on `DATA_DIR` environment variable
- Handle both Docker (`/data`) and local (`./data`) paths

### Frontend State Synchronization
- Data loaded on page load and tab switches
- Mutations trigger reload of affected data
- No WebSocket/SSE for real-time updates (not needed for single-user)

---

## Troubleshooting

### Application Directory Empty
**Symptom:** Directory exists but has no files  
**Cause:** `create_application.sh` failed or wasn't run  
**Fix:** Delete directory and re-run create script

### PDFs Not Showing
**Symptom:** PDF files exist but don't appear in UI  
**Cause:** Was showing all files, now filtered to `*.pdf`  
**Fix:** Ensure files have `.pdf` extension (lowercase check)

### Database Out of Sync
**Symptom:** Applications in filesystem not in database  
**Cause:** Manual file creation or migration  
**Fix:** Run `python scripts/sync_applications.py`

### LaTeX Compilation Fails
**Symptom:** `pdflatex` errors or hangs  
**Cause:** Syntax errors in .tex file, missing packages  
**Fix:** Check .log file, run with `-interaction=nonstopmode`, install missing packages

---

## Performance Characteristics

### Scalability
- **Applications**: Tested with dozens, should handle hundreds easily
- **Database**: SQLite adequate for single-user, thousands of records
- **PDF Generation**: 1-2 seconds per document
- **File Listing**: O(n) directory scan, fast for typical use

### Bottlenecks
- LaTeX compilation is CPU-bound (not parallelized)
- Large PDF viewing (>10MB) may be slow in browser
- No pagination on frontend (loads all data)

---

## Code Quality Notes

### Strengths
- Clear separation of concerns (routes, CRUD, models)
- Consistent naming conventions
- Good error handling in backend
- Readable, maintainable code

### Areas for Improvement
- Add input validation on frontend
- More robust error messages
- Add logging (currently minimal)
- Consider adding TypeScript
- Add automated tests
- Extract configuration to proper config files

---

## Future Architecture Considerations

### If Scaling to Multi-User
1. Add authentication (OAuth, JWT)
2. Row-level security in database
3. User-specific data directories
4. PostgreSQL instead of SQLite
5. Session management
6. Rate limiting

### If Adding CI/CD
1. Automated testing on PR
2. Docker image publishing
3. Linting enforcement
4. Security scanning
5. Automated versioning

### If Adding More Features
1. Consider frontend framework (React, Vue)
2. Add state management (Redux, Vuex)
3. Implement WebSocket for real-time updates
4. Add caching layer (Redis)
5. Microservices for document generation

---

## Useful Commands

```bash
# View database schema
sqlite3 /data/job_applications.db ".schema"

# Count applications by status
sqlite3 /data/job_applications.db "SELECT status, COUNT(*) FROM applications GROUP BY status;"

# Find application by company
sqlite3 /data/job_applications.db "SELECT * FROM applications WHERE company_id IN (SELECT id FROM companies WHERE name LIKE '%Company%');"

# List all PDFs
find /data/applications -name "*.pdf" -type f

# Bulk compile all applications
for dir in /data/applications/*/; do
  cd "$dir" && pdflatex -interaction=nonstopmode resume.tex > /dev/null 2>&1
done

# Check container status
docker-compose ps

# View API docs
open http://localhost:8000/docs
```

---

## Lessons Learned

1. **Data Separation is Key**: Keeping code and data separate allows public sharing of tool while keeping job search private
2. **LaTeX Advantages**: Version control, professional quality, customization flexibility
3. **Docker Simplifies Setup**: Especially for LaTeX dependencies
4. **Vanilla JS is Sufficient**: No need for React/Vue for this project scale
5. **SQLite is Adequate**: For single-user, file-based DB works great
6. **Metadata Matters**: PDF metadata helps with organization and tracking
7. **Automation Helps**: Scripts reduce manual work and errors
8. **Real Usage Drives Features**: MA DUA export added based on actual need

---

## Contact & Maintenance

**Primary Maintainer:** Tim Ireland  
**Repository:** (Your GitHub URL here)  
**License:** MIT  
**Last Major Update:** March 2026

---

## Appendix: File Formats

### config.txt
```
# Application Configuration
Company: Klaviyo
Job Title: Engineering Manager
Template Type: developer
Date Created: 2026-03-17
Status: Pipeline
Company ID: 123
Application ID: 456
```

### job_description.txt
Plain text format containing:
- Company information
- Role description
- Responsibilities
- Requirements
- Nice to have
- Benefits
- Location and remote policy

### Database Schema (SQLite)
See section "Database Schema" above for detailed table structures.

---

*This context document should be updated as the project evolves. Include it in AI assistant context when making significant changes or additions to the project.*
