# Contributing to Job Search Toolkit

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help make the community welcoming to everyone

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

### Local Development

```bash
# Clone your fork
git clone https://github.com/yourusername/job-search-toolkit.git
cd job-search-toolkit

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Set up test data
export DATA_DIR=./test_data
mkdir -p test_data/applications

# Run the application
uvicorn job_tracker.app:app --reload
```

### Docker Development

```bash
# Build and run
docker-compose up --build

# Run with test data
DATA_PATH=./test_data docker-compose up
```

## Making Changes

### Code Style

We use:
- **Black** for code formatting
- **Flake8** for linting
- **Type hints** where appropriate

Before committing:
```bash
# Format code
black .

# Check linting
flake8 .

# Run tests
pytest
```

### Commit Messages

Use clear, descriptive commit messages:

```
Add feature to export applications as CSV

- Added export_csv endpoint in app.py
- Created CSV serialization in crud.py
- Added export button to UI
- Updated documentation
```

Format: `<type>: <description>`

Types:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding/updating tests
- `chore:` Maintenance tasks

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `refactor/description` - Refactoring

Examples:
- `feature/add-csv-export`
- `fix/date-parsing-error`
- `docs/update-setup-guide`

## Testing

### Running Tests

```bash
pytest
```

### Writing Tests

Add tests in `tests/` directory:

```python
def test_create_application():
    """Test creating a new application"""
    # Test code here
    pass
```

### Test Coverage

Aim for:
- 80%+ code coverage
- All new features tested
- Edge cases covered

## Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Run linters and tests** locally
4. **Create pull request** with clear description
5. **Wait for CI** to pass
6. **Address review comments**
7. **Squash commits** if requested

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How did you test this?

## Checklist
- [ ] Code follows project style
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests pass
- [ ] No breaking changes (or documented)
```

## Areas for Contribution

### High Priority
- Additional LaTeX templates
- Export functionality (CSV, JSON)
- Email integration
- Calendar integration
- Mobile responsiveness improvements

### Medium Priority
- Search and filtering improvements
- Bulk operations
- Import from LinkedIn
- Statistics and analytics
- Notification system

### Documentation
- Video tutorials
- More examples
- Template customization guide
- API usage examples
- Troubleshooting guide

### Testing
- Unit tests
- Integration tests
- E2E tests
- Performance tests

## Architecture

### Technology Stack
- **Backend:** FastAPI (Python)
- **Database:** SQLAlchemy + SQLite
- **Frontend:** Vanilla JavaScript
- **Styling:** Custom CSS (Solarized theme)
- **PDF Generation:** LaTeX

### Key Components

```
job_tracker/
├── app.py          # FastAPI routes and endpoints
├── models.py       # Pydantic models for API
├── database.py     # SQLAlchemy models and DB setup
├── crud.py         # Database operations
├── static/         # JavaScript and CSS
└── templates/      # HTML templates
```

### Adding New Features

1. **Database changes:** Update `database.py` models
2. **API endpoints:** Add routes in `app.py`
3. **Business logic:** Add functions in `crud.py`
4. **Frontend:** Update JavaScript in `static/`
5. **Styling:** Update `static/style.css`

## Questions?

- Open an issue for discussion
- Join our discussions page
- Check existing issues for similar questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
