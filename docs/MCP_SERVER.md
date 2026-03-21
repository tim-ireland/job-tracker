# MCP Server

The job tracker includes a Rust-based [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that lets you manage your job search pipeline from Claude Code using natural language — no need to open the web UI for routine updates.

## Architecture

The MCP server is compiled as part of the Docker image and runs as a persistent SSE (Server-Sent Events) HTTP server on port 3000. Claude Code connects to it directly over HTTP.

```
Claude Code  ──SSE/HTTP──▶  job-tracker-mcp (port 3000)  ──HTTP──▶  FastAPI (port 8000)
                              (inside Docker container)
```

Both the MCP server and the FastAPI backend run inside the same container. The MCP server calls the FastAPI API on `localhost:8000` internally.

## Setup

### 1. Start the stack

```bash
docker compose up -d
```

The MCP server starts automatically alongside the FastAPI app. Port 3000 is exposed to the host.

First build takes a few minutes while Rust dependencies compile. Subsequent builds are fast unless `mcp-server/` changes.

### 2. Configure Claude Code

The project ships with a `.mcp.json` at the repo root and a `.claude/settings.json` that auto-approves it. No manual configuration needed — Claude Code picks these up automatically when you open the project.

If you want to verify the connection:

```
/mcp
```

You should see `job-tracker` listed as connected with 14 tools.

### 3. Use it

Just ask Claude naturally:

```
"What does my pipeline look like?"
"Show me all my P1 applications"
"Update the Stripe application — set priority to P1 and salary to $200k-$220k"
"I just got an offer from Acme: $185k base, $20k bonus, $300k equity, respond by April 10"
"Mark my last Google interview as completed — it went well, next steps TBD"
```

Claude will call the appropriate MCP tool and confirm what was changed.

## Available Tools

### Pipeline Management

| Tool | Description |
|------|-------------|
| `get_dashboard` | Pipeline summary: totals by status/priority, recent activity, upcoming interviews |
| `list_applications` | List applications, optionally filtered by status or priority |
| `add_application` | Add a new application; creates the company automatically if needed |
| `update_application` | Update status, priority, role, salary, location, hiring manager, dates, notes, and more |
| `log_interaction` | Record an email, call, meeting, or LinkedIn message |
| `list_interactions` | Show all interactions for an application |
| `schedule_interview` | Add an interview with type, date, interviewer, and meeting link |
| `update_interview` | Mark an interview complete, reschedule it, or add debrief notes |
| `get_upcoming_interviews` | List interviews scheduled in the future |
| `compare_offers` | Side-by-side comparison of all offers (comp, equity, benefits) |
| `create_offer` | Record a new offer with full compensation details |

### Document Generation

| Tool | Description |
|------|-------------|
| `create_application` | Scaffold an application directory with LaTeX templates and a DB entry |
| `get_application_files` | List files in an application directory with their absolute paths |
| `compile_application` | Run pdflatex and produce resume.pdf and cover_letter.pdf |

## Tailored Resume Workflow

Claude can handle the full document preparation loop without any shell commands:

### 1. Create the application

```
"Create an application for Figma, role Engineering Manager - Observability,
 template: manager, priority P2, salary $250k-$350k"
```

Claude calls `create_application`, which:
- Creates `data/applications/Figma_Engineering_Manager_Observability/`
- Copies `manager_resume.tex` → `resume.tex` and `manager_cover_letter.tex` → `cover_letter.tex`
- Creates a `job_description.txt` placeholder
- Registers the application in the database

### 2. Add the job description

Paste the job posting directly into the conversation, or tell Claude the path if you've already saved it. Claude reads `job_description.txt` and the current `.tex` files via `get_application_files`.

### 3. Let Claude customize the documents

```
"Customize the resume and cover letter for this role. Emphasize the
 observability platform work and Datadog experience."
```

Claude reads `resume.tex` and `cover_letter.tex`, edits them in place to match the job description, and explains what changed.

### 4. Compile to PDF

```
"Compile the Figma application"
```

Claude calls `compile_application`, which runs `pdflatex` twice per document (resolving cross-references), embeds PDF metadata, and cleans up aux files.

### 5. Review, iterate, and mark applied

Open the PDFs to review. If adjustments are needed, ask Claude to refine specific sections, then compile again. When ready:

```
"Mark the Figma application as Applied, set date_applied to today,
 and set resume_filename to resume.pdf"
```

### End-to-end example

```
"Create a manager-template application for Red Hat, ROSA Service EM,
 P2 priority, salary $148k-$245k. Here's the job description: [paste]
 Customize the resume to highlight Kubernetes and cloud infrastructure work,
 then compile it."
```

Claude will scaffold the directory, edit the documents, compile the PDFs, and confirm the output — all in one turn.

### Environment variables

The document tools read two env vars (both set in the Docker container):

| Variable | Default | Purpose |
|----------|---------|---------|
| `DATA_DIR` | `/data` | Root of the data volume; applications go in `$DATA_DIR/applications/` |
| `SCRIPTS_DIR` | `/app/scripts` | Location of `create_application.sh` and `compile_application.sh` |

## Application Statuses

| Status | Meaning |
|--------|---------|
| `Pipeline` | Identified but not yet applied |
| `Applied` | Application submitted |
| `Screening` | Initial recruiter/HR screen |
| `Interview` | Active interview process |
| `Offer` | Offer received |
| `Closed` | Rejected, withdrawn, or accepted |

## Priority Levels

| Priority | Use for |
|----------|---------|
| `P1` | Dream jobs / drop everything |
| `P2` | Strong fits |
| `P3` | Worth pursuing |
| `P4` | Long shots / exploratory (default) |

## Troubleshooting

**MCP server not showing up in `/mcp`**
- Make sure the container is running: `docker compose up -d`
- Verify port 3000 is reachable: `curl http://localhost:3000/sse` (should stream an endpoint event)
- Reload the MCP config: open `/mcp` in Claude Code

**"Error fetching dashboard" or similar API errors**
The FastAPI server may still be starting. Wait a few seconds and retry. Check health: `docker compose ps`.

**Rebuilding after changes to `mcp-server/`**
```bash
docker compose up --build -d
```
Cargo caches layers in Docker, so only changed crates recompile.

## Implementation Notes

The server is written in Rust using the [`rmcp`](https://crates.io/crates/rmcp) crate (the official Rust MCP SDK). Source is in `mcp-server/src/main.rs`. Transport is SSE (`SseServer` from `rmcp::transport::sse_server`), binding to `0.0.0.0:3000` (configurable via `MCP_PORT` env var).

### Adding an API-backed tool

1. Define a parameter struct with `#[derive(Debug, Deserialize, schemars::JsonSchema)]` and `/// doc comments` on each field (these become the JSON Schema descriptions Claude sees)
2. Add an `async fn` annotated with `#[tool(description = "...")]` to the `#[tool_router] impl JobTrackerServer` block
3. Call `self.api_get(path)`, `self.api_post(path, body)`, or `self.api_put(path, body)` as needed
4. Rebuild: `docker compose up --build -d`

### Adding a shell-backed tool

For operations that need to run inside the container (filesystem access, LaTeX compilation, etc.), use `self.run_script(script_name, &args)`:

```rust
async fn my_tool(&self, Parameters(params): Parameters<MyParams>) -> String {
    self.run_script("my_script.sh", &[params.arg1, params.arg2]).await
}
```

`run_script` automatically sets `DATA_DIR` and `FORCE_RUN=1` (bypasses the container detection guard in scripts), captures stdout/stderr, and returns a human-readable result string.
