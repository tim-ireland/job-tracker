# Massachusetts DUA Weekly Activity Export

This guide explains how to export your job search activity for reporting to the Massachusetts Department of Unemployment Assistance (DUA).

## Overview

The job tracker includes specialized endpoints that format your job application activity according to Massachusetts DUA requirements. Reports can be generated in both text and CSV formats.

### What Gets Exported

The export captures ALL job search activities that progressed during a specified time period:

- **Applications submitted** - When you applied to a position (`date_applied`)
- **Phone screenings** - When you received a screening call (`date_screening`)
- **Interviews** - When you had an interview (`date_interview`)
- **Offers received** - When you received a job offer (`date_offer`)
- **Applications closed** - When an application was rejected, withdrawn, or accepted (`date_closed`)

### Report Format

Each activity entry includes the following information in the format required by MA DUA:

```
Date: Position Pay_rate Employer_name_and_address Job_ID_or_person_contacted Contact_email_website_or_phone Result
```

**Example:**
```
Week starting Sunday 03/09/2026 through Saturday 03/15/2026:

03/10/2026: Senior Software Engineer $120k-150k Acme Corp https://acme.com John Smith john.smith@acme.com Applied
03/12/2026: Backend Developer $100k-130k TechStart Inc https://techstart.io Application #42 recruiter@techstart.io Screening
03/14/2026: Full Stack Engineer Not specified Innovate LLC Boston, MA Applied via LinkedIn https://linkedin.com/jobs/123 Interview
```

## Usage Methods

### Method 1: Web Browser

Simply navigate to the following URLs in your browser:

**Text format (previous week):**
```
http://localhost:8000/api/reports/dua-weekly
```

**CSV format (previous week):**
```
http://localhost:8000/api/reports/dua-weekly-csv
```

**Specific week (text format):**
```
http://localhost:8000/api/reports/dua-weekly?week_start=2026-03-09
```

**Date range (text format):**
```
http://localhost:8000/api/reports/dua-range?start_date=2026-02-01&end_date=2026-03-31
```

### Method 2: Command Line (curl)

#### Export Previous Week

Text format:
```bash
curl http://localhost:8000/api/reports/dua-weekly
```

CSV format:
```bash
curl http://localhost:8000/api/reports/dua-weekly-csv -o weekly_report.csv
```

#### Export Specific Week

The `week_start` parameter should be a Sunday in YYYY-MM-DD format:

```bash
# Text format
curl "http://localhost:8000/api/reports/dua-weekly?week_start=2026-03-09"

# CSV format
curl "http://localhost:8000/api/reports/dua-weekly-csv?week_start=2026-03-09" -o report.csv
```

#### Export Date Range

Get all activities within a custom date range (broken down by week):

```bash
# Text format
curl "http://localhost:8000/api/reports/dua-range?start_date=2026-02-01&end_date=2026-03-31"

# CSV format
curl "http://localhost:8000/api/reports/dua-range-csv?start_date=2026-02-01&end_date=2026-03-31" -o range_report.csv
```

### Method 3: Python Script

Use the included Python script for more convenient exporting:

```bash
# Export previous week (text)
python scripts/export_weekly_activity.py

# Export specific week (CSV)
python scripts/export_weekly_activity.py --week-start 2026-03-09 --format csv --output report.csv

# Export date range
python scripts/export_weekly_activity.py --start-date 2026-02-01 --end-date 2026-03-31

# Export date range (CSV)
python scripts/export_weekly_activity.py --start-date 2026-02-01 --end-date 2026-03-31 --format csv --output report.csv
```

### Method 4: Docker

If using Docker:

```bash
# Export previous week
docker-compose exec job-tracker curl http://localhost:8000/api/reports/dua-weekly

# Save to file
docker-compose exec job-tracker curl http://localhost:8000/api/reports/dua-weekly-csv -o /data/weekly_report.csv
```

## Week Calculation

Weeks run from **Sunday through Saturday** as required by Massachusetts DUA.

- If no week is specified, the system defaults to the **previous completed week**
- If you specify a date that isn't a Sunday, the system automatically adjusts to the Sunday of that week
- Date ranges are broken down into individual weeks for easier review

## Important Notes

### Data Requirements

For the most complete and useful reports, make sure to track:

1. **Application dates** - Set `date_applied` when you submit an application
2. **Status transitions** - The system automatically tracks when you move applications to different statuses:
   - Moving to "Applied" → sets `date_applied`
   - Moving to "Screening" → sets `date_screening`
   - Moving to "Interview" → sets `date_interview`
   - Moving to "Offer" → sets `date_offer`
   - Moving to "Rejected", "Withdrawn", or "Accepted" → sets `date_closed`

3. **Contact information** - Include:
   - Hiring manager name and email in the application
   - Company website
   - Job URLs
   - Contact information in the company record

4. **Salary information** - Enter salary range when available

### CSV vs Text Format

- **Text format** is human-readable and can be copied/pasted directly
- **CSV format** can be:
  - Opened in Excel or Google Sheets
  - Imported into other systems
  - Easier to review with multiple weeks of data

Check with your local unemployment office to confirm if they accept CSV uploads. If not, use the text format.

### Timing Tips

- **Run reports weekly** to stay current with your unemployment reporting
- **Keep dated backups** of your reports in case you need to reference them later
- **Review before submitting** to ensure all activity is captured and formatted correctly

## Troubleshooting

### No activities showing up

1. Check that you're using the correct date range
2. Verify that your applications have the appropriate date fields set
3. Remember: only applications where activity *occurred* during the week will show up

### Dates are off by one

Make sure you're using the Sunday that starts the week, not the Saturday that ends it.

### Missing contact information

The export uses this priority for contact information:
1. Hiring manager email from application
2. Contact email from company contacts
3. Company website
4. Job URL

Add missing information to get more complete reports.

## Example Workflow

1. **Track your activities throughout the week** using the web interface
   - Add applications when you apply
   - Update status when you get callbacks
   - Record interviews and outcomes

2. **Every week (usually Monday)**, generate your report:
   ```bash
   python scripts/export_weekly_activity.py --format text
   ```

3. **Review the report** to ensure accuracy

4. **Submit to Massachusetts DUA** according to their instructions

5. **Archive the report** for your records:
   ```bash
   python scripts/export_weekly_activity.py --format csv --output ~/Documents/DUA/report_$(date +%Y%m%d).csv
   ```

## API Reference

### GET /api/reports/dua-weekly

Export previous week's activity in text format.

**Query Parameters:**
- `week_start` (optional): Sunday date in YYYY-MM-DD format

**Response:** Plain text report

---

### GET /api/reports/dua-weekly-csv

Export previous week's activity in CSV format.

**Query Parameters:**
- `week_start` (optional): Sunday date in YYYY-MM-DD format

**Response:** CSV file download

---

### GET /api/reports/dua-range

Export activity for a date range, broken down by week.

**Query Parameters:**
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format

**Response:** Plain text report

---

### GET /api/reports/dua-range-csv

Export activity for a date range in CSV format, broken down by week.

**Query Parameters:**
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format

**Response:** CSV file download

## Support

For questions or issues with the export feature:
1. Check this documentation
2. Review the API documentation at http://localhost:8000/docs
3. Open an issue on GitHub
