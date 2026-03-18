# Job Search Toolkit - Shell Aliases & Functions

This file contains shell configuration to simplify working with the Job Search Toolkit.

## Option 1: Simple Wrapper Script (Recommended)

Use the `job-tracker` wrapper script in the repository root:

```bash
# Create application
./job-tracker create Google "Senior_Engineer" developer

# Compile application
./job-tracker compile Google_Senior_Engineer

# Sync applications
./job-tracker sync

# Open shell in container
./job-tracker shell
```

Add to PATH for easier access:

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/Development/job-search-toolkit:$PATH"

# Now use anywhere:
job-tracker create Company "Job Title"
```

---

## Option 2: Shell Aliases

Add to your `~/.bashrc`, `~/.zshrc`, or `~/.bash_aliases`:

```bash
# Job Search Toolkit Aliases
# Note: Change path if your repo is in a different location

# Path to your repository
export JOB_TRACKER_REPO="$HOME/Development/job-search-toolkit"
export JOB_TRACKER_CONTAINER="job-search-tracker"

# Check if container is running
alias jt-status="docker ps | grep $JOB_TRACKER_CONTAINER"

# Start/stop container
alias jt-start="cd $JOB_TRACKER_REPO && docker-compose up -d && cd -"
alias jt-stop="cd $JOB_TRACKER_REPO && docker-compose down && cd -"
alias jt-restart="jt-stop && jt-start"

# Application management
alias jt-create="docker exec -it $JOB_TRACKER_CONTAINER scripts/create_application.sh"
alias jt-customize="docker exec -it $JOB_TRACKER_CONTAINER scripts/customize_application.sh"
alias jt-compile="docker exec -it $JOB_TRACKER_CONTAINER scripts/compile_application.sh"
alias jt-sync="docker exec -it $JOB_TRACKER_CONTAINER python scripts/sync_applications.py"
alias jt-list="docker exec -it $JOB_TRACKER_CONTAINER scripts/list_applications.sh"

# Container access
alias jt-shell="docker exec -it $JOB_TRACKER_CONTAINER bash"
alias jt-logs="docker logs -f $JOB_TRACKER_CONTAINER"

# Web UI
alias jt-open="open http://localhost:8000"  # macOS
# alias jt-open="xdg-open http://localhost:8000"  # Linux

# Shorthand aliases (if you prefer shorter names)
alias jtc="jt-create"
alias jts="jt-sync"
alias jtl="jt-list"
```

**Usage after sourcing:**

```bash
# Reload shell config
source ~/.bashrc  # or ~/.zshrc

# Create application
jt-create Google "Senior_Engineer" developer

# Compile application
jt-compile Google_Senior_Engineer

# Open shell
jt-shell
```

---

## Option 3: Shell Functions (More Advanced)

For better error handling and help messages:

```bash
# Add to ~/.bashrc or ~/.zshrc

export JOB_TRACKER_REPO="$HOME/Development/job-search-toolkit"
export JOB_TRACKER_CONTAINER="job-search-tracker"

# Helper function to check container
_jt_check() {
    if ! docker ps --format '{{.Names}}' | grep -q "^${JOB_TRACKER_CONTAINER}$"; then
        echo "❌ Container not running. Start with: jt-start"
        return 1
    fi
    return 0
}

# Create application
jt-create() {
    _jt_check || return 1
    docker exec -it "$JOB_TRACKER_CONTAINER" scripts/create_application.sh "$@"
}

# Compile application
jt-compile() {
    _jt_check || return 1
    if [ $# -eq 0 ]; then
        echo "Usage: jt-compile <Company_JobTitle>"
        return 1
    fi
    docker exec -it "$JOB_TRACKER_CONTAINER" scripts/compile_application.sh "$@"
}

# Customize application
jt-customize() {
    _jt_check || return 1
    if [ $# -eq 0 ]; then
        echo "Usage: jt-customize <Company_JobTitle>"
        return 1
    fi
    docker exec -it "$JOB_TRACKER_CONTAINER" scripts/customize_application.sh "$@"
}

# Sync applications
jt-sync() {
    _jt_check || return 1
    docker exec -it "$JOB_TRACKER_CONTAINER" python scripts/sync_applications.py
}

# List applications
jt-list() {
    _jt_check || return 1
    docker exec -it "$JOB_TRACKER_CONTAINER" scripts/list_applications.sh
}

# Shell access
jt-shell() {
    _jt_check || return 1
    echo "Opening shell in container. Type 'exit' to return."
    docker exec -it "$JOB_TRACKER_CONTAINER" bash
}

# Start/stop
jt-start() {
    cd "$JOB_TRACKER_REPO" && docker-compose up -d && cd -
    echo "✓ Job Tracker started: http://localhost:8000"
}

jt-stop() {
    cd "$JOB_TRACKER_REPO" && docker-compose down && cd -
}

# Open web UI
jt-open() {
    if command -v open &> /dev/null; then
        open http://localhost:8000
    elif command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:8000
    else
        echo "Open http://localhost:8000 in your browser"
    fi
}

# Help
jt-help() {
    cat << EOF
Job Search Toolkit Commands:

Container Management:
  jt-start         Start the container
  jt-stop          Stop the container
  jt-shell         Open bash shell in container
  jt-logs          View container logs
  jt-open          Open web UI in browser

Application Management:
  jt-create <Company> <JobTitle> [template]
                   Create new application
  jt-customize <Company_JobTitle>
                   Show customization guidance
  jt-compile <Company_JobTitle>
                   Compile resume and cover letter PDFs
  jt-sync          Sync applications to database
  jt-list          List all applications

Examples:
  jt-create Google "Senior Engineer" developer
  jt-compile Google_Senior_Engineer
  jt-sync

EOF
}
```

---

## Option 4: Makefile Targets

Add to the repository's `Makefile`:

```makefile
# Job Search Toolkit - Makefile

.PHONY: help start stop restart shell logs open create compile sync list

# Container management
start:
	docker-compose up -d
	@echo "✓ Job Tracker started: http://localhost:8000"

stop:
	docker-compose down

restart: stop start

shell:
	@docker exec -it job-search-tracker bash

logs:
	docker logs -f job-search-tracker

open:
	@command -v open >/dev/null 2>&1 && open http://localhost:8000 || echo "Open http://localhost:8000 in your browser"

# Application management
create:
	@if [ -z "$(COMPANY)" ] || [ -z "$(TITLE)" ]; then \
		echo "Usage: make create COMPANY=Google TITLE='Senior Engineer' TEMPLATE=developer"; \
		exit 1; \
	fi
	docker exec -it job-search-tracker scripts/create_application.sh "$(COMPANY)" "$(TITLE)" $(TEMPLATE)

compile:
	@if [ -z "$(APP)" ]; then \
		echo "Usage: make compile APP=Google_Senior_Engineer"; \
		exit 1; \
	fi
	docker exec -it job-search-tracker scripts/compile_application.sh "$(APP)"

sync:
	docker exec -it job-search-tracker python scripts/sync_applications.py

list:
	docker exec -it job-search-tracker scripts/list_applications.sh

help:
	@echo "Job Search Toolkit - Make Targets"
	@echo ""
	@echo "Container Management:"
	@echo "  make start          Start the container"
	@echo "  make stop           Stop the container"
	@echo "  make restart        Restart the container"
	@echo "  make shell          Open bash shell in container"
	@echo "  make logs           View container logs"
	@echo "  make open           Open web UI in browser"
	@echo ""
	@echo "Application Management:"
	@echo "  make create COMPANY=<name> TITLE=<title> [TEMPLATE=<type>]"
	@echo "                      Create new application"
	@echo "  make compile APP=<name>"
	@echo "                      Compile application PDFs"
	@echo "  make sync           Sync applications to database"
	@echo "  make list           List all applications"
	@echo ""
	@echo "Examples:"
	@echo "  make create COMPANY=Google TITLE='Senior Engineer' TEMPLATE=developer"
	@echo "  make compile APP=Google_Senior_Engineer"
	@echo "  make sync"
```

**Usage:**

```bash
make start
make create COMPANY=Google TITLE="Senior Engineer" TEMPLATE=developer
make compile APP=Google_Senior_Engineer
make sync
```

---

## Recommendation

**For most users:** Use **Option 1** (wrapper script) or **Option 2** (aliases)

**Pros:**
- ✅ Simple to set up
- ✅ Clear command structure
- ✅ No confusion about container vs host
- ✅ Works from any directory (if in PATH)

**Cons:**
- Need to remember to start container first
- Slightly more typing than direct script calls

**Example workflow with wrapper:**

```bash
# One-time setup: add to PATH
echo 'export PATH="$HOME/Development/job-search-toolkit:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Daily usage
job-tracker create Klaviyo "Engineering Manager" developer
job-tracker compile Klaviyo_Engineering_Manager
job-tracker sync
```

**Example workflow with aliases:**

```bash
# One-time setup: add aliases to ~/.bashrc
cat >> ~/.bashrc << 'EOF'
export JOB_TRACKER_CONTAINER="job-search-tracker"
alias jt-create="docker exec -it $JOB_TRACKER_CONTAINER scripts/create_application.sh"
alias jt-compile="docker exec -it $JOB_TRACKER_CONTAINER scripts/compile_application.sh"
alias jt-sync="docker exec -it $JOB_TRACKER_CONTAINER python scripts/sync_applications.py"
alias jt-shell="docker exec -it $JOB_TRACKER_CONTAINER bash"
EOF
source ~/.bashrc

# Daily usage
jt-create Klaviyo "Engineering Manager" developer
jt-compile Klaviyo_Engineering_Manager
jt-sync
```

---

## Preventing Local File Creation

### Problem

Users might accidentally run scripts outside the container, creating files in the wrong location:

```bash
# WRONG - creates files in repo directory
./scripts/create_application.sh Google "Engineer"
```

### Solutions

#### 1. Add Warning to Scripts

Add this to the top of each script:

```bash
#!/bin/bash

# Detect if running outside container
if [ ! -f "/.dockerenv" ]; then
    echo "⚠️  WARNING: This script should be run inside the Docker container"
    echo ""
    echo "Run with:"
    echo "  docker exec -it job-search-tracker scripts/$(basename $0) $@"
    echo ""
    echo "Or use the wrapper: ./job-tracker create ..."
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Rest of script...
```

#### 2. Make Scripts Non-Executable Outside Container

```bash
# In repository, make scripts executable only for reading
chmod 644 scripts/*.sh

# In Docker entrypoint, make them executable
chmod +x /app/scripts/*.sh
```

#### 3. Use Wrapper Script Exclusively

Document that users should ONLY use the wrapper script, never call scripts directly.

---

## Documentation Updates Needed

### README.md

Add "Quick Start" section:

```markdown
## Quick Start

1. Start the container:
   ```bash
   docker-compose up -d
   ```

2. Create an application:
   ```bash
   ./job-tracker create Company "Job Title" developer
   ```

3. Open web UI:
   ```bash
   open http://localhost:8000
   ```

**Important:** Always use `./job-tracker` wrapper or `docker exec` commands.
Never run scripts directly from the host.
```

### Add to TODO.md

```markdown
## High Priority - User Experience

### 🎯 Simplify Container Workflow (HIGH PRIORITY)
**Priority:** P1
**Estimated Time:** 1 hour

**Tasks:**
- [x] Create wrapper script (job-tracker)
- [ ] Add container detection to scripts
- [ ] Update README with quick start
- [ ] Add example aliases to docs/SHELL_ALIASES.md
- [ ] Add troubleshooting for common mistakes
```

---

## Summary

**Problem:** Users confused about running commands inside vs outside container

**Solution:** Multiple approaches available:
1. ✅ **Wrapper script** (`./job-tracker`) - Simple, clear
2. ✅ **Shell aliases** (`jt-create`) - Convenient, customizable
3. ✅ **Shell functions** - Advanced error handling
4. ✅ **Makefile targets** (`make create`) - Familiar to developers

**Recommended:** Wrapper script + documentation emphasizing container-first workflow

**Key principle:** Make it **harder to do the wrong thing** and **easier to do the right thing**
