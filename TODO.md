# Job Search Toolkit - TODO

**Last Updated:** March 18, 2026

---

## High Priority - Workflow Automation

### 🎯 Simplify Container Workflow (CRITICAL UX)
**Priority:** P1  
**Estimated Time:** 1-2 hours  
**Impact:** Prevents user confusion and errors  
**Status:** ✅ COMPLETED

**Problem:** Users may accidentally run scripts outside container, creating files in wrong location

**Tasks:**
- [x] Create wrapper script (`job-tracker`)
- [x] Make wrapper script executable
- [x] Add container detection to all scripts (warn if not in container)
- [x] Update README with wrapper script usage
- [x] Add SHELL_ALIASES.md documentation
- [x] Update all workflow documentation to use wrapper

**Testing:**
- [x] Test wrapper script with all commands
- [x] Test container detection warnings
- [x] Verify scripts fail gracefully outside container

**Scripts Updated with Container Detection:**
- [x] `scripts/create_application.sh`
- [x] `scripts/compile_application.sh`
- [x] `scripts/customize_application.sh`
- [x] `scripts/sync_applications.py`
- [x] `scripts/list_applications.sh`

**Documentation Updated:**
- [x] Created `job-tracker` wrapper script
- [x] Created `docs/SHELL_ALIASES.md` with 4 options
- [x] Updated README.md Quick Start section
- [x] Updated README.md Usage section

---

### 🚀 Script 1: Generate Customization Prompt (HIGH IMPACT)
**Priority:** P1  
**Estimated Time:** 1-1.5 hours  
**Time Saved Per Use:** ~8-10 minutes  

**Task:** Create `scripts/generate_customization_prompt.sh`

**Requirements:**
- [ ] Read application directory path as argument
- [ ] Load job_description.txt
- [ ] Load current resume.tex
- [ ] Load base_master_resume.tex (from templates/)
- [ ] Recursively load all source_material/*.md files
- [ ] Read RESUME_CUSTOMIZATION_PROMPT.md template
- [ ] Extract the prompt section (between triple backticks)
- [ ] Replace placeholders with actual content
- [ ] Output to `customization_prompt_filled.txt`
- [ ] Handle missing files gracefully (warn but continue)
- [ ] Add usage documentation in script header

**Testing:**
- [ ] Test with existing application
- [ ] Test with missing source_material (should warn)
- [ ] Verify output is ready to send to AI
- [ ] Test with special characters in files (quotes, backticks)

**Documentation:**
- [ ] Add to README.md workflow section
- [ ] Add to WORKFLOW_SUMMARY.md
- [ ] Update PROJECT_CONTEXT.md

---

### 🚀 Script 2: Parse AI Response (HIGH IMPACT)
**Priority:** P1  
**Estimated Time:** 1-1.5 hours  
**Time Saved Per Use:** ~2 minutes  

**Task:** Create `scripts/parse_ai_response.sh`

**Requirements:**
- [ ] Read AI response file path as argument
- [ ] Read application directory path as argument
- [ ] Extract SECTION 1 (resume.tex) - between ```latex markers
- [ ] Extract SECTION 2 (cover_letter.tex) - between ```latex markers
- [ ] Extract SECTION 3 (review_prompt.txt) - full text content
- [ ] Save each section to appropriate file
- [ ] Validate LaTeX content compiles (optional warning)
- [ ] Handle malformed AI responses gracefully
- [ ] Add usage documentation in script header

**Testing:**
- [ ] Test with sample AI response
- [ ] Test with malformed response (missing sections)
- [ ] Test with various AI response formats
- [ ] Verify extracted LaTeX compiles correctly

**Documentation:**
- [ ] Add to README.md workflow section
- [ ] Add to WORKFLOW_SUMMARY.md
- [ ] Update PROJECT_CONTEXT.md

---

### 🚀 Script 3: End-to-End Automation Helper (CONVENIENCE)
**Priority:** P2  
**Estimated Time:** 30 minutes  
**Time Saved Per Use:** ~10-12 minutes  

**Task:** Create `scripts/customize_application_automated.sh`

**Requirements:**
- [ ] Read application directory path as argument
- [ ] Step 1: Call generate_customization_prompt.sh
- [ ] Step 2: Display instructions for AI assistant
- [ ] Step 3: Pause for user to save AI response
- [ ] Step 4: Call parse_ai_response.sh
- [ ] Step 5: Call compile_application.sh
- [ ] Step 6: Display next steps (review, ATS scoring)
- [ ] Add colored output for better UX
- [ ] Add progress indicators

**Testing:**
- [ ] Full end-to-end test with real application
- [ ] Test error handling at each step
- [ ] Verify workflow matches documentation

**Documentation:**
- [ ] Add to README.md as recommended workflow
- [ ] Add to WORKFLOW_SUMMARY.md

---

## Medium Priority - Documentation & Usability

### 📚 Update README.md
**Priority:** P2  
**Estimated Time:** 30 minutes  

**Tasks:**
- [ ] Add section on AI-assisted workflow
- [ ] Document new scripts (generate_customization_prompt.sh, parse_ai_response.sh)
- [ ] Add quick start guide with AI assistance
- [ ] Link to RESUME_CUSTOMIZATION_PROMPT.md and RESUME_REVIEW_PROMPT.md
- [ ] Add source_material/ directory documentation
- [ ] Update workflow section with time estimates

---

### 📚 Create Source Material Templates
**Priority:** P2  
**Estimated Time:** 1 hour  

**Task:** Create example templates in `docs/source_material_templates/`

**Files to Create:**
- [ ] `experience_template.md` - STAR format template
- [ ] `achievement_template.md` - Achievement documentation template
- [ ] `skill_template.md` - Skill documentation template
- [ ] `project_template.md` - Project documentation template
- [ ] `README.md` - Guide on using templates

**Documentation:**
- [ ] Link from RESUME_CUSTOMIZATION_PROMPT.md
- [ ] Add to PROJECT_CONTEXT.md

---

### 🎯 Feature: ATS Score Tracking (ANALYTICS VALUE)
**Priority:** P2 (moved up - high analytical value)  
**Estimated Time:** 4-6 hours  

**Task:** Add ATS score tracking to database and application table

**Database Changes:**
- [ ] Add `ats_score` column to `applications` table (INTEGER, nullable)
- [ ] Add `ats_score_date` column to `applications` table (DATETIME, nullable)
- [ ] Add `ats_keywords_matched` column (TEXT, nullable - JSON array)
- [ ] Add `ats_keywords_missing` column (TEXT, nullable - JSON array)
- [ ] Optional: Create `ats_score_history` table for tracking iterations
  - id, application_id, score, date, version, keywords_matched, keywords_missing, notes

**API Endpoints:**
- [ ] `PUT /api/applications/{id}/ats-score` - Update ATS score
- [ ] `GET /api/applications/{id}/ats-history` - Get score history (if tracking iterations)
- [ ] `GET /api/analytics/ats-correlation` - Analyze score vs callback rate

**UI Changes:**
- [ ] Add "ATS Score" column to applications table (sortable, filterable)
- [ ] Color coding: 
  - 90-100: Green (Excellent)
  - 80-89: Blue (Good)
  - 70-79: Yellow (Fair)
  - <70: Red (Poor)
- [ ] Add ATS score input field in application detail/edit view
- [ ] Display keyword match/missing in application detail
- [ ] Add filter: "Min ATS Score: [slider 0-100]"
- [ ] Dashboard widget: Average ATS score by status
- [ ] Analytics page: ATS Score vs Callback Rate chart

**Analytics Features:**
- [ ] Calculate callback rate by ATS score range:
  - 90-100: X% callback rate
  - 80-89: Y% callback rate
  - 70-79: Z% callback rate
  - <70: W% callback rate
- [ ] Show correlation: "Applications with ATS score >85 have 2.3x higher callback rate"
- [ ] Identify optimal score threshold for your profile
- [ ] Track score improvements over time

**Workflow Integration:**
- [ ] After running review prompt, manually enter ATS score in UI
- [ ] Future: Auto-parse ATS score from AI response
- [ ] Future: API integration to auto-save score

**Benefits:**
- **Data-driven insights**: See what ATS score actually correlates with interviews
- **Optimize effort**: Know when to stop iterating (diminishing returns)
- **Track improvements**: See if your source material quality is improving
- **Compare strategies**: Which template/approach yields better scores
- **Identify patterns**: Certain companies/roles require higher scores?

**Example Insights:**
- "Your applications with ATS score >82 have a 35% callback rate vs 8% below 82"
- "Engineering Manager roles: avg score 78, avg callback rate 22%"
- "Developer roles: avg score 85, avg callback rate 31%"
- "Your ATS scores improved 12 points on average over 3 months"

**Migration Strategy:**
- [ ] Add columns with ALTER TABLE (nullable for existing data)
- [ ] Existing applications will show "N/A" for ATS score
- [ ] Going forward, track for all new applications

---

### 🎨 UI Enhancement: Auto-open PDFs After Compilation
**Priority:** P3  
**Estimated Time:** 15 minutes  

**Task:** Update `scripts/compile_application.sh`

**Requirements:**
- [ ] Add optional `--open` flag
- [ ] Detect OS (macOS, Linux, Windows)
- [ ] Use appropriate PDF viewer command:
  - macOS: `open`
  - Linux: `xdg-open`
  - Windows: `start`
- [ ] Only open if compilation succeeds

---

## Low Priority - Future Enhancements

### 🔮 Web UI: AI Integration Button
**Priority:** P4  
**Estimated Time:** 8-12 hours  

**Task:** Add "Customize with AI" button to application detail view

**Requirements:**
- [ ] Add button to application view in UI
- [ ] Create backend endpoint `/api/applications/{id}/generate-customization-prompt`
- [ ] Return pre-filled prompt as JSON
- [ ] Add textarea for pasting AI response
- [ ] Create endpoint `/api/applications/{id}/parse-ai-response`
- [ ] Auto-save parsed resume.tex and cover_letter.tex
- [ ] Auto-compile PDFs
- [ ] Display success/error messages
- [ ] Add loading indicators

**Dependencies:**
- Requires Scripts 1 & 2 to be working
- May require frontend framework (or significant vanilla JS)

---

### 🔮 Web UI: Source Material Editor
**Priority:** P4  
**Estimated Time:** 16-20 hours  

**Task:** Create web-based interface for managing source_material/

**Features:**
- [ ] List all source material files
- [ ] Create new files from templates
- [ ] Edit files with Markdown preview
- [ ] WYSIWYG editor option
- [ ] Search/filter by keywords
- [ ] Tag experiences (company, skill, technology)
- [ ] Version history
- [ ] Export to markdown

**Benefits:**
- Easier to maintain source material
- More likely to keep it up-to-date
- Better UX than editing files directly

---

### 🎯 Feature: ATS Score Tracking (ANALYTICS VALUE)
**Priority:** P2 (moved up - high analytical value)  
**Estimated Time:** 4-6 hours  

**Task:** Add ATS score tracking to database and application table

**Database Changes:**
- [ ] Add `ats_score` column to `applications` table (INTEGER, nullable)
- [ ] Add `ats_score_date` column to `applications` table (DATETIME, nullable)
- [ ] Add `ats_keywords_matched` column (TEXT, nullable - JSON array)
- [ ] Add `ats_keywords_missing` column (TEXT, nullable - JSON array)
- [ ] Optional: Create `ats_score_history` table for tracking iterations
  - id, application_id, score, date, version, keywords_matched, keywords_missing, notes

**API Endpoints:**
- [ ] `PUT /api/applications/{id}/ats-score` - Update ATS score
- [ ] `GET /api/applications/{id}/ats-history` - Get score history (if tracking iterations)
- [ ] `GET /api/analytics/ats-correlation` - Analyze score vs callback rate

**UI Changes:**
- [ ] Add "ATS Score" column to applications table (sortable, filterable)
- [ ] Color coding: 
  - 90-100: Green (Excellent)
  - 80-89: Blue (Good)
  - 70-79: Yellow (Fair)
  - <70: Red (Poor)
- [ ] Add ATS score input field in application detail/edit view
- [ ] Display keyword match/missing in application detail
- [ ] Add filter: "Min ATS Score: [slider 0-100]"
- [ ] Dashboard widget: Average ATS score by status
- [ ] Analytics page: ATS Score vs Callback Rate chart

**Analytics Features:**
- [ ] Calculate callback rate by ATS score range:
  - 90-100: X% callback rate
  - 80-89: Y% callback rate
  - 70-79: Z% callback rate
  - <70: W% callback rate
- [ ] Show correlation: "Applications with ATS score >85 have 2.3x higher callback rate"
- [ ] Identify optimal score threshold for your profile
- [ ] Track score improvements over time

**Workflow Integration:**
- [ ] After running review prompt, manually enter ATS score in UI
- [ ] Future: Auto-parse ATS score from AI response
- [ ] Future: API integration to auto-save score

**Benefits:**
- **Data-driven insights**: See what ATS score actually correlates with interviews
- **Optimize effort**: Know when to stop iterating (diminishing returns)
- **Track improvements**: See if your source material quality is improving
- **Compare strategies**: Which template/approach yields better scores
- **Identify patterns**: Certain companies/roles require higher scores?

**Example Insights:**
- "Your applications with ATS score >82 have a 35% callback rate vs 8% below 82"
- "Engineering Manager roles: avg score 78, avg callback rate 22%"
- "Developer roles: avg score 85, avg callback rate 31%"
- "Your ATS scores improved 12 points on average over 3 months"

**Migration Strategy:**
- [ ] Add columns with ALTER TABLE (nullable for existing data)
- [ ] Existing applications will show "N/A" for ATS score
- [ ] Going forward, track for all new applications

---

### 🔮 Feature: Resume Version History
**Priority:** P4  
**Estimated Time:** 6-8 hours  

**Task:** Track resume versions and changes

**Requirements:**
- [ ] Git integration for automatic commits
- [ ] Store snapshot of resume.tex on each compile
- [ ] Add `resume_versions` table
- [ ] UI to view version history
- [ ] Diff view between versions
- [ ] Restore previous version
- [ ] Tag versions (v1, v2, final, submitted)

**Benefits:**
- Roll back to previous versions
- Compare what changed between iterations
- A/B test different approaches

---

### 🔮 Advanced: Direct AI API Integration
**Priority:** P5  
**Estimated Time:** 20-30 hours  

**Task:** Call AI APIs directly from application

**Requirements:**
- [ ] Add API key configuration (OpenAI, Anthropic, etc.)
- [ ] Backend service to call AI APIs
- [ ] Streaming response support
- [ ] Cost tracking per application
- [ ] Rate limiting
- [ ] Error handling and retries
- [ ] Support multiple AI providers
- [ ] A/B testing different AI models

**Benefits:**
- No copy-paste workflow
- Real-time streaming results
- Batch processing
- Automated iteration based on ATS score

**Considerations:**
- API costs ($0.50-$2 per application estimated)
- Privacy concerns (sending data to external APIs)
- Need API keys management
- Complexity of implementation

---

## Bug Fixes & Technical Debt

### 🐛 Fix: LinkedIn Parser Disabled
**Priority:** P5 (Low - workaround exists)  
**Status:** Commented out due to automation detection  

**Options:**
1. Keep disabled (current workaround: manual entry)
2. Implement rate limiting and more human-like behavior
3. Use LinkedIn API if available
4. Remove feature entirely

**Decision:** Keep disabled for now, manual entry is acceptable

---

### 🧹 Technical Debt: Add Automated Tests
**Priority:** P3  
**Estimated Time:** 12-16 hours  

**Tasks:**
- [ ] Backend API tests (pytest)
  - Test all CRUD endpoints
  - Test DUA report generation
  - Test file operations
- [ ] Frontend tests (Playwright or Cypress)
  - Test application creation flow
  - Test interview calendar
  - Test offer comparison
- [ ] Script tests (bash)
  - Test create_application.sh
  - Test compile_application.sh
  - Test sync_applications.py
- [ ] Set up CI/CD pipeline

---

### 🧹 Technical Debt: Add Logging
**Priority:** P3  
**Estimated Time:** 2-3 hours  

**Tasks:**
- [ ] Configure Python logging (app.py, crud.py)
- [ ] Log levels: DEBUG, INFO, WARNING, ERROR
- [ ] Rotate log files
- [ ] Add logging to scripts
- [ ] Log AI customization attempts (success/failure)

---

### 🧹 Technical Debt: Error Handling
**Priority:** P3  
**Estimated Time:** 4-6 hours  

**Tasks:**
- [ ] Improve frontend error messages (more specific)
- [ ] Add validation on forms
- [ ] Handle LaTeX compilation errors gracefully
- [ ] Better error messages for missing files
- [ ] Add error tracking/reporting

---

## Completed ✅

### ✅ Pipeline Stat Card Filter (March 19, 2026)
**Added dedicated Pipeline stat card with click-to-filter functionality!**

**What's New:**
- New stat card showing Pipeline application count (between Total and Applied)
- Clickable card filters applications table to show only Pipeline status
- Visual distinction with purple funnel icon (Solarized violet theme)
- Active state highlighting when filter is enabled
- Toggle behavior - click again to clear filter

**Perfect for Bulk Scoring Workflow:**
- Click Pipeline card to see all jobs awaiting evaluation
- Verify which jobs need scoring before running bulk score
- Focus on unscored jobs when preparing applications
- Quick way to check Pipeline count at a glance

**UI Layout:**
```
[Total] [Pipeline] [Applied] [Screening] [Interviews] [Offers] [Rejected]
   0        2         6          1           3          0         2
```

**Files Modified:**
- `job_tracker/templates/index.html` - Added Pipeline stat card HTML
- `job_tracker/static/app.js` - Updated dashboard and filter logic
- `job_tracker/static/style.css` - Added Pipeline card styling

**Technical Implementation:**
- Reuses existing stat card filter infrastructure
- No API changes needed (dashboard already returns Pipeline count)
- Filter index mapping updated to include Pipeline at position 1
- Icon color customization for visual distinction

### ✅ Bulk Job Scoring System (March 19, 2026)
**Complete end-to-end scoring system for evaluating job fit!**

**Phase 1 - Database Migration:**
- Added Alembic for database migrations
- Created migration adding 6 new match scoring fields to applications table
- Fields: match_score, match_reasoning, match_strengths, match_gaps, match_recommendation, evaluated_at
- Added `migrate` command to job-tracker wrapper

**Phase 2 - Scoring Engine:**
- Created `job_tracker/scoring.py` module with JobScorer class
- Generates bulk scoring prompts with candidate background + job descriptions
- Parses AI responses (handles markdown-wrapped JSON)
- Loads resume summary and source material for context
- Returns database-ready format with timestamps
- Created comprehensive documentation in `docs/BULK_JOB_SCORING_PROMPT.md`

**Phase 3 - Backend API:**
- Added 3 new API endpoints:
  - `POST /api/applications/bulk-score` - Generate scoring prompt for Pipeline jobs
  - `POST /api/applications/parse-scores` - Parse AI response and update database
  - `POST /api/applications/{id}/score` - Score single application
- Updated Pydantic models to include match_score fields
- All endpoints tested and working

**Phase 4 - Frontend UI:**
- Added Actions dropdown menu replacing single "Add Application" button
- Created 3-step bulk scoring modal workflow
- Added Match Score column to applications table (between Role and Priority)
- Color-coded badges: Green (80-100), Blue (70-79), Yellow (60-69), Orange (50-59), Red (<50)
- Clickable badges show details (score, reasoning, strengths, gaps)
- Sortable match score column
- Added dropdown and badge styles to CSS
- Implemented complete JavaScript workflow handlers

**How It Works:**
1. User clicks "Actions" → "Score Pipeline Jobs"
2. System generates prompt with all Pipeline applications + candidate background
3. User copies prompt, pastes into Claude/ChatGPT/local LLM
4. AI returns JSON with scores, reasoning, strengths, gaps for each job
5. User pastes response back, system parses and updates database
6. Match scores appear in table with color-coded badges
7. Click badge to see full details

**Benefits:**
- **Time Savings:** Score 40 jobs in 30 minutes vs 5-10 hours manual review
- **Data-Driven:** Prioritize high-scoring matches
- **Strategic Insights:** Pattern recognition on what roles fit best
- **Focus Effort:** Customize only top-scoring applications

**Files Created/Modified:**
- Database: Added match_score fields via Alembic migration
- Backend: `job_tracker/scoring.py`, updated `job_tracker/app.py`, `job_tracker/models.py`
- Frontend: Updated `templates/index.html`, `static/style.css`, `static/app.js`
- Documentation: `docs/BULK_JOB_SCORING_PROMPT.md`
- Infrastructure: `alembic.ini`, `alembic/env.py`, `alembic/script.py.mako`

### ✅ Simplify Container Workflow (March 18, 2026)
- Created `job-tracker` wrapper script for easy command execution
- Added container detection to all scripts (prevents running outside container)
- Created comprehensive SHELL_ALIASES.md documentation
- Updated README with wrapper script usage
- All scripts now warn if run outside container with helpful guidance

### ✅ PDF File Filtering (March 18, 2026)
- Modified `/api/applications/{id}/pdfs` to only show `*.pdf` files

### ✅ Calendar View Expansion (March 18, 2026)
- Expanded from "Next 4 Weeks" to "Last 2 Weeks & Next 3 Weeks"

### ✅ Role Column Hyperlinks (March 18, 2026)
- Made role column clickable when job_url exists

### ✅ AI-Assisted Workflow Documentation (March 18, 2026)
- Created RESUME_CUSTOMIZATION_PROMPT.md
- Created RESUME_REVIEW_PROMPT.md
- Created WORKFLOW_SUMMARY.md
- Updated PROJECT_CONTEXT.md

---

## Ideas / Backlog (Not Prioritized)

### 💡 Browser Extension
- Quick capture job postings from LinkedIn, Indeed, etc.
- Auto-fill job_description.txt
- One-click application creation

### 💡 Email Integration
- Track email correspondences with companies
- Link emails to applications
- Auto-detect interview invitations

### 💡 Networking/Referral Tracking
- Track who referred you
- Follow-up reminders
- Thank you note templates

### 💡 Interview Prep Notes
- Question bank per company
- Answer templates
- STAR story library

### 💡 Salary Negotiation Assistant
- Compare offers with market data
- Negotiation script generator
- Counter-offer templates

### 💡 Job Board Integration
- Direct API integration with job boards
- Auto-import job postings
- Apply directly from UI

---

## Notes

### Development Environment
- Python 3.9+
- FastAPI
- SQLite
- Vanilla JavaScript (no build step)
- LaTeX (pdflatex)
- Docker

### Testing Strategy
- Manual testing for now
- Add automated tests as P3 priority
- Real-world usage validation

### Release Strategy
- Rolling deployment (no versioning yet)
- Document breaking changes in PROJECT_CONTEXT.md
- Keep backward compatibility where possible

---

## Time Estimates Summary

**High Priority (P1):** ~3-4 hours total
- Script 1: 1-1.5 hours
- Script 2: 1-1.5 hours
- Script 3: 0.5 hours

**Medium Priority (P2):** ~7-8 hours total
- Documentation updates: 0.5 hours
- Source material templates: 1 hour
- **ATS Score Tracking: 4-6 hours** ⭐ HIGH VALUE
- PDF auto-open: 0.25 hours

**Total immediate work:** ~10-12 hours for significant improvements
- Automation scripts: 40% workflow speedup
- ATS tracking: Data-driven application optimization

**ROI:** 
- Scripts pay for themselves after 10-15 applications
- ATS tracking provides ongoing strategic insights on what works

---

*This TODO file should be updated as tasks are completed or priorities change.*
