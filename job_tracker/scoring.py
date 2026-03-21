"""
Job scoring engine for bulk evaluation of job applications.

This module provides functionality to:
1. Generate bulk scoring prompts from multiple job applications
2. Parse AI-generated scoring responses
3. Update database with match scores
"""

import json
import os
import re
from datetime import datetime
from typing import List, Dict, Optional


class JobScorer:
    """Score job applications against candidate background"""
    
    def __init__(self, data_dir: str):
        """
        Initialize scorer with paths to resume and source material.
        
        Args:
            data_dir: Path to data directory containing resumes and source material
        """
        self.data_dir = data_dir
        # Check data dir root first, then templates/ subdirectory
        _resume_root = os.path.join(data_dir, 'base_master_resume.tex')
        _resume_templates = os.path.join(data_dir, 'templates', 'base_master_resume.tex')
        self.base_resume_path = _resume_root if os.path.exists(_resume_root) else _resume_templates
        self.source_material_dir = os.path.join(data_dir, 'source_material')
    
    def generate_bulk_prompt(self, applications: List[Dict]) -> str:
        """
        Generate prompt for bulk scoring multiple applications.
        
        Args:
            applications: List of dicts with keys: id, company, role, job_description, location, job_url
            
        Returns:
            Full prompt text to send to AI for scoring
        """
        
        # Load base resume summary
        resume_summary = self._load_resume_summary()
        
        # Load source material summary
        source_summary = self._load_source_material_summary()
        
        prompt = f"""# Bulk Job Matching Score

## Your Background

{resume_summary}

### Key Achievements & Experience Summary
{source_summary}

## Jobs to Evaluate ({len(applications)} total)

"""
        
        # Add each job
        for i, app in enumerate(applications, 1):
            job_desc = app.get('job_description', 'No description provided')
            prompt += f"""
### Job {i}: {app['company']} - {app['role']}
**Application ID:** {app['id']}
**Location:** {app.get('location', 'Not specified')}
**URL:** {app.get('job_url', 'Not provided')}

{job_desc}

---

"""
        
        prompt += """

## Task

Score each job 0-100 based on fit with background above.

**Scoring Criteria:**
- **Management experience match (0-30 points):** Years of management, managing managers, org size, director-level scope
- **Technical skills match (0-25 points):** Programming languages, frameworks, technologies, architecture experience
- **Domain/industry alignment (0-20 points):** Industry experience, domain expertise, product type familiarity
- **Years of experience match (0-15 points):** Total years required vs actual experience
- **Company/role level match (0-10 points):** Seniority level, scope of responsibility

**Scoring Guidelines:**
- Be honest about gaps - don't inflate scores
- Consider transferable skills when exact domain match isn't present
- Emphasize what candidate DOES have, not what they lack
- 90-100: Excellent fit, minimal gaps
- 80-89: Strong fit, some minor gaps
- 70-79: Good fit, some notable gaps or reach aspects
- 60-69: Moderate fit, significant gaps but transferable skills
- Below 60: Poor fit, major gaps

**Output Format (JSON):**

```json
{
  "evaluations": [
    {
      "application_id": 1,
      "company": "Company Name",
      "role": "Role Title",
      "score": 85,
      "reasoning": "Detailed explanation of score covering management fit, technical alignment, domain gaps, and overall assessment. 2-3 sentences.",
      "strengths": ["Strength 1", "Strength 2", "Strength 3"],
      "gaps": ["Gap 1", "Gap 2"],
      "recommendation": "Apply"
    },
    {
      "application_id": 2,
      "company": "Next Company",
      "role": "Next Role",
      "score": 72,
      "reasoning": "...",
      "strengths": ["..."],
      "gaps": ["..."],
      "recommendation": "Reach"
    }
  ]
}
```

**Recommendation values:**
- "Apply" - Strong fit, definitely apply
- "Reach" - Stretch role, apply if interested but expect gaps discussion
- "Skip" - Poor fit, better opportunities exist

Provide honest, actionable scoring that helps prioritize where to invest application effort.
"""
        
        return prompt
    
    def parse_scores(self, ai_response: str) -> List[Dict]:
        """
        Parse AI scoring response and extract structured data.
        
        Args:
            ai_response: JSON response from AI (may be wrapped in markdown)
            
        Returns:
            List of dicts with keys: application_id, match_score, match_reasoning, 
            match_strengths (JSON string), match_gaps (JSON string), 
            match_recommendation, evaluated_at
            
        Raises:
            ValueError: If response cannot be parsed as valid JSON
        """
        
        # Try to extract JSON from markdown code blocks
        json_match = re.search(r'```json\s*(.*?)\s*```', ai_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find JSON object directly
            json_match = re.search(r'\{.*"evaluations".*\}', ai_response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = ai_response
        
        try:
            # Clean control characters from JSON string more aggressively
            # Remove all literal control characters (newlines, tabs, etc.)
            import string
            # Create translation table to remove control characters except spaces
            control_chars = ''.join(c for c in map(chr, range(32)) if c not in '\t\n\r')
            trans_table = str.maketrans('', '', control_chars)
            json_str = json_str.translate(trans_table)
            
            # Now replace newlines and tabs with spaces
            json_str = json_str.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
            # Normalize multiple spaces
            json_str = re.sub(r'\s+', ' ', json_str)
            
            # Parse JSON
            data = json.loads(json_str)
            evaluations = data.get('evaluations', [])
            
            if not evaluations:
                raise ValueError("No evaluations found in response")
            
            # Transform to database format
            results = []
            current_time = datetime.utcnow().isoformat()
            
            for eval_data in evaluations:
                results.append({
                    'application_id': eval_data.get('application_id'),
                    'match_score': eval_data.get('score'),
                    'match_reasoning': eval_data.get('reasoning'),
                    'match_strengths': json.dumps(eval_data.get('strengths', [])),
                    'match_gaps': json.dumps(eval_data.get('gaps', [])),
                    'match_recommendation': eval_data.get('recommendation', 'Apply'),
                    'evaluated_at': current_time
                })
            
            return results
        
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse AI response as JSON: {e}\n\nResponse preview: {ai_response[:500]}")
    
    def _load_resume_summary(self) -> str:
        """Load and format base resume content"""
        
        if not os.path.exists(self.base_resume_path):
            return "**Base resume not found.** Please ensure base_master_resume.tex exists in data directory."
        
        try:
            with open(self.base_resume_path, 'r') as f:
                content = f.read()
            
            # Extract key sections (simple LaTeX parsing)
            # For now, just return first 2000 chars as summary
            summary = f"""**Years Experience:** 18+ years software engineering
**Management Experience:** 6.5 years (including 3.5 years director-level)
**Current Scope:** Managing 29-person org with 2 engineering managers + 7 ICs

**Key Technical Skills:**
- Languages: Python (expert), Java, JavaScript, TypeScript, Go, C/C++
- Frameworks: React, Flask, Falcon, eventlet
- Infrastructure: Kubernetes, Docker, AWS, Kafka, PostgreSQL, MongoDB, Redis
- Domains: Distributed systems, cloud platforms, data platforms, CI/CD, DevOps

**Key Achievements:**
- CI/CD transformation: 86% build time reduction (8hrs → 40min), 450+ developers impacted
- Cloud platforms serving 10,000+ production customers
- Monitoring platform processing 1M+ entities with sub-second response times
- Promoted 2 ICs into successful management roles
- Led organizations up to 45 people across Dev/Test/DevOps

**Management Strengths:**
- Managing managers and engineers at scale
- Cross-functional collaboration with product, design, executive leadership
- Operational excellence and reliability focus
- Career development and mentorship
- Technical vision and architecture decisions

Resume excerpt:
{content[:1500]}...
"""
            return summary
            
        except Exception as e:
            return f"**Error loading resume:** {e}"
    
    def _load_source_material_summary(self) -> str:
        """Load and summarize source material"""
        
        if not os.path.exists(self.source_material_dir):
            return "**Source material directory not found.**"
        
        try:
            summaries = []
            
            # Read markdown files from source material
            for filename in sorted(os.listdir(self.source_material_dir)):
                if filename.endswith('.md'):
                    filepath = os.path.join(self.source_material_dir, filename)
                    with open(filepath, 'r') as f:
                        content = f.read()
                    
                    # Extract first paragraph or first 300 chars
                    preview = content.split('\n\n')[0][:300]
                    summaries.append(f"**{filename}:** {preview}...")
            
            if summaries:
                return "\n\n".join(summaries)
            else:
                return "**No source material markdown files found.**"
                
        except Exception as e:
            return f"**Error loading source material:** {e}"


def generate_scoring_prompt(applications: List[Dict], data_dir: str = '/data') -> str:
    """
    Convenience function to generate scoring prompt.
    
    Args:
        applications: List of application dicts
        data_dir: Path to data directory
        
    Returns:
        Prompt text
    """
    scorer = JobScorer(data_dir)
    return scorer.generate_bulk_prompt(applications)


def parse_scoring_response(ai_response: str) -> List[Dict]:
    """
    Convenience function to parse AI scoring response.
    
    Args:
        ai_response: JSON response from AI
        
    Returns:
        List of parsed scoring results
    """
    scorer = JobScorer(data_dir='/data')  # data_dir not used for parsing
    return scorer.parse_scores(ai_response)
