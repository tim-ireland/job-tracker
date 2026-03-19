#!/bin/bash
# Setup Alembic for database migrations

echo "Setting up Alembic..."

# Initialize Alembic (run in container)
docker exec -it job-search-tracker bash -c "
cd /app &&
pip install alembic==1.13.1 &&
alembic init alembic
"

echo "✅ Alembic initialized"
echo ""
echo "Next steps:"
echo "1. Configure alembic.ini"
echo "2. Update alembic/env.py with SQLAlchemy models"
echo "3. Create first migration"
