# MCP Server: stdio → HTTP/SSE Migration

## Goal

Move the Rust MCP server from stdio transport (requires a local binary spawned by Claude Code) to
HTTP/SSE transport running **inside the Docker container**. This makes the MCP server portable —
no local binary, no platform-specific build steps.

## Target Architecture

```
Claude Code  <--HTTP/SSE (port 3000)-->  [Docker]
                                           ├── Rust MCP server  (:3000)
                                           └── FastAPI app      (:8000)
                                                     ↑
                                         MCP server calls API internally
```

The MCP server already proxies the FastAPI API over HTTP. Inside the container both services share
`localhost`, so `JOB_TRACKER_URL=http://localhost:8000` continues to work unchanged.

## Why Not stdio

- stdio MCP servers are spawned as a **local process** by Claude Code.
- Requires the binary to be built and present on the host machine.
- Platform-dependent (macOS/Linux binary, must be rebuilt on each machine).
- HTTP/SSE transport runs as a network service — just a URL in settings.

## Implementation Steps

### 1. Switch `rmcp` transport feature (`Cargo.toml`)

Replace `transport-io` with `transport-sse-server`:

```toml
rmcp = { version = "0.8", features = ["server", "transport-sse-server", "macros"] }
```

`transport-sse-server` pulls in `axum` and exposes `rmcp::transport::sse_server::SseServer`.

### 2. Update `main.rs`

Replace the stdio serve call with an SSE server bound to `0.0.0.0:3000`:

```rust
use rmcp::transport::sse_server::{SseServer, SseServerConfig};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let base_url = std::env::var("JOB_TRACKER_URL")
        .unwrap_or_else(|_| "http://localhost:8000".to_string());

    let mcp_port: u16 = std::env::var("MCP_PORT")
        .ok()
        .and_then(|p| p.parse().ok())
        .unwrap_or(3000);

    let server_factory = move || JobTrackerServer::new(base_url.clone());

    let config = SseServerConfig {
        bind: format!("0.0.0.0:{mcp_port}").parse()?,
        sse_path: "/sse".to_string(),
        post_path: "/message".to_string(),
        ct: tokio_util::sync::CancellationToken::new(),
    };

    println!("MCP server listening on :{mcp_port}");
    SseServer::serve_with_config(config, server_factory).await?;
    Ok(())
}
```

> Note: exact API may vary slightly with rmcp 0.8 — verify against crate docs during build.

### 3. Start both processes in the container (`start-uvicorn.sh` → `start.sh`)

The container currently runs only uvicorn. We need a simple supervisor to run both:

```bash
#!/bin/bash
# Start MCP server in background
job-tracker-mcp &
MCP_PID=$!

# Start uvicorn (foreground — container exits when this does)
if [ "$UVICORN_RELOAD" = "1" ]; then
    uvicorn job_tracker.app:app --host 0.0.0.0 --port 8000 --reload
else
    uvicorn job_tracker.app:app --host 0.0.0.0 --port 8000
fi

# Clean up MCP server if uvicorn exits
kill $MCP_PID 2>/dev/null
```

### 4. Expose MCP port in `Dockerfile`

```dockerfile
EXPOSE 8000 3000
```

### 5. Expose MCP port in `docker-compose.yml`

```yaml
ports:
  - "${HOST_PORT:-8000}:8000"
  - "${MCP_PORT:-3000}:3000"
```

### 6. Register in `~/.claude/settings.json`

```json
{
  "mcpServers": {
    "job-tracker": {
      "type": "sse",
      "url": "http://localhost:3000/sse"
    }
  }
}
```

## Files to Change

| File | Change |
|------|--------|
| `mcp-server/Cargo.toml` | `transport-io` → `transport-sse-server` |
| `mcp-server/src/main.rs` | stdio serve → SSE server on port 3000 |
| `start-uvicorn.sh` | Launch both uvicorn and `job-tracker-mcp` |
| `Dockerfile` | `EXPOSE 8000 3000` |
| `docker-compose.yml` | Add port `3000:3000` mapping |
| `~/.claude/settings.json` | Add `mcpServers` entry with SSE URL |

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `JOB_TRACKER_URL` | `http://localhost:8000` | FastAPI base URL (unchanged) |
| `MCP_PORT` | `3000` | Port the MCP SSE server listens on |
