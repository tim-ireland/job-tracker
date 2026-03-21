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

You should see `job-tracker` listed as connected with 11 tools.

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

To add a new tool:
1. Define a parameter struct with `#[derive(Debug, Deserialize, schemars::JsonSchema)]` and `/// doc comments` on each field (these become the JSON Schema descriptions Claude sees)
2. Add an `async fn` annotated with `#[tool(description = "...")]` to the `#[tool_router] impl JobTrackerServer` block
3. Call `self.api_get(path)`, `self.api_post(path, body)`, or `self.api_put(path, body)` as needed
4. Rebuild: `docker compose up --build -d`
