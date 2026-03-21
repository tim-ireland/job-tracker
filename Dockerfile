# ── Stage 1: Build the Rust MCP server ───────────────────────────────────────
FROM rust:latest AS rust-builder
WORKDIR /build
COPY mcp-server/ .
RUN cargo build --release

# ── Stage 2: Final image ──────────────────────────────────────────────────────
FROM python:3.11-slim

# Install LaTeX and other dependencies
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    curl \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY job_tracker/ ./job_tracker/
COPY templates/ ./templates/
COPY scripts/ ./scripts/
COPY alembic/ ./alembic/
COPY alembic.ini .

# Copy MCP server binary from builder stage
COPY --from=rust-builder /build/target/release/job-tracker-mcp /usr/local/bin/job-tracker-mcp

# Create data directory mount point
RUN mkdir -p /data/applications /data/source_material

# 12-factor: Configuration via environment variables
ENV DATA_DIR=/data \
    PYTHONUNBUFFERED=1 \
    LOG_LEVEL=info \
    DATABASE_URL=sqlite:////data/job_applications.db

# Expose port (configurable via environment)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Copy and set up entrypoint
COPY docker-entrypoint.sh /
COPY start-uvicorn.sh /
RUN chmod +x /docker-entrypoint.sh /start-uvicorn.sh

# Run as non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app /data
USER appuser

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["/start-uvicorn.sh"]
