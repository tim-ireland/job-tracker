# Resume Review Prompt - ATS Scoring & Quality Check

**Purpose:** Final quality check before submitting application. This prompt evaluates resume against the job description using ATS (Applicant Tracking System) scoring criteria and checks for writing quality issues.

**When to Use:** After customizing your resume and cover letter, before generating final PDFs.

---

## How to Use This Prompt

1. **Compile your resume to PDF** (or have the .tex source ready)
2. **Copy the prompt template below**
3. **Replace placeholders** with actual content:
   - `[JOB_DESCRIPTION]` - Paste from `job_description.txt`
   - `[RESUME_CONTENT]` - Paste your resume text (from .tex or extracted from PDF)
4. **Send to your AI assistant** (Claude, GitHub Copilot Chat, ChatGPT, etc.)
5. **Review results** and make improvements based on feedback
6. **Iterate** until you achieve desired ATS score

---

## Prompt Template

```
I need you to perform a comprehensive resume review against a job description. Please analyze the resume using ATS (Applicant Tracking System) criteria and check for writing quality issues.

### JOB DESCRIPTION:
```
[PASTE JOB DESCRIPTION HERE - from job_description.txt]
```

### RESUME CONTENT:
```
[PASTE RESUME TEXT HERE - from resume.tex or extracted PDF]
```

---

## ANALYSIS REQUESTED:

### 1. ATS SCORING (0-100 scale)

**Overall ATS Score:** [Provide numeric score]

Please evaluate and score the following categories (0-100 each):

#### A. Keyword Match (Weight: 35%)
- **Score:** __/100
- **Analysis:**
  - List critical keywords from job description that ARE present in resume
  - List critical keywords that are MISSING from resume
  - Identify synonyms or related terms used effectively
  - Note keyword density (natural vs. keyword stuffing)

#### B. Skills Alignment (Weight: 25%)
- **Score:** __/100
- **Analysis:**
  - Required skills present vs. missing
  - Nice-to-have skills present vs. missing
  - Technical skills match
  - Soft skills match
  - Certifications/qualifications alignment

#### C. Experience Relevance (Weight: 25%)
- **Score:** __/100
- **Analysis:**
  - How well does work history align with role requirements?
  - Are achievements quantified and relevant?
  - Does experience progression make sense for this role?
  - Are there experience gaps that might raise questions?

#### D. Format & Structure (Weight: 15%)
- **Score:** __/100
- **Analysis:**
  - ATS-friendly formatting (no tables, columns, headers/footers with critical info)
  - Clear section headers
  - Consistent formatting
  - Appropriate use of bullet points
  - Date formats consistent and parseable

---

### 2. KEYWORD OPTIMIZATION RECOMMENDATIONS

**High-Priority Missing Keywords:**
1. [keyword] - appears [X] times in JD, [0] times in resume
2. [keyword] - appears [X] times in JD, [0] times in resume
3. ...

**Suggested Additions:**
- Where to add: [specific section]
- How to incorporate: [specific suggestion]

**Overused Keywords (possible keyword stuffing):**
- [keyword]: used [X] times (reduce to [Y] for natural flow)

---

### 3. WRITING QUALITY CHECK

#### A. Spelling Errors
- [ ] No spelling errors found
- [List any spelling errors with line/section reference]

#### B. Grammar Issues
- [ ] No grammar errors found
- [List any grammar issues with corrections suggested]

#### C. Capitalization
- [ ] Consistent and correct capitalization
- [List any capitalization inconsistencies]
  - Company names properly capitalized
  - Product names match official capitalization
  - Acronyms handled consistently

#### D. Punctuation
- [ ] Correct and consistent punctuation
- [List any punctuation issues]
  - Bullet points ending consistently (all with periods or none with periods)
  - Proper use of commas, semicolons, colons
  - Hyphenation consistency (e.g., "full-stack" vs "full stack")

#### E. Repetition & Redundancy
- [ ] No significant repetition found
- [List phrases or words used repetitively]
- [Suggest alternatives or consolidation]

#### F. Run-on Sentences
- [ ] No run-on sentences found
- [List any run-on sentences with suggested splits]

#### G. Passive vs. Active Voice
- [ ] Predominantly active voice
- [List instances of passive voice that should be active]
- Strong action verbs used: [Yes/No - provide examples]

---

### 4. CONTENT QUALITY ASSESSMENT

#### A. Quantifiable Achievements
- [ ] Achievements include metrics and impact
- [List bullets that lack quantification and suggest improvements]
  - Example: "Improved build times" → "Reduced build times by 86% (8 hrs to 40 min)"

#### B. Relevance to Target Role
- [ ] All content directly relevant to role
- [List any content that seems off-topic or should be de-emphasized]
- [List experiences that should be emphasized more]

#### C. Value Proposition Clarity
- Is it immediately clear why this candidate is a good fit? [Yes/No]
- Does the professional summary effectively position the candidate? [Yes/No]
- [Specific feedback]

---

### 5. COMPETITIVE POSITIONING

**Strengths for This Role:**
1. [Specific strength with evidence from resume]
2. [Specific strength with evidence from resume]
3. ...

**Potential Concerns:**
1. [Possible objection with mitigation suggestion]
2. [Possible objection with mitigation suggestion]
3. ...

**Differentiation:**
- What makes this resume stand out? [Specific observations]
- What's missing that competitors might have? [Gaps]

---

### 6. SECTION-BY-SECTION FEEDBACK

#### Professional Summary
- **Effectiveness:** [Rating 1-5]
- **Feedback:** [Specific suggestions]

#### Core Competencies / Skills
- **Effectiveness:** [Rating 1-5]
- **Feedback:** [Specific suggestions]

#### Professional Experience
- **Effectiveness:** [Rating 1-5]
- **Feedback:** [Specific suggestions per role if needed]

#### Education / Certifications
- **Effectiveness:** [Rating 1-5]
- **Feedback:** [Specific suggestions]

---

### 7. FINAL RECOMMENDATIONS

**Priority 1 (Critical - Fix Before Submitting):**
1. [Issue with specific fix]
2. [Issue with specific fix]
3. ...

**Priority 2 (Important - Strongly Recommended):**
1. [Issue with specific fix]
2. [Issue with specific fix]
3. ...

**Priority 3 (Nice to Have - Consider if Time Permits):**
1. [Suggestion]
2. [Suggestion]
3. ...

---

### 8. SUBMISSION READINESS

**Overall Assessment:** [Ready / Needs Minor Revisions / Needs Major Revisions]

**Estimated Impact of Recommended Changes:**
- Current ATS Score: __/100
- Potential ATS Score After Revisions: __/100

**Expected Screening Outcome:** [Likely Pass / Borderline / Likely Filtered Out]

**Final Verdict:** [Your recommendation on whether to submit as-is or revise]

---

## IMPORTANT NOTES:
- Be specific with line/section references where possible
- Provide actionable suggestions, not just criticism
- Consider both ATS algorithmic scoring AND human reviewer appeal
- Balance keyword optimization with natural, compelling writing
- Prioritize recommendations by impact on application success
```

---

## Tips for Best Results

### Preparing Resume Content
- **From LaTeX (.tex file):** Copy just the content sections, excluding LaTeX commands if possible
- **From PDF:** Use a PDF text extraction tool or copy-paste (watch for formatting artifacts)
- **Best practice:** Have AI assistant review the raw .tex file to understand structure

### Interpreting ATS Scores
- **90-100:** Excellent match, very likely to pass ATS screening
- **80-89:** Good match, likely to pass with strong presentation
- **70-79:** Moderate match, may pass but needs improvement
- **60-69:** Weak match, significant revisions needed
- **Below 60:** Poor match, major overhaul required or wrong fit

### Common Issues to Watch For
1. **Keyword stuffing:** Don't just add keywords unnaturally - integrate them into achievements
2. **Generic language:** Replace generic phrases with specific, quantified achievements
3. **Missing context:** Ensure acronyms are spelled out on first use
4. **Inconsistent formatting:** Keep bullet styles, date formats, and capitalization consistent
5. **Outdated information:** Remove or minimize very old experience that's not relevant

### Iteration Strategy
1. **First pass:** Focus on ATS score and critical missing keywords
2. **Second pass:** Address writing quality issues (grammar, spelling, etc.)
3. **Third pass:** Polish content for human appeal (storytelling, impact, clarity)
4. **Final check:** Read aloud to catch awkward phrasing or repetition

---

## Integration with Workflow

### Step-by-Step Usage

```bash
# 1. Navigate to your application directory
cd /data/applications/Company_JobTitle

# 2. Ensure your resume is customized
# (edit resume.tex)

# 3. Copy the job description
cat job_description.txt

# 4. Extract resume content (if using PDF)
pdftotext resume.pdf resume_text.txt
cat resume_text.txt

# OR work directly from .tex file
cat resume.tex

# 5. Open this prompt file
cat /app/docs/RESUME_REVIEW_PROMPT.md

# 6. Use the prompt template with your AI assistant

# 7. Make recommended revisions to resume.tex

# 8. Re-compile and re-check
pdflatex resume.tex && pdflatex resume.tex

# 9. Repeat until satisfied with score

# 10. Generate final PDFs
/app/scripts/compile_application.sh $(basename $(pwd))
```

---

## Example Output Structure

When the AI assistant responds, expect something like:

```
### 1. ATS SCORING (0-100 scale)

**Overall ATS Score:** 78/100

#### A. Keyword Match (Weight: 35%)
- **Score:** 72/100
- **Analysis:**
  - Present: CI/CD (5x), Kubernetes (3x), Python (4x), Infrastructure (8x)
  - MISSING: "Developer Experience" (appears 4x in JD, 0x in resume)
  - MISSING: "Platform Engineering" (appears 3x in JD, 0x in resume)
  - Using synonym: "Build systems" instead of "Build pipelines" (good)
  - Keyword density: Natural integration, not stuffed

#### B. Skills Alignment (Weight: 25%)
- **Score:** 85/100
- **Analysis:**
  - Required skills present (12/14):
    ✓ Python, TypeScript, Go
    ✓ CI/CD pipeline optimization
    ✓ Kubernetes
    ✓ AWS
    ...
  - Missing required skills (2/14):
    ✗ Pants (build system) - not mentioned
    ✗ FastAPI - mentioned in different context
  ...
```

---

## Advanced Usage

### For Cover Letters
Modify the prompt to review cover letters:
- Focus less on ATS scoring (cover letters often aren't parsed)
- Emphasize tone, personality, and storytelling
- Check for company-specific customization
- Verify no generic placeholders remain

### Comparing Multiple Versions
Use the prompt to compare:
- Before/after revisions
- Different template approaches
- Role-specific vs. general resume

### Tracking Improvements
Create a log file to track ATS scores over time:
```bash
echo "$(date): Company_JobTitle - ATS Score: 78/100" >> /data/ats_scores.log
```

---

## Troubleshooting

### AI Assistant Not Providing Numeric Scores
- Explicitly request: "Please provide numeric scores for each category"
- Simplify: Break the prompt into smaller pieces if too long

### Too Generic Feedback
- Provide more context about the role level (junior, senior, manager, director)
- Share specific concerns: "I'm worried about X, please focus analysis there"

### Conflicting Recommendations
- Ask for prioritization: "Which 3 changes would have the most impact?"
- Get reasoning: "Why do you recommend X over Y?"

---

## Version History

- **v1.0** (March 18, 2026): Initial prompt template created
- Focus areas: ATS scoring, writing quality, actionable feedback

---

## Related Documentation

- [Workflow Overview](../README.md#usage)
- [Customization Guide](../scripts/customize_application.sh)
- [Template Documentation](../templates/README.md)
- [Project Context](../PROJECT_CONTEXT.md)

---

*This prompt is designed to be tool-agnostic. Use it with Claude, GitHub Copilot, ChatGPT, Gemini, or any other AI assistant capable of analyzing text.*
