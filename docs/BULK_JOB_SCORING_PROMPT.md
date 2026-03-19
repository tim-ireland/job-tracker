# Bulk Job Scoring Prompt Template

This document explains how to use the bulk job scoring feature to evaluate multiple job opportunities against your background.

## Purpose

When you have many job opportunities (e.g., 40 LinkedIn saved jobs), manually reviewing each one is time-consuming. This tool helps you:

1. **Generate a scoring prompt** with all jobs and your background
2. **Send to AI** (Claude, ChatGPT, or local LLM) for bulk evaluation
3. **Parse the response** to update your database with scores
4. **Prioritize** which jobs to customize applications for

## Workflow

### Step 1: Create Applications (Manual for now)

For each job, create an application and save the job description:

```bash
./job-tracker create "Google" "Senior Engineering Manager" manager \
    --job-url="https://..." \
    --status="Pipeline" \
    --priority="P4"

# Save job description
cat > $DATA_PATH/applications/Google_Senior_Engineering_Manager/job_description.txt << 'EOF'
[Paste job description here]
EOF
```

Repeat for all 40 jobs. This takes ~5-10 minutes.

### Step 2: Generate Bulk Scoring Prompt

From the UI (or via API endpoint - coming in Phase 3):

1. Click "Actions" → "Score Pipeline Jobs"
2. System generates a prompt containing:
   - Your resume summary
   - Your source material highlights
   - All 40 job descriptions
   - Scoring instructions
3. Copy the prompt

**Prompt Structure:**
- Your background (resume + achievements)
- Job descriptions (all 40)
- Scoring criteria (0-100 scale)
- Output format (JSON with scores, reasoning, strengths, gaps)

### Step 3: Get AI Scores

1. **Paste prompt** into Claude, ChatGPT, or local LLM
2. **Wait for response** (usually 30-60 seconds for 40 jobs)
3. **Copy JSON response**

**Example Response:**
```json
{
  "evaluations": [
    {
      "application_id": 1,
      "company": "Google",
      "role": "Senior Engineering Manager",
      "score": 85,
      "reasoning": "Excellent management fit with director-level experience exceeding requirements. Strong technical alignment on distributed systems and data platforms. Gap: No search-specific experience though has query optimization background.",
      "strengths": [
        "Management scope (45-person org)",
        "Distributed systems expertise",
        "Operational excellence track record"
      ],
      "gaps": [
        "Search engine experience",
        "Consumer product at scale"
      ],
      "recommendation": "Apply"
    },
    ...
  ]
}
```

### Step 4: Parse and Update Database

1. **Paste AI response** into the tool
2. **Click "Parse Scores"**
3. System updates database with:
   - match_score (0-100)
   - match_reasoning
   - match_strengths (JSON array)
   - match_gaps (JSON array)
   - match_recommendation (Apply/Reach/Skip)
   - evaluated_at timestamp

### Step 5: Review and Prioritize

Applications table now shows:
- **Match Score** column with color-coded badges
  - 🟢 Green (80-100): Excellent fit
  - 🔵 Blue (70-79): Good fit
  - 🟡 Yellow (60-69): Moderate fit
  - 🔴 Red (<60): Poor fit
- **Sort by score** (highest first)
- **Click score** to see reasoning, strengths, gaps

**Focus your effort:**
- Score 85-100: Definitely customize and apply (5-8 jobs)
- Score 75-84: Apply if time allows (10-12 jobs)
- Score 60-74: Reach roles, apply selectively (12-15 jobs)
- Score <60: Skip, better opportunities exist (10-15 jobs)

### Step 6: Selective Customization

Only customize applications for high-scoring matches:

```bash
# Work on top matches
./job-tracker customize Google_Senior_Engineering_Manager
./job-tracker customize Meta_Engineering_Manager

# Skip low scores entirely
```

## Scoring Criteria

**Management Experience (0-30 points):**
- Years managing people
- Managing managers
- Organization size
- Director-level scope
- Cross-functional leadership

**Technical Skills (0-25 points):**
- Programming languages match
- Frameworks and tools
- Architecture experience
- System design
- Specific technologies required

**Domain/Industry (0-20 points):**
- Industry experience (e.g., real estate, fintech, enterprise)
- Product type (B2B, B2C, platform, infrastructure)
- Domain expertise (search, ML, data, security)

**Years of Experience (0-15 points):**
- Total years required vs actual
- Seniority level match

**Company/Role Level (0-10 points):**
- IC vs Manager vs Senior Manager vs Director
- Scope of responsibility
- Team size expectations

## Score Interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| 90-100 | Excellent fit, minimal gaps | Definitely apply, high priority |
| 80-89 | Strong fit, minor gaps | Apply, good odds |
| 70-79 | Good fit, notable gaps or reach | Apply if interested, prepare for gap discussion |
| 60-69 | Moderate fit, significant gaps | Reach role, apply selectively |
| <60 | Poor fit, major gaps | Skip, focus on better matches |

## Benefits

**Time Savings:**
- Before: 5-10 hours reviewing 40 jobs manually
- After: 30 minutes to score + focus time on top matches
- **Saves 4-9 hours per batch**

**Better Outcomes:**
- Data-driven prioritization
- More time per high-quality application
- No wasted effort on poor fits
- Can process more job batches

**Strategic Insights:**
- Pattern recognition (what types of roles fit best)
- Gap identification (skills to highlight or develop)
- Market positioning (where you're competitive)

## Tips

1. **Be honest with scores** - Don't inflate, it wastes time later
2. **Consider transferables** - E.g., "distributed query systems" relates to "search"
3. **Focus on top 15-20** - Quality over quantity
4. **Update regularly** - Re-score as you gain experience
5. **Track outcomes** - Which scores convert to interviews/offers?

## Future Enhancements

- **Auto-scraping** job descriptions from URLs (Phase 6)
- **API integration** for automatic scoring (no copy-paste)
- **Historical tracking** of score vs interview conversion rate
- **Score calibration** based on actual outcomes
- **Batch import** from LinkedIn saved jobs

---

*This is a living document. Update as the feature evolves.*
