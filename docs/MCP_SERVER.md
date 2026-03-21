# MCP Server

The job tracker includes a Rust-based [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that lets you manage your job search pipeline from Claude Code using natural language — no need to open the web UI for routine updates.

## How It Works

The MCP server binary (`job-tracker-mcp`) is compiled as part of the Docker image and lives at `/usr/local/bin/job-tracker-mcp` inside the container. Claude Code connects to it via `docker exec`, communicating over stdio. The server calls the FastAPI app (`http://localhost:8000`) running in the same container.

```
Claude Code  ──stdio──▶  docker exec  ──▶  job-tracker-mcp  ──HTTP──▶  FastAPI (port 8000)
                          (container)
```

This means:
- No extra ports to expose
- The server is versioned and deployed alongside the app
- You never need a local Rust toolchain

## Setup

### 1. Build the image

The MCP server is compiled automatically during `docker build`. If you're updating from a version before MCP support was added, rebuild:

```bash
docker compose build
docker compose up -d
```

The first build takes a few minutes while Rust dependencies compile. Subsequent builds are fast unless `mcp-server/` changes.

### 2. Register with Claude Code

Add the following to `~/.claude/mcp.json` (create the file if it doesn't exist):

```json
{
  "mcpServers": {
    "job-tracker": {
      "command": "docker",
      "args": [
        "exec", "-i",
        "-e", "JOB_TRACKER_URL=http://localhost:8000",
        "job-search-tracker",
        "/usr/local/bin/job-tracker-mcp"
      ]
    }
  }
}
```

> **Note:** `job-search-tracker` is the container name defined in `docker-compose.yml`. If you've customized it, update the arg accordingly.

### 3. Restart Claude Code

MCP servers are loaded at startup. Restart Claude Code (or open `/mcp` to reload) after editing `mcp.json`.

### 4. Verify the connection

In Claude Code, run `/mcp` — you should see `job-tracker` listed as connected.

## Available Tools

| Tool | Description |
|------|-------------|
| `get_dashboard` | Pipeline summary: totals by status/priority, recent activity, upcoming interviews |
| `list_applications` | List applications, optionally filtered by status or priority |
| `add_application` | Add a new application; creates the company automatically if needed |
| `update_application` | Update status, priority, notes, or date applied |
| `log_interaction` | Record an email, call, meeting, or LinkedIn message |
| `list_interactions` | Show all interactions for an application |
| `schedule_interview` | Add an interview with type, date, interviewer, and meeting link |
| `get_upcoming_interviews` | List interviews scheduled in the future |
| `compare_offers` | Side-by-side comparison of all offers (comp, equity, benefits) |

## Usage Examples

```
"What does my pipeline look like?"
→ calls get_dashboard

"Show me all my P1 applications"
→ calls list_applications with priority=P1

"Add Stripe, Staff Engineer, P1, applied today via LinkedIn"
→ calls add_application (creates Stripe company if needed), then update_application

"I just had a call with the Google recruiter — Sarah Chen. She said they're moving fast."
→ calls log_interaction with type=call, contact_person="Sarah Chen", summary=...

"Schedule a technical interview for my Stripe application, next Thursday at 2pm with meet.google.com/abc-xyz"
→ calls schedule_interview

"Mark my Acme application as closed"
→ calls update_application with status=Closed

"Compare all my offers"
→ calls compare_offers
```

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

**"Error: container not running"**
The Docker container must be running. Start it with `docker compose up -d`.

**MCP server not showing up in `/mcp`**
- Check that `~/.claude/mcp.json` is valid JSON
- Verify the container name matches: `docker ps | grep job-search-tracker`
- Restart Claude Code after editing the config

**"Error fetching dashboard" or similar API errors**
The FastAPI server inside the container may still be starting up. Wait a few seconds and try again. Check container health with `docker compose ps`.

**Rebuilding after changes to `mcp-server/`**
```bash
docker compose build
docker compose up -d
```
Cargo caches layers in Docker, so only changed crates recompile.

## Implementation Notes

The server is written in Rust using the [`rmcp`](https://crates.io/crates/rmcp) crate (the official Rust MCP SDK). Source is in `mcp-server/src/main.rs`. It's a straightforward HTTP client over the existing REST API — no direct database access.

To add a new tool, define a parameter struct with `serde::Deserialize` and `schemars::JsonSchema`, then add an `async fn` annotated with `#[tool(description = "...")]` to the `#[tool_router]` impl block in `main.rs`.
