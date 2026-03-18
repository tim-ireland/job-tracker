# Troubleshooting Guide

Common issues and solutions for the Job Search Toolkit.

---

## Container Issues

### Container Not Running

**Symptom:** Error message "Container 'job-search-tracker' is not running"

**Solution:**
```bash
cd /path/to/job-search-toolkit
docker-compose up -d
```

**Check status:**
```bash
docker ps | grep job-search-tracker
```

### Can't Access Web UI

**Symptom:** Cannot open http://localhost:8000

**Solutions:**

1. Check if container is running:
   ```bash
   docker ps | grep job-search-tracker
   ```

2. Check container logs:
   ```bash
   docker logs job-search-tracker
   ```

3. Verify port is not in use:
   ```bash
   # macOS/Linux
   lsof -i :8000
   
   # If port is in use, change it:
   HOST_PORT=8001 docker-compose up -d
   ```

---

## Script Issues

### "WARNING: This script should be run inside the Docker container"

**Symptom:** Scripts show warning when run directly

**Cause:** You're running scripts from the host machine instead of inside the container

**Solutions:**

**Best practice - Use the wrapper:**
```bash
./job-tracker create Company "Job Title"
./job-tracker compile Company_JobTitle
```

**Alternative - Run in container:**
```bash
docker exec -it job-search-tracker scripts/create_application.sh Company "Job Title"
```

**Force run (not recommended):**
```bash
FORCE_RUN=1 ./scripts/create_application.sh Company "Job Title"
```

### Files Created in Wrong Location

**Symptom:** Application files appear in `job-search-toolkit/applications` instead of your data directory

**Cause:** Scripts were run outside the container

**Solution:**
1. Delete incorrectly created files:
   ```bash
   rm -rf applications/Company_JobTitle
   ```

2. Use the wrapper script:
   ```bash
   ./job-tracker create Company "Job Title"
   ```

### "Permission denied" When Running Scripts

**Symptom:** Cannot execute scripts

**Solution:**
```bash
# Make wrapper executable
chmod +x job-tracker

# Scripts inside container are automatically executable
```

---

## Data Directory Issues

### "Directory does not exist"

**Symptom:** Container can't find data directory

**Solutions:**

1. Check DATA_PATH is set correctly:
   ```bash
   echo $DATA_PATH
   # Should show path to your data directory
   ```

2. Create data directory if missing:
   ```bash
   mkdir -p $DATA_PATH/applications
   ```

3. Verify in docker-compose.yml:
   ```bash
   docker-compose config | grep volumes
   ```

### Database Locked

**Symptom:** "database is locked" errors

**Causes:**
- Multiple containers accessing same data
- Network storage latency
- File sync conflicts (Dropbox, OneDrive)

**Solutions:**

1. Ensure only one container is running:
   ```bash
   docker ps | grep job-tracker
   docker-compose down
   docker-compose up -d
   ```

2. For network storage, consider local database:
   - Keep applications on network storage
   - Override DATABASE_URL to local disk

---

## LaTeX/PDF Issues

### PDFs Not Generating

**Symptom:** `compile` command runs but no PDF created

**Solutions:**

1. Check for LaTeX errors in output:
   ```bash
   ./job-tracker shell
   cd /data/applications/Company_JobTitle
   pdflatex resume.tex
   # Look for error messages
   ```

2. Check .log file:
   ```bash
   cat resume.log | grep Error
   ```

3. Common LaTeX errors:
   - Unmatched braces `{}` or brackets `[]`
   - Special characters not escaped: `$`, `&`, `%`, `#`, `_`
   - Missing packages (should be included in Docker)

### PDFs Don't Show in Web UI

**Symptom:** Files exist but don't appear in UI

**Solutions:**

1. Ensure files have `.pdf` extension (lowercase):
   ```bash
   ls -la /data/applications/Company_JobTitle/*.pdf
   ```

2. Refresh the page

3. Check browser console for errors

### LaTeX Compilation Hangs

**Symptom:** `pdflatex` command never finishes

**Solution:**

Use non-interactive mode:
```bash
pdflatex -interaction=nonstopmode resume.tex
```

Or use the compile script which does this automatically:
```bash
./job-tracker compile Company_JobTitle
```

---

## Application Sync Issues

### Applications in Filesystem But Not in Database

**Symptom:** Created application directory manually, doesn't show in web UI

**Solution:**
```bash
./job-tracker sync
```

This scans the applications directory and adds missing entries to the database.

### Duplicate Applications

**Symptom:** Same application appears multiple times in UI

**Solutions:**

1. Check for duplicate directories with slightly different names
2. Manually delete duplicate via web UI
3. Or use database directly:
   ```bash
   ./job-tracker shell
   sqlite3 /data/job_applications.db
   SELECT * FROM applications WHERE company_id = X;
   DELETE FROM applications WHERE id = Y;
   ```

---

## Wrapper Script Issues

### "job-tracker: command not found"

**Symptom:** Can't run `job-tracker` from any directory

**Cause:** Script is not in your PATH

**Solutions:**

**Option 1:** Run from repository directory:
```bash
cd /path/to/job-search-toolkit
./job-tracker create Company "Job Title"
```

**Option 2:** Add to PATH:
```bash
echo 'export PATH="$HOME/Development/job-search-toolkit:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Option 3:** Create symlink:
```bash
sudo ln -s /path/to/job-search-toolkit/job-tracker /usr/local/bin/job-tracker
```

### Wrapper Shows Wrong Container Name

**Symptom:** Wrapper can't find container

**Cause:** Container has different name

**Solution:**

Check actual container name:
```bash
docker ps --format '{{.Names}}'
```

Edit `job-tracker` script if needed:
```bash
# Change this line if your container has a different name
CONTAINER_NAME="job-search-tracker"
```

---

## Web UI Issues

### Cannot Edit Application

**Symptom:** Edit button doesn't work

**Solutions:**

1. Check browser console for JavaScript errors
2. Refresh the page
3. Clear browser cache
4. Try different browser

### Changes Don't Save

**Symptom:** Edits are lost after refresh

**Solutions:**

1. Check container logs for errors:
   ```bash
   docker logs job-search-tracker
   ```

2. Verify database file is writable:
   ```bash
   ls -la $DATA_PATH/job_applications.db
   ```

3. Check database isn't locked:
   ```bash
   fuser $DATA_PATH/job_applications.db
   ```

### PDF Viewer Not Working

**Symptom:** Can't view PDFs in browser

**Solutions:**

1. Download PDF instead (click download icon)
2. Check PDF isn't corrupted:
   ```bash
   file /data/applications/Company_JobTitle/resume.pdf
   ```
3. Try different browser
4. Check browser console for errors

---

## Common Mistakes

### ❌ Running Scripts Outside Container

**Wrong:**
```bash
./scripts/create_application.sh Company "Job Title"
```

**Right:**
```bash
./job-tracker create Company "Job Title"
```

### ❌ Using Wrong Path Inside Container

**Wrong:**
```bash
docker exec -it job-search-tracker ls applications/
```

**Right:**
```bash
docker exec -it job-search-tracker ls /data/applications/
```

### ❌ Forgetting to Start Container

**Wrong:**
```bash
./job-tracker create Company "Job Title"
# Error: Container not running
```

**Right:**
```bash
docker-compose up -d
./job-tracker create Company "Job Title"
```

### ❌ Editing Files in Repo Instead of Data Directory

**Wrong:**
```bash
cd job-search-toolkit/applications/Company_JobTitle
vim resume.tex  # This doesn't exist here!
```

**Right:**
```bash
cd $DATA_PATH/applications/Company_JobTitle
vim resume.tex
```

Or edit via web UI.

---

## Getting Help

### Enable Debug Mode

For more verbose output:

```bash
# Set in docker-compose.yml or .env
LOG_LEVEL=DEBUG

docker-compose restart
docker logs -f job-search-tracker
```

### Check Container Health

```bash
# View container status
docker ps -a | grep job-tracker

# Check health
docker inspect job-search-tracker | grep -A 10 Health

# View resource usage
docker stats job-search-tracker
```

### Gather Diagnostic Information

When reporting issues, include:

```bash
# System info
docker version
docker-compose version

# Container info
docker ps -a | grep job-tracker
docker logs --tail 100 job-search-tracker

# Configuration
echo $DATA_PATH
cat .env

# Directory structure
ls -la $DATA_PATH
ls -la $DATA_PATH/applications
```

---

## Reset/Recovery

### Soft Reset - Restart Container

```bash
docker-compose restart
```

### Hard Reset - Rebuild Container

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Nuclear Option - Complete Reset

**⚠️  Warning:** This deletes all data!

```bash
# Stop container
docker-compose down

# Remove database (backup first!)
cp $DATA_PATH/job_applications.db $DATA_PATH/job_applications.db.backup
rm $DATA_PATH/job_applications.db

# Restart
docker-compose up -d

# Database will be recreated (empty)
```

### Backup Before Reset

```bash
# Backup everything
tar -czf job-search-backup-$(date +%Y%m%d).tar.gz $DATA_PATH

# Or just database
cp $DATA_PATH/job_applications.db ~/backup-$(date +%Y%m%d).db
```

---

## Performance Issues

### Slow Web UI

**Solutions:**

1. Check Docker resource allocation (Docker Desktop settings)
2. Close unused applications
3. Check database size:
   ```bash
   du -h $DATA_PATH/job_applications.db
   ```
4. Optimize database:
   ```bash
   ./job-tracker shell
   sqlite3 /data/job_applications.db "VACUUM;"
   ```

### Slow PDF Compilation

**Solutions:**

1. Use faster template (base instead of complex ones)
2. Reduce document size
3. Run compilation in background
4. Allocate more CPU to Docker

---

## Still Having Issues?

1. Check [GitHub Issues](https://github.com/yourusername/job-search-toolkit/issues)
2. Search [Discussions](https://github.com/yourusername/job-search-toolkit/discussions)
3. Create new issue with:
   - Detailed description
   - Steps to reproduce
   - Error messages
   - System information
   - Logs

---

*Last Updated: March 18, 2026*
