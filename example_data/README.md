# Example Data

This directory contains example data to help you get started with the Job Search Toolkit.

## Directory Structure

When you mount a data volume for the first time, the following structure will be created:

```
/data/
├── applications/           # Your job applications
│   └── Example_Company_Software_Engineer/
│       ├── job_description.txt
│       ├── config.txt
│       ├── resume.tex
│       ├── resume.pdf
│       ├── cover_letter.tex
│       └── cover_letter.pdf
├── source_material/       # Your personal resume content
│   ├── experience.tex
│   ├── skills.tex
│   ├── education.tex
│   └── projects.tex
├── custom_templates/      # Custom LaTeX templates (optional)
├── job_applications.db    # SQLite database
└── .initialized          # Marker file (auto-created)
```

## Application Directory Format

Each application should follow this naming convention:
```
CompanyName_JobTitle_With_Underscores/
```

Examples:
- `Google_Senior_Software_Engineer/`
- `Microsoft_Engineering_Manager/`
- `Startup_Inc_Full_Stack_Developer/`

## Configuration File (config.txt)

Each application directory should contain a `config.txt` file:

```
template: base
priority: P3
status: Pipeline
location: Remote
remote_policy: Fully Remote
salary_range: $120k-180k
```

### Available Options:

**Templates:**
- `base` - Standard resume format
- `manager` - Management-focused resume
- `director` - Executive-level resume

**Priorities:**
- `P1` - Dream job, highest priority
- `P2` - Very interested
- `P3` - Interested
- `P4` - Backup option
- `P5` - Low priority

**Status:**
- `Pipeline` - Identified, not yet applied
- `Applied` - Application submitted
- `Screening` - Phone/initial screening
- `Interview` - In interview process
- `Offer` - Offer received
- `Accepted` - Offer accepted
- `Rejected` - Application rejected
- `Withdrawn` - You withdrew

## Job Description File

The `job_description.txt` file should contain the full job posting. This helps you:
- Tailor your resume to the specific role
- Prepare for interviews
- Track requirements and responsibilities

## Source Material

Your personal content should be organized in LaTeX format:

### experience.tex
```latex
\section{Experience}

\experience{Senior Software Engineer}{Company Name}{Jan 2020 -- Present}
\begin{itemize}
    \item Led development of microservices architecture
    \item Improved system performance by 40\%
\end{itemize}
```

### skills.tex
```latex
\section{Technical Skills}

\textbf{Languages:} Python, JavaScript, Go, Java\\
\textbf{Frameworks:} FastAPI, React, Django\\
\textbf{Cloud:} AWS, GCP, Docker, Kubernetes
```

## Custom Templates

You can override default templates by placing custom versions in `custom_templates/`:
- `custom_templates/resume.tex`
- `custom_templates/cover_letter.tex`

The system will use custom templates if they exist, otherwise fall back to the built-in templates.

## Getting Started

1. Start the Docker container
2. The system will auto-initialize if `/data` is empty
3. Edit the example application or create new ones
4. Access the web interface at `http://localhost:8000`
5. Add your applications through the UI or filesystem
6. Generate customized resumes and cover letters

## Backup

It's recommended to:
1. Keep your data directory in a separate git repository (private)
2. Back up the `job_applications.db` file regularly
3. Commit generated PDFs if you want version history
4. Consider using encrypted backups for sensitive information

## Migration from Existing Data

If you have existing job search data:

1. Copy your applications to the `applications/` directory
2. Copy your resume content to `source_material/`
3. Run the sync script to import into database:
   ```bash
   docker-compose exec job-tracker python scripts/sync_applications.py
   ```
