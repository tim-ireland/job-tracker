# Resume Customization Prompt - Conservative Approach

**Purpose:** Generate customized resume and cover letter for a specific job application while staying truthful to your actual experience and accomplishments.

**Philosophy:** Be strategic and keyword-aware, but NEVER fabricate experience or exaggerate accomplishments. Only use material from your actual work history.

---

## How to Use This Prompt

1. **Gather required materials** (see checklist below)
2. **Copy the prompt template** from this document
3. **Replace placeholders** with actual content from your files
4. **Send to your AI assistant** (Claude, GitHub Copilot Chat, ChatGPT, etc.)
5. **Review the generated resume/cover letter** carefully for accuracy
6. **Verify** that no claims are made about work you haven't done
7. **Use the output** to replace content in your `resume.tex` and `cover_letter.tex`

---

## Required Materials Checklist

Before using this prompt, gather these files:

- [ ] `job_description.txt` - The job posting you're applying to
- [ ] `resume.tex` - Your current role-specific template (e.g., manager_resume.tex, developer_resume.tex)
- [ ] Base master resume (from `/templates/base_master_resume.tex` or your personal version)
- [ ] `source_material/` directory contents - Your documented experiences, achievements, projects
- [ ] Base master cover letter (from `/templates/base_master_cover_letter.tex`)

---

## Source Material Structure

Your `source_material/` directory should contain documented evidence of your work. Organize it like:

```
source_material/
├── experiences/
│   ├── aruba_hpe.md              # Your work at each company
│   ├── plexxi.md
│   └── arbor_networks.md
├── achievements/
│   ├── ci_cd_transformation.md   # Specific major achievements
│   ├── device_config_migration.md
│   └── ai_adoption.md
├── skills/
│   ├── technical_skills.md       # Languages, frameworks, tools
│   ├── leadership_skills.md      # People management, mentoring
│   └── certifications.md
├── projects/
│   └── notable_projects.md       # Side projects, open source
└── metrics/
    └── quantified_results.md     # Numbers, percentages, scale
```

**Important:** Only include truthful, verifiable information in source material. This is your single source of truth.

---

## Prompt Template

```
I need you to customize a resume and cover letter for a specific job application. Follow these critical rules:

## RULES - READ CAREFULLY:

1. **TRUTHFULNESS IS PARAMOUNT**: Only use experiences, skills, and achievements that are documented in the source materials provided. Do NOT fabricate, embellish, or infer experiences.

2. **CONSERVATIVE APPROACH**: When in doubt, leave something out rather than exaggerate. It's better to undersell slightly than to make false claims.

3. **USE THEIR LANGUAGE**: Incorporate keywords and phrases from the job description, but only where they truthfully apply to documented experience.

4. **QUANTIFY WHEN POSSIBLE**: Use metrics from source material, but never make up numbers.

5. **RESPECT TEMPLATE STRUCTURE**: Maintain the LaTeX structure and formatting of the template provided.

6. **PRESERVE EXISTING CONTENT**: Start with the role-specific template, enhance with base master resume content, and supplement with source material. Don't remove working content unless replacing with something stronger.

---

## JOB DESCRIPTION:
```
[PASTE job_description.txt CONTENT HERE]
```

---

## CURRENT ROLE-SPECIFIC TEMPLATE RESUME:
```
[PASTE current resume.tex CONTENT HERE]
```

---

## BASE MASTER RESUME (for reference):
```
[PASTE base_master_resume.tex or your master resume CONTENT HERE]
```

---

## SOURCE MATERIAL:

### Experiences:
```
[PASTE content from source_material/experiences/*.md files]
```

### Achievements:
```
[PASTE content from source_material/achievements/*.md files]
```

### Skills:
```
[PASTE content from source_material/skills/*.md files]
```

### Projects (if relevant):
```
[PASTE content from source_material/projects/*.md files]
```

### Metrics & Quantified Results:
```
[PASTE content from source_material/metrics/*.md files]
```

---

## CUSTOMIZATION INSTRUCTIONS:

### For the RESUME:

#### 1. Professional Summary (CRITICAL SECTION)
- Rewrite to align with the target role and company
- Use keywords from job description that match your actual experience
- Highlight the 2-3 most relevant achievements from source material
- Keep to 3-4 sentences maximum
- MUST truthfully represent your background
- Include years of experience that match reality

#### 2. Core Competencies / Skills
- Review required skills in job description
- List ONLY skills you actually have (from source material)
- Prioritize skills mentioned in job description that you possess
- Include both technical and soft skills
- Use their exact terminology when you have that skill
- Do NOT add skills you don't have, even if required

#### 3. Professional Experience
For each role:
- **Keep existing structure** from template
- **Enhance bullet points** that relate to job requirements
- **Add missing relevant achievements** from source material
- **Use keywords** from job description where applicable
- **Quantify results** using metrics from source material
- **Reorder bullets** to put most relevant first
- **Remove or de-emphasize** content not relevant to this role
- **DO NOT** add responsibilities or achievements not documented

Focus areas based on job description:
- [List 3-5 key focus areas from the job description]
- [For each, identify which source materials are relevant]

#### 4. Format & Structure
- Maintain LaTeX formatting from template
- Ensure consistent date formats
- Keep section headers clear
- Use strong action verbs
- Keep consistent bullet point style

---

### For the COVER LETTER:

#### 1. Opening Paragraph
- Express genuine interest in the specific role and company
- Mention 1-2 key qualifications that make you a strong fit
- Reference the job title exactly as posted
- Keep to 3-4 sentences

#### 2. Body Paragraphs (2-3 paragraphs)

**Paragraph 1 - Relevant Experience:**
- Highlight experience most relevant to role
- Use 1-2 specific examples from source material
- Connect your experience to their needs
- Include quantified achievements where relevant

**Paragraph 2 - Skills & Approach:**
- Discuss how your skills align with their requirements
- Mention specific technologies, methodologies, or approaches they emphasized
- Reference their company mission, values, or recent initiatives (if mentioned in JD)
- Show understanding of their challenges and how you can help

**Paragraph 3 (optional) - Cultural Fit:**
- If job description emphasizes culture, values, or team dynamics
- Explain why you're drawn to their company specifically
- Reference their mission or values authentically
- Keep brief - 2-3 sentences

#### 3. Closing Paragraph
- Reiterate interest and fit
- Express enthusiasm for discussing further
- Professional but warm tone
- 2-3 sentences maximum

#### 4. Tone & Style
- Professional but personable
- Confident but not arrogant
- Specific, not generic
- Authentic to how you actually communicate
- NO clichés or buzzwords without substance

---

## OUTPUT FORMAT:

Please provide TWO sections in your response:

### SECTION 1: CUSTOMIZED RESUME

```latex
[Provide the complete customized resume.tex content]
[Use proper LaTeX formatting]
[Maintain the template structure]
```

### SECTION 2: CUSTOMIZED COVER LETTER

```latex
[Provide the complete customized cover_letter.tex content]
[Use proper LaTeX formatting]
[Maintain the template structure]
```

### SECTION 3: REVIEW PROMPT

Now, generate the complete review prompt by filling in this template:

```
I need you to perform a comprehensive resume review against a job description. Please analyze the resume using ATS (Applicant Tracking System) criteria and check for writing quality issues.

### JOB DESCRIPTION:
```
[COPY THE JOB DESCRIPTION PROVIDED ABOVE]
```

### RESUME CONTENT:
```
[COPY THE CUSTOMIZED RESUME.TEX CONTENT YOU JUST GENERATED]
```

[THEN INCLUDE THE REST OF THE REVIEW PROMPT FROM /docs/RESUME_REVIEW_PROMPT.md]
```

### SECTION 4: CUSTOMIZATION NOTES

Provide a brief summary of:

**Changes Made:**
1. [List major changes to resume]
2. [List major changes to cover letter]

**Keywords Incorporated:**
- [List key terms from JD that were naturally integrated]

**Source Material Used:**
- [List which source files were referenced]

**Truthfulness Check:**
- Confirm: "All content is based on documented source material. No fabricated experience or exaggerated claims."
- OR flag: "⚠️ Note: I was unable to address [X requirement] due to lack of source material documenting this experience."

**Suggestions for Source Material:**
- [If any gaps were found, suggest what to document for future applications]

---

## IMPORTANT REMINDERS:

1. **Verify every claim**: If you're not sure whether I have experience with something, DON'T include it
2. **Use my words when possible**: Prefer phrasing from source material over creating new descriptions
3. **Match their keywords**: Use exact terminology from job description when truthfully applicable
4. **Quantify strategically**: Use numbers from source material; don't estimate or approximate
5. **Preserve LaTeX structure**: Don't break formatting; maintain template style
6. **Stay conservative**: Better to have a 90% match with 100% truth than 100% match with 95% truth
7. **Flag gaps**: Tell me if requirements can't be met with available source material
```

---

## Workflow Integration

### Complete Customization Workflow

```bash
# 1. Navigate to application directory
cd /data/applications/Company_JobTitle

# 2. Gather all materials
cat job_description.txt
cat resume.tex
cat /data/templates/base_master_resume.tex
find /data/source_material -type f -name "*.md" -exec cat {} \;

# 3. Open customization prompt
cat /app/docs/RESUME_CUSTOMIZATION_PROMPT.md

# 4. Fill in the template with your materials

# 5. Send to AI assistant

# 6. Review output carefully
#    - Check every claim for truthfulness
#    - Verify metrics are accurate
#    - Ensure no fabricated experience

# 7. Save customized resume
# Copy SECTION 1 output to resume.tex

# 8. Save customized cover letter  
# Copy SECTION 2 output to cover_letter.tex

# 9. Save review prompt for later
# Copy SECTION 3 output to review_prompt.txt

# 10. Compile PDFs
pdflatex resume.tex && pdflatex resume.tex
pdflatex cover_letter.tex && pdflatex cover_letter.tex

# 11. Review PDFs
open resume.pdf cover_letter.pdf

# 12. If satisfied, run the review prompt (SECTION 3)
#     Send review_prompt.txt to AI assistant for ATS scoring

# 13. Make final adjustments based on ATS feedback

# 14. Final compile with metadata
/app/scripts/compile_application.sh $(basename $(pwd))
```

---

## Source Material Best Practices

### What to Document

**For Each Job/Experience:**
```markdown
# Company Name - Role Title (Dates)

## Overview
[Brief description of role, team size, reporting structure]

## Key Responsibilities
- [Specific responsibility with context]
- [Specific responsibility with context]

## Major Achievements
### Achievement Name
- **Context**: [What was the problem/opportunity]
- **Action**: [What you did specifically]
- **Result**: [Quantified outcome]
- **Technologies**: [Tools, languages, frameworks used]
- **Timeline**: [How long it took]

### Another Achievement
...

## Skills Demonstrated
- Technical: [Specific technologies/languages]
- Leadership: [People management, mentoring]
- Process: [Methodologies, improvements]

## Metrics & Scale
- Team size: X people
- Budget: $X
- Users/Customers impacted: X
- Performance improvements: X%
- Time savings: X hours/days
```

**For Skills:**
```markdown
# Skill Category (e.g., Python Programming)

## Proficiency Level
[Beginner / Intermediate / Advanced / Expert]

## Years of Experience
[X years]

## Projects Using This Skill
1. [Project name] - [Brief description]
2. [Project name] - [Brief description]

## Specific Capabilities
- [Specific thing you can do]
- [Frameworks/libraries you've used]
- [Size/scale of systems built]

## Can Teach Others
[Yes/No - important for leadership roles]
```

### What NOT to Include

❌ Vague statements: "Worked on various projects"
❌ Unquantified claims: "Significantly improved performance"
❌ Skills you've only read about
❌ Responsibilities from job descriptions you didn't actually do
❌ Team achievements where you weren't a key contributor

✅ Specific, verifiable, quantified achievements
✅ Skills you've actually used in production
✅ Responsibilities you personally handled
✅ Your individual contributions to team efforts

---

## Example Source Material

### Example: CI/CD Achievement

```markdown
# CI/CD Transformation Achievement

## Context
- Organization had 450+ developers
- Build times were 8 hours for full pipeline
- Blocking development velocity significantly
- Distributed monolith architecture
- Multiple teams affected

## My Role
- Engineering Manager leading the initiative
- Championed the project to leadership
- Secured buy-in during hiring freeze
- Led team of X developers/devops engineers
- Made architectural decisions on refactoring approach

## Actions Taken
1. Analyzed bottlenecks in existing pipeline
2. Proposed refactoring strategy to leadership
3. Secured resources and team allocation
4. Led technical design sessions
5. Mentored team on implementation
6. Measured and tracked improvements

## Results (Quantified)
- Reduced build times from 8 hours to 40 minutes (86% reduction)
- Impacted 450+ developers
- Timeline: [X months from start to finish]
- Adoption rate: [X% of teams migrated in Y months]

## Technologies Used
- CI/CD: [Specific tools - Jenkins, GitHub Actions, etc.]
- Containerization: Docker, Kubernetes
- Languages: [Languages involved in refactoring]
- Infrastructure: [Cloud provider, IaC tools]

## Skills Demonstrated
- Technical Leadership
- Stakeholder Management
- DevOps/Platform Engineering
- Performance Optimization
- Team Leadership
```

This level of detail allows conservative but powerful customization.

---

## Validation Checklist

After receiving customized resume/cover letter, verify:

### Resume Validation
- [ ] Every job title, company, and date is accurate
- [ ] Every achievement listed is documented in source material
- [ ] All metrics/numbers are accurate (not rounded or estimated)
- [ ] Skills listed are skills you actually possess
- [ ] Technologies mentioned are ones you've actually used
- [ ] No responsibilities claimed that you didn't have
- [ ] LaTeX formatting is intact and compiles
- [ ] Dates are consistent and formatted correctly
- [ ] No typos or grammatical errors introduced

### Cover Letter Validation
- [ ] Company name spelled correctly
- [ ] Job title matches posting exactly
- [ ] Claims about interest/motivation are genuine
- [ ] Examples referenced are real and documented
- [ ] Tone sounds like how you actually write/speak
- [ ] No generic placeholder text remains
- [ ] No exaggerated language or false enthusiasm
- [ ] LaTeX formatting is intact and compiles

### Review Prompt Validation
- [ ] Job description is complete and accurate
- [ ] Resume content matches what you approved
- [ ] Prompt structure is complete (all sections included)
- [ ] Ready to send to AI for ATS scoring

---

## Troubleshooting

### Issue: AI Suggests Adding Experience You Don't Have

**Response:**
"Thank you for the suggestion, but I don't have documented experience with [X]. Please only include content based on the source material provided. If you believe this is a critical requirement, please flag it in the Customization Notes so I can consider whether to apply for this role."

### Issue: AI Exaggerates Metrics

**Response:**
"Please use only the exact metrics provided in source material. Do not round up, estimate, or extrapolate. If a metric wasn't provided, either omit it or use qualitative language like 'significantly improved' instead of inventing a percentage."

### Issue: AI Creates Generic Statements

**Response:**
"Please replace generic statements with specific examples from source material. For instance, instead of 'experienced leader', use 'led team of X engineers to deliver Y project resulting in Z impact' - using actual details from the source material."

### Issue: Not Enough Source Material

**Problem:** You realize your source material is incomplete for this type of role.

**Solution:**
1. Pause the application process
2. Document your actual experience in source material files
3. Be thorough and specific
4. Come back to customization once documentation is complete
5. **Never** let AI fill gaps with fabricated content

---

## Tips for Success

### 1. Build Comprehensive Source Material First
Don't start customizing until you have well-documented source material. It's worth the time investment.

### 2. Update Source Material Continuously
After each project or achievement, document it immediately while details are fresh.

### 3. Be Specific in Source Material
The more specific your source material, the better the AI can customize conservatively.

### 4. Use Multiple Iterations
First iteration: Get structure and keyword alignment
Second iteration: Refine language and flow
Third iteration: Verify truthfulness and polish

### 5. Read Everything Out Loud
If a statement sounds exaggerated or unnatural when read aloud, it probably is.

### 6. Get a Second Opinion
Have someone who knows your work review the customized resume to verify accuracy.

---

## Version History

- **v1.0** (March 18, 2026): Initial prompt template created
- Focus: Conservative, truthful customization using documented source material

---

## Related Documentation

- [Resume Review Prompt](./RESUME_REVIEW_PROMPT.md) - Use after customization
- [Project Context](../PROJECT_CONTEXT.md) - Overall project documentation
- [Workflow Overview](../README.md#usage) - Complete application workflow
- [Template Documentation](../templates/README.md) - Template reference

---

*Remember: Your reputation and career are built on trust. Never compromise truthfulness for a perceived better fit. The right role will value your actual experience.*
