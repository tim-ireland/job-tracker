# Job Search Toolkit - Workflow Summary

**Last Updated:** March 21, 2026

---

## Recommended: MCP-Driven Workflow (Claude Code)

The fastest path uses the MCP server to let Claude handle every automated step in a single conversation. No shell commands, no copy-paste between tools.

### Full example

```
"Create a manager-template application for Red Hat, ROSA Service EM,
 P2 priority, salary $148k-$245k. Here's the job description: [paste]
 Customize the resume to highlight Kubernetes and cloud infrastructure work,
 then compile it."
```

Claude will:
1. Call `create_application` — scaffolds directory, copies templates, creates DB entry
2. Read the job description you pasted
3. Edit `resume.tex` and `cover_letter.tex` to match the role
4. Call `compile_application` — runs pdflatex, embeds PDF metadata

Then after your review:
```
"Looks good. Mark it as Applied, today's date, resume_filename resume.pdf"
```

### Time with MCP workflow

| Step | Time | Who |
|------|------|-----|
| Paste job description + prompt | 1 min | You |
| Claude scaffolds, customizes, compiles | 1-2 min | Claude |
| Review PDFs and verify accuracy | 3-5 min | You (critical) |
| Mark Applied via MCP | 10 sec | Claude |
| **Total** | **~5-8 min** | |

See [MCP_SERVER.md](MCP_SERVER.md) for setup and full tool reference.

---

## Complete Application Workflow

### Legacy: Semi-Automated (Shell Scripts)

The workflow combines automated tooling with necessary human review steps to ensure quality and truthfulness.

---

## Step-by-Step Workflow

### 1️⃣ Create Application Structure (AUTOMATED)
```bash
./scripts/create_application.sh "Company" "Job_Title" template_type
# Example: ./scripts/create_application.sh Klaviyo "Engineering_Manager" developer
```

**What it does:**
- ✅ Creates application directory: `applications/Company_JobTitle/`
- ✅ Copies LaTeX templates (resume.tex, cover_letter.tex)
- ✅ Creates placeholder files (job_description.txt, config.txt)
- ✅ Creates database entries (company + application)
- ✅ Assigns application ID

**Time:** ~5 seconds

---

### 2️⃣ Fill Job Description (MANUAL - 1 min)
```bash
cd applications/Company_JobTitle
# Edit job_description.txt - paste full job posting
```

**What you do:**
- Copy job posting from company website
- Paste into `job_description.txt`
- Save file

**Time:** ~1 minute

---

### 3️⃣ Generate Customization Prompt (SEMI-AUTOMATED)

**Option A: Manual Assembly (current)**
```bash
# Gather materials
cat job_description.txt
cat resume.tex
cat /data/templates/base_master_resume.tex
find /data/source_material -name "*.md" -exec cat {} \;

# Copy template from docs/RESUME_CUSTOMIZATION_PROMPT.md
# Fill in placeholders with gathered materials
# Send to AI assistant
```
**Time:** ~5-10 minutes (manual copying)

**Option B: Automated Script (RECOMMENDED - see below)**
```bash
./scripts/generate_customization_prompt.sh Company_JobTitle
# Outputs: customization_prompt_filled.txt (ready to send to AI)
```
**Time:** ~10 seconds ⚡

---

### 4️⃣ AI Customization (EXTERNAL - 2-5 min)
```bash
# Send prompt to AI assistant (Claude, GitHub Copilot, ChatGPT)
# Wait for response with 3 sections:
#   SECTION 1: Customized resume.tex
#   SECTION 2: Customized cover_letter.tex
#   SECTION 3: Pre-filled review prompt
```

**What AI does:**
- Analyzes job description
- Customizes resume using your source material
- Customizes cover letter
- Generates pre-filled review prompt

**Time:** 2-5 minutes (AI processing + your review)

---

### 5️⃣ Save AI Output (SEMI-AUTOMATED)

**Option A: Manual (current)**
```bash
# Copy SECTION 1 → resume.tex
# Copy SECTION 2 → cover_letter.tex
# Copy SECTION 3 → review_prompt.txt
```
**Time:** ~2 minutes (manual copying)

**Option B: Automated Script (RECOMMENDED - see below)**
```bash
# Save AI response to ai_response.txt, then:
./scripts/parse_ai_response.sh ai_response.txt
# Automatically extracts and saves all 3 sections
```
**Time:** ~5 seconds ⚡

---

### 6️⃣ Verify Truthfulness (MANUAL - CRITICAL - 3-5 min)
```bash
# Review customized documents
cat resume.tex
cat cover_letter.tex

# Check against source material:
# - Every achievement is documented?
# - All metrics are accurate?
# - No fabricated experience?
# - Skills you actually have?
```

**Critical human oversight - cannot be automated**

**Time:** 3-5 minutes

---

### 7️⃣ Compile PDFs (AUTOMATED)
```bash
./scripts/compile_application.sh Company_JobTitle
```

**What it does:**
- ✅ Runs pdflatex twice (resolves references)
- ✅ Adds PDF metadata (company, role, version)
- ✅ Cleans up auxiliary files (.aux, .log, .out)
- ✅ Generates both resume.pdf and cover_letter.pdf

**Time:** ~10 seconds

---

### 8️⃣ Review PDFs (MANUAL - 2-3 min)
```bash
open resume.pdf cover_letter.pdf
# Visual review of formatting, content, accuracy
```

**Time:** 2-3 minutes

---

### 9️⃣ ATS Scoring & Quality Check (EXTERNAL - 2-3 min)
```bash
# Send review_prompt.txt (from step 5) to AI assistant
# Review feedback:
#   - Overall ATS score (target: 80+)
#   - Missing keywords
#   - Writing quality issues
#   - Prioritized recommendations
```

**Time:** 2-3 minutes

---

### 🔟 Iterate if Needed (OPTIONAL - 5-10 min)
```bash
# If ATS score < 80 or issues found:
# 1. Make recommended changes to resume.tex/cover_letter.tex
# 2. Re-compile: ./scripts/compile_application.sh Company_JobTitle
# 3. Optionally re-run review prompt to verify improvements
```

**Time:** 5-10 minutes (if needed)

---

### 1️⃣1️⃣ Final Compilation (AUTOMATED)
```bash
./scripts/compile_application.sh Company_JobTitle
# Final PDFs ready for submission
```

**Time:** ~10 seconds

---

### 1️⃣2️⃣ Track in Web UI (MANUAL - 1 min)
```bash
# Open http://localhost:8000
# Update application:
#   - Status: Applied
#   - Date applied: [today]
#   - Any notes
```

**Time:** ~1 minute

---

## Time Summary

### Current Workflow (Semi-Automated)
| Step | Time | Type |
|------|------|------|
| 1. Create structure | 5 sec | AUTO |
| 2. Fill job description | 1 min | MANUAL |
| 3. Gather materials & fill prompt | 5-10 min | MANUAL |
| 4. AI customization | 2-5 min | EXTERNAL |
| 5. Save AI output | 2 min | MANUAL |
| 6. Verify truthfulness | 3-5 min | MANUAL |
| 7. Compile PDFs | 10 sec | AUTO |
| 8. Review PDFs | 2-3 min | MANUAL |
| 9. ATS scoring | 2-3 min | EXTERNAL |
| 10. Iterate (if needed) | 5-10 min | MANUAL |
| 11. Final compile | 10 sec | AUTO |
| 12. Track in UI | 1 min | MANUAL |
| **TOTAL (first pass)** | **~20-30 min** | |
| **TOTAL (with iteration)** | **~25-40 min** | |

### Optimized Workflow (With New Scripts - RECOMMENDED)
| Step | Time | Type |
|------|------|------|
| 1. Create structure | 5 sec | AUTO |
| 2. Fill job description | 1 min | MANUAL |
| 3. **Generate prompt (script)** | **10 sec** | **AUTO ⚡** |
| 4. AI customization | 2-5 min | EXTERNAL |
| 5. **Parse AI response (script)** | **5 sec** | **AUTO ⚡** |
| 6. Verify truthfulness | 3-5 min | MANUAL |
| 7. Compile PDFs | 10 sec | AUTO |
| 8. Review PDFs | 2-3 min | MANUAL |
| 9. ATS scoring | 2-3 min | EXTERNAL |
| 10. Iterate (if needed) | 5-10 min | MANUAL |
| 11. Final compile | 10 sec | AUTO |
| 12. Track in UI | 1 min | MANUAL |
| **TOTAL (first pass)** | **~12-20 min** | **⚡ 40% faster** |
| **TOTAL (with iteration)** | **~17-30 min** | |

---

## Automation Opportunities

### ✅ Already Automated
1. Application directory creation
2. Template copying
3. Database entry creation
4. LaTeX compilation
5. PDF metadata addition
6. Review prompt generation (by AI)

### 🚀 Can Be Automated (Scripts Needed)
1. **Gathering materials and filling prompt template** ⭐ HIGH IMPACT
2. **Parsing AI response and saving to files** ⭐ HIGH IMPACT
3. Auto-opening PDFs after compilation
4. Auto-updating application status after submission

### ⚠️ Cannot/Should Not Be Automated
1. Finding and selecting job postings (requires judgment)
2. Copying job description (varies by source)
3. **Verifying truthfulness** (critical human oversight)
4. Visual PDF review (formatting, readability)
5. Deciding whether to iterate based on ATS score
6. Making judgment calls on feedback

---

## Recommended Automation Scripts

### Script 1: Generate Customization Prompt (HIGH PRIORITY)

**Purpose:** Auto-gather materials and fill prompt template

```bash
#!/bin/bash
# scripts/generate_customization_prompt.sh

DIR_NAME=$1
APP_DIR="applications/${DIR_NAME}"
PROMPT_TEMPLATE="docs/RESUME_CUSTOMIZATION_PROMPT.md"
OUTPUT="customization_prompt_filled.txt"

# Extract the prompt template section
awk '/^```$/,/^```$/' "$PROMPT_TEMPLATE" | sed '1d;$d' > "$OUTPUT"

# Gather materials
JOB_DESC=$(cat "$APP_DIR/job_description.txt")
CURRENT_RESUME=$(cat "$APP_DIR/resume.tex")
BASE_RESUME=$(cat "templates/base_master_resume.tex")
SOURCE_MATERIAL=$(find source_material -name "*.md" -exec cat {} \; 2>/dev/null)

# Replace placeholders
sed -i "s|\[PASTE job_description.txt CONTENT HERE\]|$JOB_DESC|g" "$OUTPUT"
sed -i "s|\[PASTE current resume.tex CONTENT HERE\]|$CURRENT_RESUME|g" "$OUTPUT"
sed -i "s|\[PASTE base_master_resume.tex.*\]|$BASE_RESUME|g" "$OUTPUT"
sed -i "s|\[PASTE content from source_material.*\]|$SOURCE_MATERIAL|g" "$OUTPUT"

echo "✓ Generated: $OUTPUT"
echo "→ Send this file to your AI assistant"
```

**Time saved:** ~8-10 minutes per application

---

### Script 2: Parse AI Response (HIGH PRIORITY)

**Purpose:** Auto-extract sections from AI response and save to files

```bash
#!/bin/bash
# scripts/parse_ai_response.sh

AI_RESPONSE=$1
APP_DIR=$2

# Extract SECTION 1 (resume)
awk '/SECTION 1.*RESUME/,/SECTION 2/' "$AI_RESPONSE" | \
  awk '/```latex$/,/```$/' | sed '1d;$d' > "$APP_DIR/resume.tex"

# Extract SECTION 2 (cover letter)
awk '/SECTION 2.*COVER LETTER/,/SECTION 3/' "$AI_RESPONSE" | \
  awk '/```latex$/,/```$/' | sed '1d;$d' > "$APP_DIR/cover_letter.tex"

# Extract SECTION 3 (review prompt)
awk '/SECTION 3.*REVIEW PROMPT/,/SECTION 4/' "$AI_RESPONSE" | \
  sed '1,/```$/d;/```$/,$d' > "$APP_DIR/review_prompt.txt"

echo "✓ Saved resume.tex"
echo "✓ Saved cover_letter.tex"
echo "✓ Saved review_prompt.txt"
```

**Time saved:** ~2 minutes per application

---

### Script 3: End-to-End Helper (CONVENIENCE)

**Purpose:** Combine multiple steps

```bash
#!/bin/bash
# scripts/customize_application_automated.sh

DIR_NAME=$1

echo "=== Automated Customization Workflow ==="
echo ""
echo "Step 1: Generating customization prompt..."
./scripts/generate_customization_prompt.sh "$DIR_NAME"

echo ""
echo "Step 2: Copy customization_prompt_filled.txt to your AI assistant"
echo "        (Claude, GitHub Copilot, ChatGPT)"
echo ""
read -p "Press Enter after AI responds and you've saved response to ai_response.txt..."

echo ""
echo "Step 3: Parsing AI response..."
./scripts/parse_ai_response.sh ai_response.txt "applications/$DIR_NAME"

echo ""
echo "Step 4: Compiling PDFs..."
./scripts/compile_application.sh "$DIR_NAME"

echo ""
echo "✓ Done! Review PDFs in applications/$DIR_NAME/"
echo ""
echo "Next: Send review_prompt.txt to AI for ATS scoring"
```

**Time saved:** ~10-12 minutes per application (full workflow)

---

## Future Automation Ideas

### Web UI Integration (Long-term)
1. Paste job description in UI
2. Click "Customize with AI" button
3. UI calls AI API directly (OpenAI, Anthropic)
4. Auto-saves results and compiles PDFs
5. Shows ATS score in dashboard
6. One-click iteration with improvements

**Potential time:** ~5-10 minutes per application (70% reduction)

### AI API Integration
- Direct API calls instead of copy-paste
- Streaming responses for real-time feedback
- Automatic retry with improvements
- Batch processing multiple applications

### Source Material Editor
- Web-based interface for managing source_material/
- Templates for STAR format
- Version control integration
- Search/filter experiences

---

## Recommendation

### Immediate Actions (High ROI)

1. **Create the two automation scripts:**
   - `generate_customization_prompt.sh` (saves ~8-10 min)
   - `parse_ai_response.sh` (saves ~2 min)

2. **Update workflow documentation** to reference these scripts

3. **Create end-to-end helper script** for convenience

**Total development time:** ~2-3 hours
**Time saved per application:** ~10-12 minutes
**Break-even:** After 10-15 applications

### Long-term Enhancements

1. **Web UI integration** with AI API
2. **Source material editor** in web UI
3. **ATS score tracking** and history
4. **A/B testing** of resume versions

---

## Bottlenecks That Cannot Be Removed

1. **Job description gathering** - requires human judgment on which jobs to apply to
2. **Truthfulness verification** - critical human oversight to prevent false claims
3. **AI processing time** - external service (2-5 minutes)
4. **Visual review** - ensuring PDFs look professional
5. **Decision-making** - whether to iterate based on ATS score

---

## Summary

**Current workflow:** ~20-30 minutes per application
**Optimized workflow (with scripts):** ~12-20 minutes per application (40% faster)
**Future workflow (full web integration):** ~5-10 minutes per application (75% faster)

**Key insight:** The critical path includes unavoidable human review steps (truthfulness, visual quality) and external AI processing. Automation should focus on:
- Eliminating copy-paste operations
- Auto-compiling and formatting
- Streamlining handoffs between steps

The proposed scripts target the highest-impact automation opportunities while preserving essential human oversight.
