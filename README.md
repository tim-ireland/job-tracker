# Job Search Toolkit

A comprehensive web-based job application tracking system with LaTeX resume generation, built with FastAPI and Docker.

<img width="1512" height="1407" alt=" Job Application Tracker" src="https://github.com/user-attachments/assets/34d26ada-3675-4d26-9b28-acdd428d3498" />

## Features

- 📊 **Track Applications**: Manage job applications with status tracking, priorities, and deadlines
- 📝 **Resume Generation**: Generate customized LaTeX resumes and cover letters for each application
- 📄 **PDF Management**: View and download generated PDFs directly from the web interface
- 👥 **Company Tracking**: Maintain company information, contacts, and tech stacks
- 📅 **Interview Scheduling**: Track interviews with dates, interviewers, and outcomes
- 💼 **Offer Comparison**: Compare multiple job offers side-by-side
- 📋 **MA DUA Export**: Export weekly activity reports for Massachusetts Department of Unemployment Assistance
- 🎨 **Modern UI**: Clean, responsive interface with dark/light mode
- 🐳 **Docker Support**: Containerized application with persistent data volumes
- 🤖 **Claude Code MCP Server**: Drive your job search from the terminal using natural language via Claude Code

## Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/job-search-toolkit.git
   cd job-search-toolkit
   ```

2. **Create your data directory**
   ```bash
   mkdir ../my-job-search
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   
   Open your browser to `http://localhost:8000`

The first time you run the application, it will automatically initialize the data directory with example files and structure.

### Local Development

If you prefer to run without Docker:

1. **Install dependencies**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Install LaTeX (Ubuntu/Debian)
   sudo apt-get install texlive-latex-base texlive-latex-extra
   
   # Install LaTeX (macOS)
   brew install --cask mactex
   ```

2. **Set environment variables**
   ```bash
   export DATA_DIR=./data
   ```

3. **Run the application**
   ```bash
   uvicorn job_tracker.app:app --reload
   ```

## Directory Structure

```
job-search-toolkit/          # This repository (public)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── job_tracker/            # Web application
├── templates/              # LaTeX templates
├── scripts/                # Helper scripts
└── docs/                   # Documentation

my-job-search/              # Your data (keep private)
├── applications/           # Job applications
├── source_material/        # Personal resume content
├── custom_templates/       # Custom LaTeX templates
└── job_applications.db     # Database
```

## Usage

### Using the Wrapper Script (Recommended)

The `job-tracker` wrapper script ensures all commands run inside the container:

```bash
# Create a new application
./job-tracker create Google "Senior Engineer" developer

# Show customization guidance
./job-tracker customize Google_Senior_Engineer

# Compile resume and cover letter PDFs
./job-tracker compile Google_Senior_Engineer

# Sync applications to database
./job-tracker sync

# Open shell in container
./job-tracker shell

# Get help
./job-tracker help
```

**Optional:** Add to your PATH for system-wide access:
```bash
echo 'export PATH="$HOME/Development/job-search-toolkit:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Now use from anywhere
job-tracker create Company "Job Title"
```

### Alternative: Shell Aliases

For power users, add these to your `~/.bashrc` or `~/.zshrc`:

```bash
alias jt-create="docker exec -it job-search-tracker scripts/create_application.sh"
alias jt-compile="docker exec -it job-search-tracker scripts/compile_application.sh"
alias jt-sync="docker exec -it job-search-tracker python scripts/sync_applications.py"
alias jt-shell="docker exec -it job-search-tracker bash"
```

See [docs/SHELL_ALIASES.md](docs/SHELL_ALIASES.md) for more options.

### Creating Applications

Applications are stored in your data directory at `applications/Company_JobTitle/`:
- `job_description.txt` - The job posting
- `config.txt` - Configuration (template type, priority, status)
- `resume.tex` - Generated LaTeX resume
- `resume.pdf` - Compiled PDF
- `cover_letter.tex` - Generated cover letter
- `cover_letter.pdf` - Compiled PDF

Edit the `.tex` files with your favorite editor, then compile:
```bash
./job-tracker compile Company_JobTitle
```

### Syncing Applications

If you create applications manually in the filesystem, sync them to the database:
```bash
./job-tracker sync
```

## Configuration

### Environment Variables

- `DATA_DIR` - Path to data directory (default: `/data` in Docker)
- `DATABASE_URL` - Database connection string (default: SQLite in data dir)
- `TEMPLATES_DIR` - Path to LaTeX templates

### Docker Compose

You can customize the data path in `docker-compose.yml`:
```yaml
volumes:
  - /path/to/your/data:/data
```

Or set the `DATA_PATH` environment variable:
```bash
DATA_PATH=/path/to/your/data docker-compose up
```

## Templates

The toolkit includes several resume templates:
- `base_resume.tex` - Standard resume format
- `manager_resume.tex` - Management-focused resume
- `director_resume.tex` - Executive-level resume
- `cover_letter.tex` - Cover letter template

Create custom templates in your data directory at `custom_templates/`.

## API Documentation

Once running, view the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Weekly Activity Export (Massachusetts DUA)

The toolkit includes specialized endpoints for exporting job search activity in the format required by the Massachusetts Department of Unemployment Assistance.

#### Export Previous Week (Text Format)
```bash
curl http://localhost:8000/api/reports/dua-weekly
```

#### Export Specific Week (Text Format)
```bash
# Week starting Sunday, March 9, 2026
curl http://localhost:8000/api/reports/dua-weekly?week_start=2026-03-09
```

#### Export Previous Week (CSV Format)
```bash
curl http://localhost:8000/api/reports/dua-weekly-csv -o weekly_report.csv
```

#### Export Specific Week (CSV Format)
```bash
curl "http://localhost:8000/api/reports/dua-weekly-csv?week_start=2026-03-09" -o weekly_report.csv
```

#### Export Date Range (Text Format)
```bash
# Get all activity from February 1 through March 31, 2026
curl "http://localhost:8000/api/reports/dua-range?start_date=2026-02-01&end_date=2026-03-31"
```

#### Export Date Range (CSV Format)
```bash
curl "http://localhost:8000/api/reports/dua-range-csv?start_date=2026-02-01&end_date=2026-03-31" -o range_report.csv
```

**Report Format:**
Each activity entry includes:
- Date: When the activity occurred
- Position: Job title
- Pay rate: Salary range or "Not specified"
- Employer name and address: Company name with website or location
- Job ID or person contacted: Application ID or contact person
- Contact email, website, or phone: Contact information
- Result: Status of the application (Applied, Screening, Interview, Offer Received, Rejected, etc.)

The export captures ALL job search activity that progressed during the week, including:
- Applications submitted
- Phone screenings received
- Interviews conducted
- Offers received
- Applications closed (rejected/withdrawn/accepted)

## Claude Code MCP Server

The toolkit includes a Rust-based MCP (Model Context Protocol) server that lets you manage your job search pipeline directly from Claude Code using natural language.

See [docs/MCP_SERVER.md](docs/MCP_SERVER.md) for full setup and usage details.

### Quick Setup

The MCP server binary is built into the Docker image automatically. To connect Claude Code to it:

1. **Rebuild the image** (if you haven't since the MCP server was added):
   ```bash
   docker compose build
   docker compose up -d
   ```

2. **Register the server** by adding this to `~/.claude/mcp.json`:
   ```json
   {
     "mcpServers": {
       "job-tracker": {
         "command": "docker",
         "args": ["exec", "-i", "-e", "JOB_TRACKER_URL=http://localhost:8000",
                  "job-search-tracker", "/usr/local/bin/job-tracker-mcp"]
       }
     }
   }
   ```

3. **Restart Claude Code** — the server loads at startup.

### Example Usage

Once connected, you can talk to your job search data naturally:

```
"Show me my pipeline summary"
"Add an application for Stripe, Staff Engineer role, P1 priority"
"Log that I had a call with the Google recruiter today"
"Schedule a technical interview for my Stripe application on Friday at 2pm"
"Which applications are still in Pipeline status?"
"Compare my current offers"
```

## Development

### Running Tests
```bash
pytest
```

### Code Style
```bash
black .
flake8
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details

## Privacy

This toolkit is designed to keep your personal job search data separate from the application code. Your data directory should be:
- Kept in a separate location
- Backed up regularly
- Never committed to a public repository
- Optionally tracked in a private git repository

## Support

- 📖 [Documentation](docs/)
- 🤖 [MCP Server Setup](docs/MCP_SERVER.md)
- 🐛 [Issue Tracker](https://github.com/yourusername/job-search-toolkit/issues)
- 💬 [Discussions](https://github.com/yourusername/job-search-toolkit/discussions)

## Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [LaTeX](https://www.latex-project.org/)
- [Docker](https://www.docker.com/)
