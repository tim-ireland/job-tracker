# Job Search Toolkit - TODO

**Last Updated:** March 18, 2026

---

## High Priority - Workflow Automation

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

### 🔮 Feature: ATS Score Tracking
**Priority:** P4  
**Estimated Time:** 4-6 hours  

**Task:** Add ATS score tracking to database

**Requirements:**
- [ ] Add `ats_scores` table to database
  - application_id, score, date, keywords_matched, keywords_missing, notes
- [ ] Add API endpoints for CRUD operations
- [ ] Add UI section to application detail view
- [ ] Chart showing score history over iterations
- [ ] Display keyword match analysis
- [ ] Export scores to CSV

**Benefits:**
- Track improvements over time
- Compare scores across applications
- Identify patterns in successful applications

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

**Medium Priority (P2):** ~2 hours total
- Documentation updates: 0.5 hours
- Source material templates: 1 hour
- PDF auto-open: 0.25 hours

**Total immediate work:** ~5-6 hours for 40% workflow speedup

**ROI:** Scripts pay for themselves after 10-15 applications

---

*This TODO file should be updated as tasks are completed or priorities change.*
