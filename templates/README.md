# LaTeX Resume Templates

This directory is for storing LaTeX resume and cover letter templates used by the job search toolkit.

## Template Files

Place your `.tex` template files here. Common templates include:

- `base_resume.tex` - Standard resume format
- `manager_resume.tex` - Management-focused resume
- `director_resume.tex` - Executive-level resume
- `cover_letter.tex` - Cover letter template

## Template Variables

Templates should use placeholder variables that will be replaced by the application:

- `{{CANDIDATE_NAME}}` - Your name
- `{{CANDIDATE_EMAIL}}` - Your email
- `{{CANDIDATE_PHONE}}` - Your phone number
- `{{POSITION}}` - The job title you're applying for
- `{{COMPANY}}` - The company name
- `{{SKILLS}}` - Relevant skills for the position
- `{{EXPERIENCE}}` - Work experience section
- `{{EDUCATION}}` - Education section

## Custom Templates

You can also create custom templates in your data directory at:
```
/data/custom_templates/
```

These will take precedence over the default templates in this directory.

## Usage

When creating a new application, specify which template to use in the `config.txt` file:

```
template=base_resume
```

The system will look for `base_resume.tex` in:
1. `/data/custom_templates/` (your custom templates)
2. `/app/templates/` (default templates, this directory)

## Example Template Structure

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}

\begin{document}

\section*{{{CANDIDATE_NAME}}}
\texttt{{{CANDIDATE_EMAIL}}} | {{CANDIDATE_PHONE}}

\section*{Objective}
Seeking the position of {{POSITION}} at {{COMPANY}}.

\section*{Skills}
{{SKILLS}}

\section*{Experience}
{{EXPERIENCE}}

\section*{Education}
{{EDUCATION}}

\end{document}
```

## Compiling

Templates are compiled automatically by the system using `pdflatex`. You can also compile manually:

```bash
cd /data/applications/CompanyName_JobTitle/
pdflatex resume.tex
```
