# Job Tracker Changelog

## Version 1.1.0 - Dark Mode & Enhanced Features

### UI Changes
✅ **Dark Mode Theme**
- Switched to dark color scheme with slate/blue palette
- Primary background: #0f172a (dark navy)
- Surface background: #1e293b (slate)
- Text colors optimized for dark background
- Enhanced contrast for better readability

### New Application Fields
✅ **Job Posting Tracking**
- `job_url` - Store URL of job posting

✅ **Document Tracking**
- `resume_filename` - Track which resume version was submitted
- `cover_letter_filename` - Track which cover letter was submitted

✅ **Contact Information**
- `hiring_manager_name` - Store hiring manager name
- `hiring_manager_email` - Store hiring manager email

### Priority System Updates
✅ **Enhanced Priority Levels**
- P1 - P5 

### Interview Tracking (New Feature)
✅ **Interview Management**
- New `interviews` table for tracking interviews
- Fields:
  - `scheduled_date` - When the interview is scheduled
  - `interview_type` - Phone, Video, On-site, Technical, Behavioral
  - `interviewer_name` - Name of interviewer
  - `interviewer_email` - Email of interviewer
  - `interviewer_title` - Title/role of interviewer
  - `location` - Physical location or meeting link
  - `meeting_link` - Video conference URL
  - `notes` - Interview preparation notes
  - `completed` - Yes/No tracking

✅ **API Endpoints**
- `GET /api/applications/{id}/interviews` - List interviews for application
- `POST /api/interviews` - Create new interview
- `PUT /api/interviews/{id}` - Update interview
- `DELETE /api/interviews/{id}` - Delete interview

### Database Schema Changes
- Removed old fields: `resume_version`, `cover_letter_sent`
- Added new fields: `resume_filename`, `cover_letter_filename`, `hiring_manager_name`, `hiring_manager_email`
- Added new table: `interviews`
- Updated relationships: Application → Interview (one-to-many)

### Technical Improvements
- Updated Pydantic models for new fields
- Enhanced CRUD operations for interviews
- Improved form layout and styling
- Better color accessibility in dark mode

## Version 1.0.0 - Initial Release
- FastAPI backend with SQLite
- Company and Application tracking
- Contact management
- Interaction logging
- Dashboard with statistics
- Web UI with CRUD operations
