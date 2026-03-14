# Job Search Toolkit

A comprehensive web-based job application tracking system with LaTeX resume generation, built with FastAPI and Docker.

## Features

- 📊 **Track Applications**: Manage job applications with status tracking, priorities, and deadlines
- 📝 **Resume Generation**: Generate customized LaTeX resumes and cover letters for each application
- 📄 **PDF Management**: View and download generated PDFs directly from the web interface
- 👥 **Company Tracking**: Maintain company information, contacts, and tech stacks
- 📅 **Interview Scheduling**: Track interviews with dates, interviewers, and outcomes
- 💼 **Offer Comparison**: Compare multiple job offers side-by-side
- 🎨 **Modern UI**: Clean, responsive interface with dark/light mode
- 🐳 **Docker Support**: Containerized application with persistent data volumes

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

### Creating a New Application

1. Click "Add Application" in the web interface
2. Fill in company details and job information
3. Or use the command line:
   ```bash
   docker-compose exec job-tracker python scripts/create_application.sh "Company Name" "Job Title"
   ```

### Generating Resumes

Applications are stored in your data directory at `applications/Company_JobTitle/`:
- `job_description.txt` - The job posting
- `config.txt` - Configuration (template type, priority, status)
- `resume.tex` - Generated LaTeX resume
- `resume.pdf` - Compiled PDF
- `cover_letter.tex` - Generated cover letter
- `cover_letter.pdf` - Compiled PDF

Edit the `.tex` files with your favorite editor, then compile:
```bash
docker-compose exec job-tracker bash
cd /data/applications/Company_JobTitle
pdflatex resume.tex
```

### Syncing Applications

If you create applications manually in the filesystem, sync them to the database:
```bash
docker-compose exec job-tracker python scripts/sync_applications.py
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
- 🐛 [Issue Tracker](https://github.com/yourusername/job-search-toolkit/issues)
- 💬 [Discussions](https://github.com/yourusername/job-search-toolkit/discussions)

## Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [LaTeX](https://www.latex-project.org/)
- [Docker](https://www.docker.com/)
